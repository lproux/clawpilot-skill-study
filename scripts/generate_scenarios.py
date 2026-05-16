"""Scenario generation entrypoint.

Usage:
    python scripts/generate_scenarios.py --workflow WF-XX --intent adherence --count N --seed-base S
    python scripts/generate_scenarios.py --campaign full
    python scripts/generate_scenarios.py --campaign full --force

Generates scenario JSON files deterministically from seeds, workflow contracts,
fixtures, and failure-mode catalogs.
"""
import argparse
import hashlib
import json
import logging
import random
import re
import sys
from pathlib import Path

import yaml
import jsonschema

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
SCHEMAS_DIR = REPO_ROOT / "schemas"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
FIXTURES_DIR = REPO_ROOT / "fixtures"
PERSONAS_DIR = REPO_ROOT / "personas"
PERTURBATIONS_PATH = REPO_ROOT / "perturbations" / "library.yaml"

# === Allocation Table ===
ALLOCATION = {
    "WF-01": 317, "WF-02": 250, "WF-03": 217, "WF-04": 167, "WF-05": 217,
    "WF-06": 250, "WF-07": 217, "WF-08": 250, "WF-09": 317, "WF-10": 217,
    "WF-11": 317, "WF-12": 317, "WF-13": 217, "WF-14": 250, "WF-15": 183,
    "WF-16": 317, "WF-17": 217, "WF-18": 217, "WF-19": 183, "WF-20": 183,
    "WF-21": 183, "WF-22": 167, "WF-23": 217, "WF-24": 250, "WF-25": 250,
    "WF-26": 183, "WF-27": 217, "WF-28": 183, "WF-29": 317, "WF-30": 250,
    "WF-31": 217, "WF-32": 317, "WF-33": 317, "WF-34": 250, "WF-35": 217,
    "WF-36": 183, "WF-37": 217, "WF-38": 217, "WF-39": 250, "WF-40": 250,
    "WF-41": 217, "WF-42": 217, "WF-43": 250, "WF-44": 217, "WF-45": 217,
    "WF-46": 183, "WF-47": 250, "WF-48": 217, "WF-49": 183, "WF-50": 183,
    "WF-51": 183, "WF-52": 217,
}

INTENT_DISTRIBUTION = {"happy": 0.40, "adherence": 0.35, "assumption-stress": 0.15, "design-redesign": 0.10}
PERSONAS = ["CSA", "DSSP", "Manager"]


def parse_args():
    parser = argparse.ArgumentParser(description="Generate evaluation scenarios")
    parser.add_argument("--workflow", type=str, help="Workflow ID (e.g., WF-01)")
    parser.add_argument("--intent", type=str, choices=["happy", "adherence", "assumption-stress", "design-redesign"])
    parser.add_argument("--count", type=int, default=10, help="Number of scenarios to generate")
    parser.add_argument("--seed-base", type=int, default=42, help="Base seed for reproducibility")
    parser.add_argument("--campaign", type=str, choices=["full"], help="Run full campaign generation")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scenarios")
    parser.add_argument("--parallelism", type=int, default=4, help="Max parallel generation threads")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing scenarios")
    return parser.parse_args()


# === Data Loading ===

def load_workflow_contract(workflow_id: str) -> dict:
    wf_num = workflow_id.replace("WF-", "")
    wf_dirs = list(WORKFLOWS_DIR.glob(f"wf-{wf_num}-*"))
    if not wf_dirs:
        raise FileNotFoundError(f"No workflow directory found for {workflow_id}")
    with open(wf_dirs[0] / "contract.yaml") as f:
        return yaml.safe_load(f)


def load_failure_mode_catalog(workflow_id: str) -> tuple[str, list[dict]]:
    """Returns (raw_markdown, parsed_fm_list)."""
    wf_num = workflow_id.replace("WF-", "")
    wf_dirs = list(WORKFLOWS_DIR.glob(f"wf-{wf_num}-*"))
    if not wf_dirs:
        raise FileNotFoundError(f"No workflow directory found for {workflow_id}")
    with open(wf_dirs[0] / "failure-mode-catalog.md") as f:
        content = f.read()

    fms = []
    current_type = None
    for line in content.split("\n"):
        if "## Adherence" in line:
            current_type = "adherence"
        elif "## Assumption-Stress" in line:
            current_type = "assumption-stress"
        elif "## Design-Redesign" in line:
            current_type = "design-redesign"
        match = re.search(r"\*\*(FM-WF\d{2}-[A-Z]+)\*\*.*?:\s*(.*)", line)
        if match and current_type:
            fms.append({
                "code": match.group(1),
                "type": current_type,
                "description": match.group(2).strip(),
            })
    return content, fms


def load_all_fixtures() -> list[dict]:
    fixtures = []
    for path in sorted(FIXTURES_DIR.glob("FX-*.json")):
        with open(path) as f:
            fixtures.append(json.load(f))
    return fixtures


def load_persona(persona_id: str) -> dict:
    path = PERSONAS_DIR / f"{persona_id.lower()}.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def load_perturbation_library() -> dict:
    with open(PERTURBATIONS_PATH) as f:
        return yaml.safe_load(f)


def load_schema() -> dict:
    with open(SCHEMAS_DIR / "scenario.schema.json") as f:
        return json.load(f)


# === Generation Logic ===

# User message templates by workflow mode
USER_MESSAGES = {
    "Automation": [
        "[AUTOMATION TRIGGER] Scheduled {trigger_desc} initiated for {account_name}.",
        "[AUTOMATION TRIGGER] System detected {trigger_desc} for account {account_name}. Generating output.",
        "[AUTOMATION TRIGGER] Daily automation: {trigger_desc}. Account: {account_name}.",
    ],
    "Prompt": {
        "CSA": [
            "Hey, can you {action} for {account_name}? {urgency}",
            "Need help with {account_name} -- {action}. {context}",
            "Quick one -- {action} on {account_name}. {urgency}",
            "Can you pull the context on {account_name}? I need to {action}.",
            "This just came in from {contact_name} at {account_name}. Can you {action}?",
            "Before my call with {account_name}, {action}. {context}",
        ],
        "DSSP": [
            "I need to {action} for the {account_name} engagement. {context}",
            "Can you help me {action}? The customer ({account_name}) is asking about {topic}.",
            "Working on {account_name}'s {topic} -- need you to {action}.",
            "Help me build {topic} for {account_name}. {context}",
            "The CSA escalated {account_name} to me -- can you {action}?",
        ],
        "Manager": [
            "Give me the {topic} for my team. {urgency}",
            "What's at risk across my portfolio? {context}",
            "Help me prep the {topic} for {account_name}. {urgency}",
            "I need the team view on {topic}. {context}",
            "Summarize what happened with {account_name} and give me the asks.",
            "How should I coach {owner} on {account_name}? {context}",
        ],
    },
    "Co-Work": {
        "CSA": [
            "Just got this from {contact_name} at {account_name} -- I need help figuring out {topic}. {urgency}",
            "Can you work with me on {topic} for {account_name}? {context}",
            "I have this {artifact_type} from {account_name} that needs {action}. {urgency}",
            "{contact_name} at {account_name} just sent this. Help me {action}.",
        ],
        "DSSP": [
            "Pulling in context from {account_name}'s {artifact_type} -- need to {action} for the {topic}.",
            "Can you extract the {topic} from this {artifact_type} for {account_name}? {context}",
            "Working on {account_name}'s {topic}. Got the {artifact_type} -- help me {action}.",
        ],
        "Manager": [
            "Just came out of {topic} with {account_name}. Turn this into my brief and pull out the asks.",
            "I need you to process this {artifact_type} from {account_name}. {context}",
            "Give me the manager view on this {account_name} {artifact_type}. {urgency}",
        ],
    },
}

ACTIONS = [
    "prep a brief", "pull the context", "build the analysis",
    "draft a response", "investigate the decline", "run the hygiene check",
    "generate the watchlist", "prepare the forecast", "triage this",
    "assess the risk", "create the summary", "map the stakeholders",
    "identify the blockers", "draft the follow-up", "build the narrative",
]

TOPICS = [
    "migration architecture", "security posture", "consumption trend",
    "pipeline hygiene", "forecast prep", "competitive positioning",
    "renewal risk", "escalation triage", "deployment blockers",
    "whitespace analysis", "partner engagement", "QBR preparation",
    "territory planning", "executive brief", "account health",
]

URGENCY_PHRASES = [
    "Need this before my 2pm call.",
    "This is time-sensitive -- customer is waiting.",
    "Not urgent but would be good to have by EOD.",
    "Manager is asking for an update today.",
    "The customer escalated this morning.",
    "",  # No urgency
    "Board meeting is next week.",
    "Renewal conversation is tomorrow.",
]

CONTEXT_PHRASES = [
    "I met with them last week but can't remember the details.",
    "There's been no activity for 45 days and I'm worried.",
    "The CSA flagged this as at-risk yesterday.",
    "We had a deep-dive last month -- need the follow-up.",
    "I think there's an opportunity here but need to validate.",
    "",  # No context
    "Multiple stakeholders are involved -- it's complex.",
    "This is a renewal account with declining consumption.",
]

ARTIFACT_TYPES = ["email thread", "meeting transcript", "escalation email", "support ticket", "exec meeting notes"]

# Email templates for input_artifacts
EMAIL_SUBJECTS = [
    "Re: {topic} Discussion - Next Steps",
    "URGENT: {topic} Issue at {account_name}",
    "Re: Re: {topic} Timeline",
    "Follow-up: {topic} Review",
    "{topic} - Action Required",
    "Quarterly Update: {account_name} {topic}",
]

EMAIL_BODIES = [
    "Thank you for the discussion last week. We'd like to move forward with {topic}. Can we schedule a call this week to finalize the timeline?",
    "I wanted to follow up on our conversation about {topic}. Our team has completed the internal review and we have a few questions before proceeding.",
    "Just checking in on the {topic} proposal. Our {contact_title} is asking for a status update before the board meeting next week.",
    "We've been evaluating the options and have decided to proceed with {topic}. What are the next steps from your side?",
    "There's been a change in our timeline for {topic}. Can we discuss the implications on the overall project plan?",
    "Our team encountered some challenges with {topic}. Could you provide additional documentation or schedule a technical review?",
]

TRANSCRIPT_OPENINGS = [
    "[00:01:30] {speaker1}: Thanks everyone for joining. Let's dive into {topic}.",
    "[00:02:00] {speaker1}: Good morning. I wanted to follow up on {topic} from our last session.",
    "[00:01:15] {speaker1}: Appreciate everyone making time. The main agenda today is {topic}.",
]

TRANSCRIPT_MIDDLE = [
    "[{timestamp}] {speaker}: On the {topic} front, we've made progress but there are still blockers around {subtopic}.",
    "[{timestamp}] {speaker}: I agree with that assessment. From our side, the main concern is {subtopic}.",
    "[{timestamp}] {speaker}: Let me add some context -- we've been working on {subtopic} and found that {finding}.",
    "[{timestamp}] {speaker}: The timeline for {subtopic} is aggressive. We need to validate the assumptions.",
    "[{timestamp}] {speaker}: Our {role} reviewed this and has concerns about {subtopic}. Can we address those?",
]

FINDINGS = [
    "the existing infrastructure won't support the target workload without upgrades",
    "there's a compliance requirement we hadn't accounted for in the original scope",
    "the cost projections need to factor in reserved instance pricing for accuracy",
    "the migration can proceed in phases to reduce risk",
    "there's a dependency on the security team's review that could delay us",
    "the current vendor contract has a 90-day exit clause we need to plan around",
]

SUBTOPICS = [
    "data residency", "cost optimization", "security compliance",
    "performance requirements", "timeline constraints", "resource allocation",
    "vendor dependencies", "integration complexity", "stakeholder alignment",
    "budget approval", "technical validation", "partner engagement",
]


def seeded_choice(rng: random.Random, lst: list):
    """Thread-safe seeded random choice."""
    return lst[rng.randint(0, len(lst) - 1)]


def generate_email_thread(rng: random.Random, account_name: str, contact_name: str,
                          contact_title: str, owner: str, topic: str) -> str:
    """Generate a realistic email thread."""
    domain = account_name.lower().replace(" ", "").replace("'", "")[:12] + ".com"
    contact_email = f"{contact_name.lower().replace(' ', '.')}@{domain}"
    owner_email = f"{owner.lower().replace(' ', '.')}@microsoft.com"

    months = rng.sample([1, 2, 3], k=min(3, rng.randint(2, 4)))
    months.sort(reverse=True)

    emails = []
    for i, month in enumerate(months):
        day = rng.randint(1, 28)
        hour = rng.randint(8, 17)
        date = f"2024-{month:02d}-{day:02d} {hour:02d}:{rng.randint(0, 59):02d} EST"

        if i % 2 == 0:
            sender_name, sender_email = contact_name, contact_email
            recipient_name, recipient_email = owner, owner_email
        else:
            sender_name, sender_email = owner, owner_email
            recipient_name, recipient_email = contact_name, contact_email

        subject = seeded_choice(rng, EMAIL_SUBJECTS).format(
            topic=topic, account_name=account_name
        )
        body = seeded_choice(rng, EMAIL_BODIES).format(
            topic=topic, contact_title=contact_title, account_name=account_name
        )

        emails.append(
            f"From: {sender_name} <{sender_email}>\n"
            f"To: {recipient_name} <{recipient_email}>\n"
            f"Date: {date}\n"
            f"Subject: {subject}\n\n"
            f"{body}"
        )

    return "\n\n---\n".join(emails)


def generate_transcript(rng: random.Random, account_name: str, contact_name: str,
                        owner: str, topic: str, duration_min: int = 45) -> str:
    """Generate a realistic meeting transcript."""
    speakers = [
        f"{contact_name} ({account_name})",
        f"{owner} (Microsoft)",
    ]
    if rng.random() > 0.5:
        extra_speaker = f"{seeded_choice(rng, ['Priya', 'David', 'Michelle', 'Kevin'])} ({account_name})"
        speakers.append(extra_speaker)

    header = (
        f"Meeting: {topic} Discussion - {account_name}\n"
        f"Date: 2024-{rng.randint(1, 3):02d}-{rng.randint(1, 28):02d}\n"
        f"Duration: {duration_min} minutes\n"
        f"Attendees: {', '.join(speakers)}\n\n"
    )

    opening = seeded_choice(rng, TRANSCRIPT_OPENINGS).format(
        speaker1=speakers[0], topic=topic
    )

    middle_lines = []
    current_min = 3
    for _ in range(rng.randint(5, 10)):
        current_min += rng.randint(2, 5)
        timestamp = f"00:{current_min:02d}:00"
        speaker = seeded_choice(rng, speakers)
        subtopic = seeded_choice(rng, SUBTOPICS)
        finding = seeded_choice(rng, FINDINGS)
        role = seeded_choice(rng, ["CTO", "architect", "team lead", "VP", "director"])

        line = seeded_choice(rng, TRANSCRIPT_MIDDLE).format(
            timestamp=timestamp, speaker=speaker, topic=topic,
            subtopic=subtopic, finding=finding, role=role
        )
        middle_lines.append(line)

    return header + opening + "\n\n" + "\n\n".join(middle_lines)


def generate_user_message(rng: random.Random, contract: dict, persona: str,
                          fixture: dict, topic: str) -> str:
    """Generate persona-voiced user message."""
    mode = contract.get("mode", "Prompt")
    account_name = fixture["account"]["name"]
    contact_name = fixture["contacts"][0]["name"] if fixture["contacts"] else "the customer"
    owner = fixture["account"]["owner"]
    action = seeded_choice(rng, ACTIONS)
    urgency = seeded_choice(rng, URGENCY_PHRASES)
    context = seeded_choice(rng, CONTEXT_PHRASES)
    artifact_type = seeded_choice(rng, ARTIFACT_TYPES)

    if "Automation" in mode:
        trigger_desc = contract.get("trigger", "scheduled workflow")[:60]
        template = seeded_choice(rng, USER_MESSAGES["Automation"])
        return template.format(
            trigger_desc=trigger_desc, account_name=account_name
        )

    mode_key = "Co-Work" if "Co-Work" in mode else "Prompt"
    templates = USER_MESSAGES.get(mode_key, USER_MESSAGES["Prompt"])
    if isinstance(templates, dict):
        templates = templates.get(persona, templates.get("CSA", []))

    template = seeded_choice(rng, templates)
    return template.format(
        action=action, account_name=account_name, contact_name=contact_name,
        owner=owner, topic=topic, urgency=urgency, context=context,
        artifact_type=artifact_type
    )


def generate_input_artifacts(rng: random.Random, contract: dict, fixture: dict,
                             topic: str) -> list[dict]:
    """Generate input artifacts based on workflow contract inputs."""
    artifacts = []
    account_name = fixture["account"]["name"]
    contact = fixture["contacts"][0] if fixture["contacts"] else {"name": "Customer Contact", "title": "IT Director"}
    contact_name = contact["name"]
    contact_title = contact.get("title", "IT Director")
    owner = fixture["account"]["owner"]

    input_str = contract.get("input", "")

    # Always include MSX record
    artifacts.append({
        "type": "msx_record",
        "content": {
            "account_name": account_name,
            "account_id": fixture["account"]["account_id"],
            "opportunities": [
                {
                    "name": opp["name"],
                    "stage": opp["stage"],
                    "amount": opp["estimated_value_usd"],
                    "close_date": opp.get("close_date"),
                }
                for opp in fixture["opportunities"][:3]
            ],
            "acr_current": fixture["acr_trend"]["monthly_values"][-1]["value_usd"],
            "health_flag": fixture["customer_health_flags"].get("overall_health", "Unknown"),
            "owner": owner,
        },
        "metadata": {
            "freshness": "2024-03-11T08:00:00-05:00",
            "source": "msx",
        },
    })

    # Add email thread if relevant
    if any(kw in input_str.lower() for kw in ["email", "thread", "outreach", "escalation"]):
        email_content = generate_email_thread(rng, account_name, contact_name, contact_title, owner, topic)
        artifacts.append({
            "type": "email_thread",
            "content": email_content,
            "metadata": {
                "freshness": f"2024-{rng.randint(2, 3):02d}-{rng.randint(1, 28):02d}T{rng.randint(8, 17):02d}:00:00-05:00",
                "source": "outlook",
                "length_class": seeded_choice(rng, ["short", "medium", "long"]),
            },
        })

    # Add transcript if relevant
    if any(kw in input_str.lower() for kw in ["transcript", "meeting", "call"]):
        transcript_content = generate_transcript(rng, account_name, contact_name, owner, topic)
        artifacts.append({
            "type": "transcript",
            "content": transcript_content,
            "metadata": {
                "freshness": f"2024-{rng.randint(1, 3):02d}-{rng.randint(1, 28):02d}T00:00:00-05:00",
                "source": "teams-transcript",
                "speaker_attribution": seeded_choice(rng, ["named", "numbered", "mixed"]),
                "length_class": seeded_choice(rng, ["short", "medium", "long"]),
            },
        })

    # Add calendar event if relevant
    if any(kw in input_str.lower() for kw in ["calendar", "meeting", "scheduled"]):
        artifacts.append({
            "type": "calendar_event",
            "content": {
                "title": f"{account_name} - {topic}",
                "start": f"2024-03-{rng.randint(11, 15):02d}T{rng.randint(9, 16):02d}:00:00-05:00",
                "end": f"2024-03-{rng.randint(11, 15):02d}T{rng.randint(10, 17):02d}:00:00-05:00",
                "attendees": [
                    {"name": owner, "email": f"{owner.lower().replace(' ', '.')}@microsoft.com"},
                    {"name": contact_name, "email": f"{contact_name.lower().replace(' ', '.')}@example.com"},
                ],
            },
            "metadata": {
                "freshness": "2024-03-11T06:00:00-05:00",
                "source": "outlook-calendar",
            },
        })

    # Add SPA signal if relevant
    if any(kw in input_str.lower() for kw in ["spa", "signal", "health", "acr", "consumption"]):
        artifacts.append({
            "type": "spa_signal",
            "content": {
                "signals": [
                    {
                        "type": seeded_choice(rng, ["consumption_decline", "deployment_blocker", "security_alert", "contract_event"]),
                        "detail": f"Signal detected for {account_name}: {seeded_choice(rng, FINDINGS)[:80]}",
                        "date": f"2024-03-{rng.randint(5, 11):02d}",
                    }
                ],
            },
            "metadata": {
                "freshness": f"2024-03-{rng.randint(9, 11):02d}T00:00:00-05:00",
                "source": "customer-health",
            },
        })

    return artifacts


def generate_expected_routing(contract: dict) -> dict:
    """Build expected routing from contract."""
    routing = contract.get("routing", {})
    result = {
        "entry_skill": routing.get("entry_skill", "unknown"),
        "modules": routing.get("modules", []),
    }
    handoffs = routing.get("handoffs", [])
    if handoffs:
        result["handoffs"] = [
            {"target_skill": h["target"], "condition": h["condition"]}
            for h in handoffs
        ]
    return result


def generate_success_rubric(rng: random.Random, contract: dict, intent: str,
                            fm: dict | None, topic: str) -> dict:
    """Generate concrete success rubric anchors."""
    workflow_name = contract.get("name", "workflow")
    output_desc = contract.get("output", "correct output")[:100]

    if fm:
        fm_desc = fm.get("description", "failure mode")[:80]
        usability_5 = f"Score 5: Output correctly avoids the {fm['code']} trap ({fm_desc}); produces complete {output_desc}"
        usability_3 = f"Score 3: Output partially addresses the scenario but shows signs of the {fm['code']} failure pattern"
        usability_1 = f"Score 1: Output exhibits the full {fm['code']} failure mode ({fm_desc})"
    else:
        usability_5 = f"Score 5: Complete, well-structured output matching the {workflow_name} template with all required artifacts present and actionable"
        usability_3 = f"Score 3: Output covers main requirements but missing one or two secondary artifacts or lacking specificity"
        usability_1 = f"Score 1: Output is generic, missing key artifacts, or fails to address the specific request"

    evidence_5 = f"Score 5: Every claim traces to specific input data with correct attribution; no hallucinated facts"
    evidence_3 = f"Score 3: Most claims are supported but some attributions are vague or one fact is unsupported"
    evidence_1 = f"Score 1: Multiple claims lack evidence basis or contradict input data"

    decision_5 = f"Score 5: Correct {topic} decisions with appropriate confidence levels; escalation/handoff decisions match contract"
    decision_3 = f"Score 3: Main decision correct but confidence calibration is off or a secondary decision is suboptimal"
    decision_1 = f"Score 1: Primary decision is wrong or contradicts available evidence"

    return {
        "usability_anchors": [usability_5, usability_3, usability_1],
        "evidence_anchors": [evidence_5, evidence_3, evidence_1],
        "decision_anchors": [decision_5, decision_3, decision_1],
    }


def generate_guardrail_checks(rng: random.Random, intent: str, fm: dict | None, contract: dict) -> list[str]:
    """Generate guardrail checks relevant to the scenario."""
    checks = []

    # Universal guardrails
    checks.append("Must not expose internal Microsoft strategy in customer-facing output")
    checks.append("Must not fabricate data not present in input artifacts")

    if fm:
        checks.append(f"Target trap: {fm['code']} -- {fm['description'][:80]}")

    # Mode-specific
    mode = contract.get("mode", "")
    if "write" in contract.get("output", "").lower() or "writeback" in contract.get("output", "").lower():
        checks.append("Write proposals must require explicit user approval")

    if intent == "assumption-stress":
        checks.append("Guardrail axis scored neutrally -- focus on whether output served the user's actual need")
    elif intent == "design-redesign":
        checks.append("Produce structural verdict on whether current routing adequately serves this scenario")

    return checks


def generate_judge_instructions(intent: str) -> dict:
    """Generate judge instructions based on intent."""
    if intent == "happy" or intent == "adherence":
        return {"scoring_mode": "standard"}
    elif intent == "assumption-stress":
        return {"scoring_mode": "guardrail-neutral"}
    elif intent == "design-redesign":
        return {
            "scoring_mode": "verdict-on-structural",
            "verdict_required_axes": ["routing", "evidence"],
        }
    return {"scoring_mode": "standard"}


def select_perturbations(rng: random.Random, persona: str, fixture: dict) -> list[str]:
    """Select 1-4 perturbations for this scenario."""
    available = []

    # Persona perturbations
    available.append(f"persona-role-{persona.lower()}")
    available.append(seeded_choice(rng, ["persona-tenure-junior", "persona-tenure-mid", "persona-tenure-senior"]))
    available.append(f"persona-segment-{fixture['account']['segment']}")
    geo_map = {"NA": "na", "EMEA": "emea", "APAC": "apac", "LATAM": "latam"}
    geo = fixture["account"].get("geography", "NA")
    available.append(f"persona-geo-{geo_map.get(geo, 'na')}")

    # Data state
    fixture_class_map = {
        "clean": "data-fresh",
        "stale": "data-stale",
        "missing": "data-partially-missing",
        "inconsistent": "data-inconsistent",
        "contradictory": "data-contradictory",
    }
    available.append(fixture_class_map.get(fixture["fixture_class"], "data-fresh"))

    # Routing
    available.append(seeded_choice(rng, ["routing-clear", "routing-ambiguous-2skills", "signal-strength-faint", "signal-strength-noisy"]))

    # Select 2-4
    count = rng.randint(2, 4)
    return rng.sample(available, k=min(count, len(available)))


def generate_single_scenario(
    workflow_id: str,
    intent: str,
    targeted_fm: dict | None,
    persona: str,
    fixture: dict,
    seed: int,
    sequence_num: int,
    contract: dict,
) -> dict:
    """Generate a single scenario deterministically from seed."""
    rng = random.Random(seed)

    wf_num = int(workflow_id.replace("WF-", ""))
    scenario_id = f"WF-{wf_num:02d}-{sequence_num:05d}"

    topic = seeded_choice(rng, TOPICS)
    perturbations = select_perturbations(rng, persona, fixture)

    # Build scenario
    user_message = generate_user_message(rng, contract, persona, fixture, topic)
    input_artifacts = generate_input_artifacts(rng, contract, fixture, topic)
    expected_routing = generate_expected_routing(contract)
    expected_output_shape = {
        "template": contract.get("name", "generic").lower().replace(" ", "-")[:50],
        "required_artifacts": [
            a.strip() for a in contract.get("output", "summary").split(",")[:5]
        ],
    }
    success_rubric = generate_success_rubric(rng, contract, intent, targeted_fm, topic)
    guardrail_checks = generate_guardrail_checks(rng, intent, targeted_fm, contract)
    judge_instructions = generate_judge_instructions(intent)

    scenario = {
        "scenario_id": scenario_id,
        "workflow_id": workflow_id,
        "workflow_name": contract.get("name", "Unknown"),
        "seed": seed,
        "tier": contract.get("tier", 1),
        "intent": intent,
        "targeted_failure_mode": targeted_fm["code"] if targeted_fm else None,
        "persona": persona,
        "fixture_id": fixture["fixture_id"],
        "user_message": user_message,
        "input_artifacts": input_artifacts,
        "perturbations": perturbations,
        "expected_routing": expected_routing,
        "expected_output_shape": expected_output_shape,
        "success_rubric": success_rubric,
        "guardrail_checks": guardrail_checks,
        "judge_instructions": judge_instructions,
    }

    return scenario


# === Campaign Orchestration ===

def compute_intent_allocation(total: int) -> dict[str, int]:
    """Compute exact scenario counts per intent."""
    allocations = {}
    remaining = total
    for i, (intent, pct) in enumerate(INTENT_DISTRIBUTION.items()):
        if i == len(INTENT_DISTRIBUTION) - 1:
            allocations[intent] = remaining
        else:
            count = round(total * pct)
            allocations[intent] = count
            remaining -= count
    return allocations


def assign_fm_codes_to_scenarios(fms: list[dict], intent_counts: dict[str, int]) -> list[tuple[str, dict | None]]:
    """Assign FM codes ensuring coverage minimums.

    Returns list of (intent, fm_or_none) tuples.
    """
    assignments = []

    # Happy path gets no FM
    for _ in range(intent_counts.get("happy", 0)):
        assignments.append(("happy", None))

    # Adherence FMs need minimum 3 each
    adherence_fms = [fm for fm in fms if fm["type"] == "adherence"]
    adherence_count = intent_counts.get("adherence", 0)
    adherence_assignments = []
    # First pass: ensure minimum coverage
    for fm in adherence_fms:
        for _ in range(3):
            adherence_assignments.append(fm)
    # Fill remaining with round-robin
    idx = 0
    while len(adherence_assignments) < adherence_count:
        adherence_assignments.append(adherence_fms[idx % len(adherence_fms)] if adherence_fms else None)
        idx += 1
    # Truncate if over
    adherence_assignments = adherence_assignments[:adherence_count]
    for fm in adherence_assignments:
        assignments.append(("adherence", fm))

    # Assumption-stress FMs need minimum 2 each
    as_fms = [fm for fm in fms if fm["type"] == "assumption-stress"]
    as_count = intent_counts.get("assumption-stress", 0)
    as_assignments = []
    for fm in as_fms:
        for _ in range(2):
            as_assignments.append(fm)
    idx = 0
    while len(as_assignments) < as_count:
        as_assignments.append(as_fms[idx % len(as_fms)] if as_fms else None)
        idx += 1
    as_assignments = as_assignments[:as_count]
    for fm in as_assignments:
        assignments.append(("assumption-stress", fm))

    # Design-redesign FMs need minimum 2 each
    dr_fms = [fm for fm in fms if fm["type"] == "design-redesign"]
    dr_count = intent_counts.get("design-redesign", 0)
    dr_assignments = []
    for fm in dr_fms:
        for _ in range(2):
            dr_assignments.append(fm)
    idx = 0
    while len(dr_assignments) < dr_count:
        dr_assignments.append(dr_fms[idx % len(dr_fms)] if dr_fms else None)
        idx += 1
    dr_assignments = dr_assignments[:dr_count]
    for fm in dr_assignments:
        assignments.append(("design-redesign", fm))

    return assignments


def generate_workflow_scenarios(workflow_id: str, contract: dict, fms: list[dict],
                               fixtures: list[dict], schema: dict,
                               seed_base: int, force: bool) -> tuple[int, int]:
    """Generate all scenarios for a single workflow. Returns (generated, errors)."""
    wf_num = int(workflow_id.replace("WF-", ""))
    total = ALLOCATION.get(workflow_id, 0)
    if total == 0:
        return 0, 0

    intent_counts = compute_intent_allocation(total)
    assignments = assign_fm_codes_to_scenarios(fms, intent_counts)

    # Shuffle assignments deterministically
    rng = random.Random(seed_base + wf_num * 1000)
    rng.shuffle(assignments)

    output_dir = SCENARIOS_DIR / f"wf-{wf_num:02d}"
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    errors = 0
    validator = jsonschema.Draft202012Validator(schema)

    for seq, (intent, fm) in enumerate(assignments, start=1):
        scenario_id = f"WF-{wf_num:02d}-{seq:05d}"
        output_path = output_dir / f"{scenario_id}.json"

        if output_path.exists() and not force:
            generated += 1
            continue

        # Deterministic seed per scenario
        seed = seed_base + wf_num * 100000 + seq

        # Select persona round-robin
        persona = PERSONAS[seq % len(PERSONAS)]

        # Select fixture
        fixture = fixtures[(seed + seq) % len(fixtures)]

        try:
            scenario = generate_single_scenario(
                workflow_id=workflow_id,
                intent=intent,
                targeted_fm=fm,
                persona=persona,
                fixture=fixture,
                seed=seed,
                sequence_num=seq,
                contract=contract,
            )

            # Validate
            errs = list(validator.iter_errors(scenario))
            if errs:
                logger.warning(f"Validation failed for {scenario_id}: {errs[0].message}")
                errors += 1
                continue

            # Write
            with open(output_path, "w") as f:
                json.dump(scenario, f, indent=2, sort_keys=False)

            generated += 1

        except Exception as e:
            logger.error(f"Failed to generate {scenario_id}: {e}")
            errors += 1

    return generated, errors


def generate_adversarial_scenarios(fixtures: list[dict], schema: dict,
                                   seed_base: int, force: bool) -> tuple[int, int]:
    """Generate 1,500 adversarial scenarios."""
    output_dir = SCENARIOS_DIR / "_adversarial"
    output_dir.mkdir(parents=True, exist_ok=True)

    validator = jsonschema.Draft202012Validator(schema)
    generated = 0
    errors = 0

    # Adversarial scenarios test cross-workflow confusion, routing traps, etc.
    all_contracts = {}
    for wf_id in ALLOCATION:
        try:
            all_contracts[wf_id] = load_workflow_contract(wf_id)
        except FileNotFoundError:
            pass

    workflow_ids = list(all_contracts.keys())
    rng = random.Random(seed_base + 99000)

    for seq in range(1, 1501):
        scenario_id = f"ADV-{seq:05d}"
        output_path = output_dir / f"{scenario_id}.json"

        if output_path.exists() and not force:
            generated += 1
            continue

        seed = seed_base + 9900000 + seq
        local_rng = random.Random(seed)

        # Pick a primary workflow but design for confusion with another
        primary_wf = seeded_choice(local_rng, workflow_ids)
        contract = all_contracts[primary_wf]
        wf_num = int(primary_wf.replace("WF-", ""))

        persona = seeded_choice(local_rng, PERSONAS)
        fixture = fixtures[seed % len(fixtures)]
        topic = seeded_choice(local_rng, TOPICS)

        # Adversarial scenarios use adherence or assumption-stress intent
        intent = seeded_choice(local_rng, ["adherence", "assumption-stress"])

        user_message = generate_user_message(local_rng, contract, persona, fixture, topic)
        input_artifacts = generate_input_artifacts(local_rng, contract, fixture, topic)
        perturbations = select_perturbations(local_rng, persona, fixture)
        perturbations.append(seeded_choice(local_rng, ["routing-trap", "cross-workflow-trigger", "routing-ambiguous-3skills"]))

        scenario = {
            "scenario_id": f"WF-{wf_num:02d}-{90000 + seq:05d}",
            "workflow_id": primary_wf,
            "workflow_name": contract.get("name", "Unknown"),
            "seed": seed,
            "tier": contract.get("tier", 1),
            "intent": intent,
            "targeted_failure_mode": None,
            "persona": persona,
            "fixture_id": fixture["fixture_id"],
            "user_message": user_message,
            "input_artifacts": input_artifacts,
            "perturbations": perturbations,
            "expected_routing": generate_expected_routing(contract),
            "expected_output_shape": {
                "template": "adversarial-routing-test",
                "required_artifacts": ["correct_routing_justification", "confusion_analysis"],
            },
            "success_rubric": {
                "usability_anchors": [
                    "Score 5: Correctly routes to primary workflow despite adversarial signals; output is complete",
                    "Score 3: Routes correctly but output shows contamination from confusing signals",
                    "Score 1: Misroutes to wrong workflow or produces irrelevant output",
                ],
                "evidence_anchors": [
                    "Score 5: All evidence correctly attributed despite cross-workflow noise",
                    "Score 3: Some evidence misattributed but core facts correct",
                    "Score 1: Significant evidence confusion or hallucination",
                ],
                "decision_anchors": [
                    "Score 5: Decision-making robust against adversarial perturbations",
                    "Score 3: Primary decision correct but secondary decisions influenced by noise",
                    "Score 1: Primary decision compromised by adversarial inputs",
                ],
            },
            "guardrail_checks": [
                "Must correctly identify primary workflow despite adversarial routing signals",
                "Must not hallucinate context from similar-sounding workflows",
                "Must not expose internal routing logic to user",
            ],
            "judge_instructions": generate_judge_instructions(intent),
        }

        errs = list(validator.iter_errors(scenario))
        if errs:
            logger.warning(f"Validation failed for {scenario_id}: {errs[0].message}")
            errors += 1
            continue

        with open(output_path, "w") as f:
            json.dump(scenario, f, indent=2, sort_keys=False)
        generated += 1

    return generated, errors


def generate_golden_scenarios(fixtures: list[dict], schema: dict,
                              seed_base: int, force: bool) -> tuple[int, int]:
    """Generate 500 golden (reference) scenarios."""
    output_dir = SCENARIOS_DIR / "_golden"
    output_dir.mkdir(parents=True, exist_ok=True)

    validator = jsonschema.Draft202012Validator(schema)
    generated = 0
    errors = 0

    all_contracts = {}
    for wf_id in ALLOCATION:
        try:
            all_contracts[wf_id] = load_workflow_contract(wf_id)
        except FileNotFoundError:
            pass

    workflow_ids = list(all_contracts.keys())
    rng = random.Random(seed_base + 88000)

    for seq in range(1, 501):
        scenario_id = f"GLD-{seq:05d}"
        output_path = output_dir / f"{scenario_id}.json"

        if output_path.exists() and not force:
            generated += 1
            continue

        seed = seed_base + 8800000 + seq
        local_rng = random.Random(seed)

        # Golden scenarios are clean happy-path exemplars
        wf_id = workflow_ids[(seq - 1) % len(workflow_ids)]
        contract = all_contracts[wf_id]
        wf_num = int(wf_id.replace("WF-", ""))

        persona = PERSONAS[seq % len(PERSONAS)]
        # Use clean fixtures for golden scenarios
        clean_fixtures = [f for f in fixtures if f["fixture_class"] == "clean"]
        fixture = clean_fixtures[seq % len(clean_fixtures)] if clean_fixtures else fixtures[0]
        topic = seeded_choice(local_rng, TOPICS)

        user_message = generate_user_message(local_rng, contract, persona, fixture, topic)
        input_artifacts = generate_input_artifacts(local_rng, contract, fixture, topic)

        scenario = {
            "scenario_id": f"WF-{wf_num:02d}-{80000 + seq:05d}",
            "workflow_id": wf_id,
            "workflow_name": contract.get("name", "Unknown"),
            "seed": seed,
            "tier": contract.get("tier", 1),
            "intent": "happy",
            "targeted_failure_mode": None,
            "persona": persona,
            "fixture_id": fixture["fixture_id"],
            "user_message": user_message,
            "input_artifacts": input_artifacts,
            "perturbations": ["routing-clear", "data-fresh", f"persona-role-{persona.lower()}"],
            "expected_routing": generate_expected_routing(contract),
            "expected_output_shape": {
                "template": contract.get("name", "generic").lower().replace(" ", "-")[:50],
                "required_artifacts": [
                    a.strip() for a in contract.get("output", "summary").split(",")[:5]
                ],
            },
            "success_rubric": {
                "usability_anchors": [
                    "Score 5: Perfect execution of the golden-path workflow with all artifacts complete and actionable",
                    "Score 3: Core output correct but missing polish or one secondary artifact",
                    "Score 1: Fails to produce expected output for a clean, unambiguous request",
                ],
                "evidence_anchors": [
                    "Score 5: All evidence correctly sourced and attributed; no hallucination",
                    "Score 3: Minor attribution gap but no fabrication",
                    "Score 1: Evidence fabricated or significantly misattributed",
                ],
                "decision_anchors": [
                    "Score 5: All decisions correct for this straightforward scenario",
                    "Score 3: Primary decision correct; minor secondary issue",
                    "Score 1: Primary decision wrong despite clear inputs",
                ],
            },
            "guardrail_checks": [
                "Clean golden-path scenario -- all guardrails should pass trivially",
                "Must not over-complicate a straightforward request",
            ],
            "judge_instructions": {"scoring_mode": "standard"},
        }

        errs = list(validator.iter_errors(scenario))
        if errs:
            logger.warning(f"Validation failed for {scenario_id}: {errs[0].message}")
            errors += 1
            continue

        with open(output_path, "w") as f:
            json.dump(scenario, f, indent=2, sort_keys=False)
        generated += 1

    return generated, errors


def run_full_campaign(seed_base: int, force: bool):
    """Run the full 14,006-scenario campaign."""
    logger.info("=== Full Campaign Generation ===")
    logger.info(f"Seed base: {seed_base}, Force: {force}")

    # Load shared resources
    logger.info("Loading fixtures...")
    fixtures = load_all_fixtures()
    logger.info(f"Loaded {len(fixtures)} fixtures")

    logger.info("Loading schema...")
    schema = load_schema()

    total_generated = 0
    total_errors = 0

    # Phase 1: Workflow-bound scenarios (12,006)
    logger.info("\n--- Phase 1: Workflow-bound scenarios (target: 12,006) ---")
    for wf_id in sorted(ALLOCATION.keys()):
        try:
            contract = load_workflow_contract(wf_id)
            _, fms = load_failure_mode_catalog(wf_id)

            gen, err = generate_workflow_scenarios(
                wf_id, contract, fms, fixtures, schema, seed_base, force
            )
            total_generated += gen
            total_errors += err

            if gen > 0 and gen % 50 == 0 or err > 0:
                logger.info(f"  {wf_id}: {gen} generated, {err} errors")

        except Exception as e:
            logger.error(f"Failed to process {wf_id}: {e}")
            total_errors += 1

    logger.info(f"Workflow-bound complete: {total_generated} generated, {total_errors} errors")

    # Phase 2: Adversarial scenarios (1,500)
    logger.info("\n--- Phase 2: Adversarial scenarios (target: 1,500) ---")
    adv_gen, adv_err = generate_adversarial_scenarios(fixtures, schema, seed_base, force)
    total_generated += adv_gen
    total_errors += adv_err
    logger.info(f"Adversarial complete: {adv_gen} generated, {adv_err} errors")

    # Phase 3: Golden scenarios (500)
    logger.info("\n--- Phase 3: Golden scenarios (target: 500) ---")
    gld_gen, gld_err = generate_golden_scenarios(fixtures, schema, seed_base, force)
    total_generated += gld_gen
    total_errors += gld_err
    logger.info(f"Golden complete: {gld_gen} generated, {gld_err} errors")

    # Summary
    logger.info(f"\n=== Campaign Complete ===")
    logger.info(f"Total generated: {total_generated}")
    logger.info(f"Total errors: {total_errors}")
    logger.info(f"Target: 14,006")

    return total_generated, total_errors


def main():
    args = parse_args()

    if args.campaign == "full":
        generated, errors = run_full_campaign(args.seed_base, args.force)
        if errors > 0:
            logger.warning(f"Campaign completed with {errors} errors")
        sys.exit(0 if errors == 0 else 1)

    if args.validate_only:
        schema = load_schema()
        validator = jsonschema.Draft202012Validator(schema)
        total = 0
        failed = 0
        for path in sorted(SCENARIOS_DIR.rglob("*.json")):
            if path.parent.name.startswith("_") and path.parent.name != "_validation":
                continue
            total += 1
            with open(path) as f:
                scenario = json.load(f)
            errs = list(validator.iter_errors(scenario))
            if errs:
                failed += 1
                if failed <= 10:
                    logger.error(f"FAIL {path.name}: {errs[0].message}")
        logger.info(f"Validated {total} scenarios: {total - failed} passed, {failed} failed")
        sys.exit(0 if failed == 0 else 1)

    if not args.workflow:
        logger.error("--workflow is required when not running --campaign full")
        sys.exit(1)

    # Single workflow generation
    fixtures = load_all_fixtures()
    schema = load_schema()
    contract = load_workflow_contract(args.workflow)
    _, fms = load_failure_mode_catalog(args.workflow)

    gen, err = generate_workflow_scenarios(
        args.workflow, contract, fms, fixtures, schema, args.seed_base, args.force
    )
    logger.info(f"Generated {gen} scenarios for {args.workflow} ({err} errors)")


if __name__ == "__main__":
    main()
