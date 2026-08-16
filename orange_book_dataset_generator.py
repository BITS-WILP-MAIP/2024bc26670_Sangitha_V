import csv
import json
from pathlib import Path
from urllib.request import urlopen

API_URL = "https://api.fda.gov/drug/orangebook.json"
DATA_DIR = Path(__file__).resolve().parent / "data"

INTERACTION_RULES = [
    {
        "drug_a": "WARFARIN SODIUM",
        "drug_b": "ASPIRIN",
        "severity": "high",
        "explanation": "Both affect clotting. The combination increases bleeding risk.",
    },
    {
        "drug_a": "WARFARIN SODIUM",
        "drug_b": "IBUPROFEN",
        "severity": "high",
        "explanation": "NSAIDs can increase bleeding risk and change INR when combined with warfarin.",
    },
    {
        "drug_a": "LISINOPRIL",
        "drug_b": "IBUPROFEN",
        "severity": "moderate",
        "explanation": "NSAIDs may reduce blood pressure control and affect kidney function when taken with ACE inhibitors.",
    },
    {
        "drug_a": "AMLODIPINE",
        "drug_b": "ATORVASTATIN",
        "severity": "moderate",
        "explanation": "This combination can increase statin levels in the blood and may require dose review.",
    },
    {
        "drug_a": "ASPIRIN",
        "drug_b": "IBUPROFEN",
        "severity": "low",
        "explanation": "Regular concurrent use can reduce aspirin's cardiovascular protective effect and add GI irritation risk.",
    },
]


def fetch_orange_book_records():
    records = []
    limit = 1000

    # The OpenFDA Orange Book API has a hard pagination ceiling around skip=26000.
    # Fetch by approval-year windows and pre-1982 records to avoid the 400 error while
    # still capturing the full Orange Book dataset.
    years = list(range(1982, 2027))
    queries = []
    for year in years:
        start = f"{year}0101"
        end = f"{year}1231"
        queries.append(f"approval_date:[{start}+TO+{end}]")
    queries.append("approved_prior_to_1982:true")

    for query in queries:
        skip = 0
        while True:
            url = f"{API_URL}?search={query}&limit={limit}&skip={skip}"
            with urlopen(url, timeout=60) as response:
                payload = json.load(response)

            page = payload.get("results", [])
            if not page:
                break

            records.extend(page)
            if len(page) < limit:
                break

            skip += limit
            total = int(payload.get("meta", {}).get("results", {}).get("total", 0))
            if skip >= total:
                break

    return records


def normalize_ingredient_name(value):
    text = (value or "").strip()
    text = " ".join(text.split())
    return text.upper()


def write_drug_dataset(records):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    columns = [
        "ingredient",
        "brand_name",
        "application_number",
        "application_type",
        "product_number",
        "marketing_status",
        "dosage_form",
        "route",
        "approval_date",
        "reference_listed_drug",
        "reference_standard",
        "therapeutic_equivalence_codes",
        "applicant_name",
        "applicant_full_name",
    ]

    seen = set()
    rows = []
    for item in records:
        record_product_number = item.get("product_number", "")
        record_application_number = item.get("application_number", "")
        record_application_type = item.get("application_type", "")
        record_approval_date = item.get("approval_date", "")

        for product in item.get("products", []):
            product_number = product.get("product_number") or record_product_number
            application_number = product.get("application_number") or record_application_number
            application_type = product.get("application_type") or record_application_type
            approval_date = item.get("approval_date", "") or record_approval_date
            brand_name = (product.get("brand_name") or "").strip()
            applicant_name = (product.get("application_name") or "").strip()
            applicant_full_name = (product.get("application_full_name") or "").strip()
            marketing_status = (product.get("marketing_status") or "").strip()
            dosage_form = (product.get("dosage_form") or "").strip()
            route = (product.get("route") or "").strip()
            rld = bool(product.get("reference_listed_drug"))
            rs = bool(product.get("reference_standard"))
            te_codes = ";".join(product.get("therapeutic_equivalence_codes", []) or [])

            for ingredient_data in product.get("active_ingredients", []):
                ingredient = normalize_ingredient_name(ingredient_data.get("name"))
                strength = (ingredient_data.get("strength") or "").strip()
                key = (
                    ingredient,
                    brand_name,
                    application_number,
                    application_type,
                    product_number,
                    dosage_form,
                    route,
                    strength,
                )
                if not ingredient or key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "ingredient": ingredient,
                        "brand_name": brand_name,
                        "application_number": application_number,
                        "application_type": application_type,
                        "product_number": product_number,
                        "marketing_status": marketing_status,
                        "dosage_form": dosage_form,
                        "route": route,
                        "approval_date": approval_date,
                        "reference_listed_drug": str(rld).lower(),
                        "reference_standard": str(rs).lower(),
                        "therapeutic_equivalence_codes": te_codes,
                        "applicant_name": applicant_name,
                        "applicant_full_name": applicant_full_name,
                    }
                )

    rows.sort(key=lambda r: (r["ingredient"], r["brand_name"], r["application_number"]))
    out_path = DATA_DIR / "orange_book_drugs.csv"
    with out_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} Orange Book drug records to {out_path}")


def write_interaction_dataset():
    rows = []
    for rule in INTERACTION_RULES:
        rows.append(
            {
                "drug_a": normalize_ingredient_name(rule["drug_a"]),
                "drug_b": normalize_ingredient_name(rule["drug_b"]),
                "severity": rule["severity"],
                "explanation": rule["explanation"],
            }
        )

    out_path = DATA_DIR / "orange_book_interactions.csv"
    with out_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["drug_a", "drug_b", "severity", "explanation"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} interaction records to {out_path}")


if __name__ == "__main__":
    records = fetch_orange_book_records()
    write_drug_dataset(records)
    write_interaction_dataset()
