"""Generate 50 synthetic MSX account fixtures for the ClawPilot study.

Distribution: 10 clean, 15 stale, 10 missing, 10 inconsistent, 5 contradictory.
"""
import json
import random
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = REPO_ROOT / "fixtures"
FIXTURES_DIR.mkdir(exist_ok=True)

# Seed for reproducibility
random.seed(42)

# === Company data pools ===
COMPANIES = [
    ("Contoso Ltd", "Technology", 320),
    ("Fabrikam Inc", "Manufacturing", 580),
    ("Northwind Traders", "Retail", 210),
    ("Adventure Works", "Outdoor Recreation", 450),
    ("Tailspin Toys", "Consumer Goods", 180),
    ("Woodgrove Bank", "Financial Services", 1200),
    ("Litware Inc", "Software", 95),
    ("Proseware Inc", "Software", 270),
    ("VanArsdel Ltd", "Electronics", 640),
    ("Trey Research", "Biotech", 380),
    ("Alpine Ski House", "Hospitality", 150),
    ("Bellows College", "Education", 2100),
    ("Coho Winery", "Food & Beverage", 120),
    ("Datum Corporation", "Data Services", 890),
    ("Fourth Coffee", "Food & Beverage", 85),
    ("Graphic Design Institute", "Education", 340),
    ("Humongous Insurance", "Insurance", 4200),
    ("Lamna Healthcare", "Healthcare", 1500),
    ("Lucerne Publishing", "Media", 220),
    ("Margie's Travel", "Travel", 165),
    ("Nod Publishers", "Media", 95),
    ("Relecloud", "Technology", 410),
    ("Wide World Importers", "Import/Export", 780),
    ("Wingtip Toys", "Consumer Goods", 290),
    ("Adatum Corporation", "Technology", 560),
    ("A. Datum", "Analytics", 180),
    ("Blue Yonder Airlines", "Aviation", 3200),
    ("City Power & Light", "Utilities", 1800),
    ("Consolidated Messenger", "Logistics", 650),
    ("First Up Consultants", "Consulting", 130),
    ("Liberty's Delightful Sinful Bakery", "Food & Beverage", 45),
    ("Munson's Pickles", "Food & Beverage", 38),
    ("Parnell Aerospace", "Aerospace", 2800),
    ("Southridge Video", "Entertainment", 420),
    ("Treyarch Global", "Defense", 5400),
    ("Vineyard Bank", "Financial Services", 980),
    ("Woodgrove Labs", "Pharmaceuticals", 1100),
    ("Contoso Suites", "Hospitality", 250),
    ("Fabrikam Residences", "Real Estate", 190),
    ("Prism Media Group", "Media", 340),
    ("Quantum Analytics", "Technology", 160),
    ("Sunrise Healthcare", "Healthcare", 720),
    ("Pacific Northwest Outfitters", "Retail", 280),
    ("Redmond Instruments", "Medical Devices", 490),
    ("Azure Ridge Partners", "Investment", 85),
    ("Cascadia Systems", "Technology", 310),
    ("Evergreen Solutions", "Environmental", 140),
    ("Summit Financial", "Financial Services", 620),
    ("Iron Creek Mining", "Mining", 1900),
    ("Meridian Software", "Software", 230),
]

OWNERS = [
    "Marcus Williams", "Lisa Patel", "Ahmed Hassan", "Sarah Kim",
    "Raj Mehta", "Jennifer Walsh", "David Chen", "Priya Sharma",
    "Tom Rodriguez", "Michelle Park",
]

FIRST_NAMES = [
    "James", "Patricia", "Robert", "Sarah", "Michael", "Angela",
    "David", "Jennifer", "William", "Maria", "Thomas", "Rachel",
    "Kevin", "Diana", "Brian", "Karen", "Steven", "Laura",
    "Daniel", "Sandra", "Andrew", "Michelle", "Christopher", "Tamara",
    "Jason", "Nicole", "Eric", "Samantha", "Ryan", "Victoria",
]

LAST_NAMES = [
    "Park", "Chen", "Morrison", "Torres", "Yamamoto", "Kowalski",
    "Singh", "O'Brien", "Nakamura", "Petrov", "Kim", "Doyle",
    "Martinez", "Schmidt", "Okafor", "Thompson", "Rivera", "Berg",
    "Patel", "Hansen", "Lee", "Foster", "Nguyen", "Anderson",
    "Wilson", "Brown", "Taylor", "Davis", "Jackson", "White",
]

TITLES = [
    "CTO", "CIO", "VP Engineering", "IT Director", "Cloud Architect",
    "Infrastructure Manager", "DevOps Lead", "Security Manager",
    "CFO", "COO", "Head of Digital", "Data Platform Lead",
    "Director of IT", "VP Operations", "Technology Manager",
]

ROLES = ["Technical", "Business", "Executive", "Operations", "Finance"]

OPPORTUNITY_TYPES = [
    "Azure Infrastructure", "M365 E5 Upsell", "Security Modernization",
    "Data Platform Migration", "Azure SQL Migration", "AKS Deployment",
    "Dynamics 365 Implementation", "Power Platform", "Azure AI Services",
    "Cloud Migration Phase", "Azure DevOps", "Copilot Adoption",
    "Azure Arc Deployment", "Azure Virtual Desktop", "Intune Rollout",
]

RECOMMENDATION_TYPES = ["SPA", "CxObserve", "Advisor", "Manual"]
RECOMMENDATION_DESCS = [
    "Enable Azure Security Center standard tier",
    "Rightsize underutilized VMs (potential 23% savings)",
    "Migrate to Azure SQL Managed Instance",
    "Enable MFA for all admin accounts",
    "Adopt Azure Policy for compliance governance",
    "Consider Reserved Instances for stable workloads",
    "Enable Azure Monitor for production workloads",
    "Review network security group rules",
    "Upgrade to premium tier storage for production",
    "Enable Azure Backup for critical databases",
    "Migrate legacy .NET apps to Azure App Service",
    "Enable Defender for Cloud across subscriptions",
    "Implement Azure Landing Zones",
    "Deploy Azure Front Door for global load balancing",
    "Enable diagnostic logging for all services",
]

ACTIVITY_DESCS = {
    "meeting": [
        "QBR with customer IT team",
        "Architecture review session",
        "Executive business review",
        "Technical deep-dive on migration",
        "Partner introduction meeting",
        "Weekly sync with account team",
        "Security posture review",
    ],
    "email": [
        "Sent follow-up on migration timeline",
        "Received pricing inquiry from CFO",
        "Shared architecture documentation",
        "Customer requested partner introduction",
        "Sent renewal reminder to procurement",
        "Follow-up on support ticket resolution",
    ],
    "call": [
        "Quick call on deployment blocker",
        "Check-in on pilot progress",
        "Discussed budget approval timeline",
        "Escalation triage call",
    ],
    "msx_update": [
        "Updated opportunity stage to Develop",
        "Added new milestone: Technical Validation",
        "Updated close date based on customer feedback",
        "Added competitive intelligence notes",
    ],
    "spa_received": [
        "SPA: VM rightsizing opportunity detected",
        "SPA: Security recommendation - MFA gaps",
        "SPA: Cost anomaly detected",
    ],
    "escalation": [
        "Customer escalated support ticket response time",
        "Performance degradation reported by end users",
    ],
    "contract_event": [
        "Contract renewal notification (90 days)",
        "MACC milestone approaching",
        "Billing discrepancy flagged",
    ],
    "deployment": [
        "Production deployment completed successfully",
        "Pilot environment provisioned",
        "Migration batch 1 completed",
    ],
}


def gen_id(prefix: str, idx: int, width: int = 8) -> str:
    """Generate a deterministic ID like ACC-A1B2C3D4."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random.seed(hash((prefix, idx)) & 0xFFFFFFFF)
    suffix = "".join(random.choice(chars) for _ in range(width))
    random.seed(42 + idx)  # Reset to fixture-level seed
    return f"{prefix}-{suffix}"


def generate_acr_trend(base_value: float, fixture_class: str, fixture_idx: int) -> dict:
    """Generate 12-month ACR trend based on fixture class."""
    months = [f"2023-{m:02d}" for m in range(4, 13)] + [f"2024-{m:02d}" for m in range(1, 4)]
    values = []

    if fixture_class == "clean":
        # Steady or growing
        for i in range(12):
            growth = random.uniform(0.98, 1.04)
            base_value *= growth
            values.append(round(base_value, 2))
    elif fixture_class == "stale":
        # Data stops changing after month 6-8
        stale_point = random.randint(6, 8)
        for i in range(12):
            if i < stale_point:
                growth = random.uniform(0.97, 1.03)
                base_value *= growth
            values.append(round(base_value, 2))
    elif fixture_class == "missing":
        # Some months have 0 (data gaps)
        missing_months = random.sample(range(12), k=random.randint(2, 4))
        for i in range(12):
            if i in missing_months:
                values.append(0)
            else:
                growth = random.uniform(0.96, 1.05)
                base_value *= growth
                values.append(round(base_value, 2))
    elif fixture_class == "inconsistent":
        # Irregular jumps that don't make business sense
        for i in range(12):
            if random.random() < 0.25:
                spike = random.choice([0.5, 2.0, 0.3, 1.8])
                values.append(round(base_value * spike, 2))
            else:
                growth = random.uniform(0.95, 1.05)
                base_value *= growth
                values.append(round(base_value, 2))
    else:  # contradictory
        # Declining but health says "Healthy"
        for i in range(12):
            decline = random.uniform(0.88, 0.97)
            base_value *= decline
            values.append(round(base_value, 2))

    workloads = ["compute", "storage", "networking", "paas"]
    monthly_values = []
    for i, month in enumerate(months):
        entry = {"month": month, "value_usd": values[i]}
        if values[i] > 0:
            # Generate workload breakdown
            remaining = values[i]
            breakdown = {}
            for j, wl in enumerate(workloads):
                if j == len(workloads) - 1:
                    breakdown[wl] = round(remaining, 2)
                else:
                    share = random.uniform(0.15, 0.45) * remaining
                    breakdown[wl] = round(share, 2)
                    remaining -= share
            entry["workload_breakdown"] = breakdown
        monthly_values.append(entry)

    return {"currency": "USD", "monthly_values": monthly_values}


def generate_contacts(company_name: str, fixture_class: str, count: int) -> list:
    """Generate contact list."""
    contacts = []
    influence_levels = ["Decision Maker", "Influencer", "Champion", "End User", "Blocker"]
    domain = company_name.lower().replace(" ", "").replace("'", "").replace(".", "")[:12] + ".com"

    used_names = set()
    for i in range(count):
        # Ensure unique name
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            full = f"{first} {last}"
            if full not in used_names:
                used_names.add(full)
                break

        contact_id = gen_id("CON", hash((company_name, i)) & 0xFFFF)
        title = random.choice(TITLES) if i < 5 else random.choice(TITLES[5:])
        influence = influence_levels[min(i, 4)] if i < 5 else random.choice(influence_levels[2:])

        # Last interaction date
        if fixture_class == "stale" and i > 2:
            last_int = f"2023-{random.randint(1, 6):02d}-{random.randint(1, 28):02d}"
        elif fixture_class == "missing" and random.random() < 0.3:
            last_int = None
        else:
            last_int = f"2024-{random.randint(1, 3):02d}-{random.randint(1, 28):02d}"

        contact = {
            "contact_id": contact_id,
            "name": full,
            "role": random.choice(ROLES),
            "title": title,
            "email": f"{first.lower()}.{last.lower()}@{domain}",
            "influence_level": influence,
            "last_interaction": last_int,
            "is_current": not (fixture_class == "stale" and i > 3),
        }
        contacts.append(contact)

    return contacts


def generate_opportunities(fixture_class: str, owner: str, idx: int) -> list:
    """Generate 1-5 opportunities."""
    count = random.randint(1, min(4, 5))
    stages = ["Prospect", "Qualify", "Develop", "Propose", "Close"]
    bpf_stages = ["Qualify", "Develop", "Propose", "Close"]
    forecast_cats = ["Pipeline", "Best Case", "Committed", "Omitted"]
    opps = []

    for i in range(count):
        opp_id = gen_id("OPP", hash((idx, i)) & 0xFFFF)
        stage_idx = random.randint(0, 4)
        stage = stages[stage_idx]

        # BPF stage logic varies by fixture class
        if fixture_class == "inconsistent" and i == 0:
            # BPF doesn't match stage (intentional inconsistency)
            bpf = random.choice([s for s in bpf_stages if s != stage]) if stage in bpf_stages else "Qualify"
        elif fixture_class == "missing" and random.random() < 0.3:
            bpf = None
        elif stage == "Prospect":
            bpf = None
        else:
            bpf = stage if stage in bpf_stages else "Qualify"

        # Close date
        if fixture_class == "stale" and i == 0:
            close_date = f"2023-{random.randint(9, 12):02d}-{random.randint(1, 28):02d}"
        elif fixture_class == "inconsistent" and i == 0 and stage == "Close":
            close_date = f"2024-{random.randint(7, 12):02d}-{random.randint(1, 28):02d}"
        else:
            close_date = f"2024-{random.randint(4, 12):02d}-{random.randint(1, 28):02d}"

        # Last updated
        if fixture_class == "stale":
            last_updated = f"2023-{random.randint(6, 10):02d}-{random.randint(1, 28):02d}T{random.randint(8, 17):02d}:00:00-05:00"
        elif fixture_class == "missing" and random.random() < 0.3:
            last_updated = None
        else:
            last_updated = f"2024-{random.randint(1, 3):02d}-{random.randint(1, 28):02d}T{random.randint(8, 17):02d}:00:00-05:00"

        value = random.choice([45000, 68000, 89000, 125000, 175000, 210000, 280000, 350000, 450000, 560000])

        # Forecast category
        if stage in ("Won", "Lost"):
            fc = "Omitted"
        elif stage == "Close":
            fc = "Committed"
        elif stage in ("Develop", "Propose"):
            fc = random.choice(["Best Case", "Pipeline"])
        else:
            fc = "Pipeline"

        # Contradictory: committed but stage is Qualify
        if fixture_class == "contradictory" and i == 0:
            stage = "Qualify"
            fc = "Committed"
            bpf = "Qualify"

        # Milestones
        milestones = []
        ms_names = ["Discovery", "Technical Validation", "Business Case Approved", "Security Review", "Executive Sponsor Identified"]
        ms_count = random.randint(1, 3)
        for mi in range(ms_count):
            ms_id = gen_id("MS", hash((idx, i, mi)) & 0xFFFF)
            ms_status_options = ["Not Started", "In Progress", "Completed", "Blocked"]
            ms_status = ms_status_options[min(mi, 2)] if fixture_class == "clean" else random.choice(ms_status_options)

            ms = {
                "milestone_id": ms_id,
                "name": ms_names[mi],
                "status": ms_status,
                "due_date": f"2024-{random.randint(3, 8):02d}-{random.randint(1, 28):02d}",
                "completed_date": f"2024-{random.randint(1, 3):02d}-{random.randint(1, 28):02d}" if ms_status == "Completed" else None,
                "owner": owner,
                "evidence": f"email_thread_{random.randint(1000, 9999)}" if ms_status == "Completed" else "",
            }
            milestones.append(ms)

        opp = {
            "opportunity_id": opp_id,
            "name": f"{COMPANIES[idx % len(COMPANIES)][0].split()[0]} {random.choice(OPPORTUNITY_TYPES)}",
            "stage": stage,
            "estimated_value_usd": value,
            "close_date": close_date,
            "bpf_stage": bpf,
            "forecast_category": fc,
            "owner": owner,
            "last_updated": last_updated,
            "milestones": milestones,
        }
        opps.append(opp)

    return opps


def generate_recommendations(fixture_class: str) -> list:
    """Generate 0-8 open recommendations."""
    if fixture_class == "clean":
        count = random.randint(1, 3)
    elif fixture_class == "stale":
        count = random.randint(3, 6)
    elif fixture_class == "missing":
        count = random.randint(0, 2)
    else:
        count = random.randint(2, 5)

    recs = []
    used_descs = set()
    for i in range(count):
        while True:
            desc = random.choice(RECOMMENDATION_DESCS)
            if desc not in used_descs:
                used_descs.add(desc)
                break

        rec_type = random.choice(RECOMMENDATION_TYPES)
        priority = random.choice(["High", "Medium", "Low"])
        status = random.choice(["New", "Acknowledged", "In Progress", "Dismissed"])

        if fixture_class == "stale":
            created = f"2023-{random.randint(3, 8):02d}-{random.randint(1, 28):02d}T10:00:00-05:00"
        else:
            created = f"2024-{random.randint(1, 3):02d}-{random.randint(1, 28):02d}T10:00:00-05:00"

        recs.append({
            "recommendation_id": f"REC-{random.randint(10000, 99999)}",
            "type": rec_type,
            "description": desc,
            "priority": priority,
            "created_at": created,
            "status": status,
        })

    return recs


def generate_activity_timeline(fixture_class: str) -> list:
    """Generate recent activity timeline."""
    if fixture_class == "clean":
        count = random.randint(8, 15)
    elif fixture_class == "stale":
        count = random.randint(2, 5)
    elif fixture_class == "missing":
        count = random.randint(3, 6)
    else:
        count = random.randint(5, 12)

    activities = []
    activity_types = list(ACTIVITY_DESCS.keys())

    for i in range(count):
        atype = random.choice(activity_types)
        desc = random.choice(ACTIVITY_DESCS[atype])

        if fixture_class == "stale":
            date = f"2023-{random.randint(6, 12):02d}-{random.randint(1, 28):02d}"
        else:
            month = random.randint(1, 3)
            date = f"2024-{month:02d}-{random.randint(1, 28):02d}"

        activity = {
            "date": date,
            "activity_type": atype,
            "description": desc,
            "participants": random.sample(OWNERS[:5], k=random.randint(1, 3)),
        }
        activities.append(activity)

    # Sort by date descending
    activities.sort(key=lambda x: x["date"], reverse=True)
    return activities


def generate_health_flags(fixture_class: str, acr_values: list) -> dict:
    """Generate customer health flags."""
    # Determine actual trend from ACR
    non_zero = [v for v in acr_values if v > 0]
    if len(non_zero) >= 3:
        recent_avg = sum(non_zero[-3:]) / 3
        earlier_avg = sum(non_zero[:3]) / 3
        actual_trend = "Growing" if recent_avg > earlier_avg * 1.05 else (
            "Declining" if recent_avg < earlier_avg * 0.95 else "Stable"
        )
    else:
        actual_trend = "Unknown"

    if fixture_class == "contradictory":
        # Health says opposite of reality
        health = "Healthy"
        consumption = "Growing" if actual_trend == "Declining" else "Declining"
        renewal_risk = "Low"
    elif fixture_class == "clean":
        health = "Healthy" if actual_trend in ("Growing", "Stable") else "At Risk"
        consumption = actual_trend
        renewal_risk = "Low" if actual_trend == "Growing" else "Medium"
    elif fixture_class == "stale":
        health = random.choice(["Healthy", "At Risk"])
        consumption = random.choice(["Growing", "Stable", "Declining"])
        renewal_risk = random.choice(["Low", "Medium", "High"])
    else:
        health = random.choice(["Healthy", "At Risk", "Critical", "Unknown"])
        consumption = actual_trend if random.random() > 0.3 else random.choice(["Growing", "Stable", "Declining", "Volatile"])
        renewal_risk = random.choice(["Low", "Medium", "High", "Unknown"])

    if fixture_class == "stale":
        last_assessed = f"2023-{random.randint(4, 9):02d}-{random.randint(1, 28):02d}"
    elif fixture_class == "missing":
        last_assessed = None
    else:
        last_assessed = f"2024-{random.randint(1, 3):02d}-{random.randint(1, 28):02d}"

    return {
        "overall_health": health,
        "engagement_score": random.randint(20, 95),
        "consumption_trend": consumption,
        "renewal_risk": renewal_risk,
        "last_assessed": last_assessed,
    }


def generate_contract(fixture_class: str) -> dict:
    """Generate contract/billing info."""
    sub_types = ["CSP", "MCA", "EA", "PAYG"]
    sub_type = random.choice(sub_types)

    if sub_type == "PAYG":
        contract_end = None
        macc_commitment = None
        macc_consumed = None
        billing = "Monthly"
        auto_renew = False
    elif sub_type == "EA":
        contract_end = f"2024-{random.randint(6, 12):02d}-{random.randint(1, 28):02d}"
        macc_commitment = random.choice([500000, 750000, 1000000, 1500000, 2000000])
        macc_consumed = round(macc_commitment * random.uniform(0.3, 0.85), 2)
        billing = "Annual"
        auto_renew = random.choice([True, False])
    else:
        contract_end = f"2024-{random.randint(4, 12):02d}-{random.randint(1, 28):02d}"
        macc_commitment = random.choice([None, 200000, 350000, 500000])
        macc_consumed = round(macc_commitment * random.uniform(0.2, 0.7), 2) if macc_commitment else None
        billing = random.choice(["Monthly", "Annual"])
        auto_renew = random.choice([True, False])

    if fixture_class == "missing" and random.random() < 0.4:
        contract_end = None
        macc_commitment = None
        macc_consumed = None

    return {
        "subscription_type": sub_type,
        "contract_end_date": contract_end,
        "macc_commitment_usd": macc_commitment,
        "macc_consumed_usd": macc_consumed,
        "billing_frequency": billing,
        "auto_renew": auto_renew,
    }


def generate_fixture(idx: int, fixture_class: str) -> dict:
    """Generate a single fixture."""
    random.seed(42 + idx * 7)  # Deterministic per fixture

    company_name, industry, emp_count = COMPANIES[idx % len(COMPANIES)]
    owner = OWNERS[idx % len(OWNERS)]
    segment = random.choice(["smb-small", "smb-mid", "smb-corporate"])
    geography = random.choice(["NA", "EMEA", "APAC", "LATAM"])
    tenure = round(random.uniform(0.5, 8.0), 1)

    account_id = gen_id("ACC", idx)
    base_acr = random.uniform(5000, 120000)

    acr = generate_acr_trend(base_acr, fixture_class, idx)
    acr_values = [m["value_usd"] for m in acr["monthly_values"]]

    contact_count = random.randint(5, 12)
    contacts = generate_contacts(company_name, fixture_class, contact_count)
    opportunities = generate_opportunities(fixture_class, owner, idx)
    recommendations = generate_recommendations(fixture_class)
    timeline = generate_activity_timeline(fixture_class)
    health = generate_health_flags(fixture_class, acr_values)
    contract = generate_contract(fixture_class)

    return {
        "fixture_id": f"FX-{idx + 1:03d}",
        "fixture_class": fixture_class,
        "authored_at": "2024-03-15T10:00:00-05:00",
        "account": {
            "account_id": account_id,
            "name": company_name,
            "segment": segment,
            "geography": geography,
            "tenure_years": tenure,
            "owner": owner,
            "industry": industry,
            "employee_count": emp_count,
        },
        "opportunities": opportunities,
        "contacts": contacts,
        "acr_trend": acr,
        "open_recommendations": recommendations,
        "recent_activity_timeline": timeline,
        "customer_health_flags": health,
        "contract_billing": contract,
    }


def main():
    # Distribution: 10 clean, 15 stale, 10 missing, 10 inconsistent, 5 contradictory
    classes = (
        ["clean"] * 10
        + ["stale"] * 15
        + ["missing"] * 10
        + ["inconsistent"] * 10
        + ["contradictory"] * 5
    )

    fixtures = []
    for idx, fixture_class in enumerate(classes):
        fixture = generate_fixture(idx, fixture_class)
        fixtures.append(fixture)

        # Write individual file
        path = FIXTURES_DIR / f"{fixture['fixture_id']}.json"
        with open(path, "w") as f:
            json.dump(fixture, f, indent=2, sort_keys=False)

    # Write combined manifest
    manifest = {
        "total": len(fixtures),
        "distribution": {
            "clean": 10,
            "stale": 15,
            "missing": 10,
            "inconsistent": 10,
            "contradictory": 5,
        },
        "fixture_ids": [fx["fixture_id"] for fx in fixtures],
    }
    with open(FIXTURES_DIR / "_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(fixtures)} fixtures in {FIXTURES_DIR}")
    print(f"Distribution: {manifest['distribution']}")


if __name__ == "__main__":
    main()
