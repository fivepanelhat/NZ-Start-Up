"""
Paid pilot offer pack - commercial artefacts for founders/EDAs.

Drafts only. Not legal advice. Human sends and signs.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists
from nz_startup.paths import company_dir, templates_dir


def build_pilot_offer(
 company_id: str,
 *,
 customer_name: str,
 pilot_fee_nzd: str = "1500",
 term_days: int = 90,
 success_criteria: str = "",
 conversion_price_nzd: str = "799-999/mo or enterprise quote",
 scope: str = "Sovereign AI pilot - local-first demo + weekly operating cadence",
 champion: str = "",
 start_date: str | None = None,
) -> dict[str, Any]:
 if not customer_name.strip():
 raise ValueError("customer_name is required")
 start = start_date or date.today().isoformat()
 try:
 end = (date.fromisoformat(start) + timedelta(days=int(term_days))).isoformat()
 except ValueError as e:
 raise ValueError("start_date must be YYYY-MM-DD") from e

 criteria = success_criteria.strip() or (
 "Named champion engaged weekly; pilot scope delivered offline-capable; "
 "written go/no-go on conversion pricing path"
 )

 offer = {
 "status": "DRAFT_NOT_SENT",
 "not_legal_advice": True,
 "company_id": company_id,
 "customer_name": customer_name.strip(),
 "champion": champion.strip(),
 "scope": scope.strip(),
 "pilot_fee_nzd": pilot_fee_nzd.strip(),
 "term_days": int(term_days),
 "start_date": start,
 "end_date": end,
 "success_criteria": criteria,
 "conversion_price_nzd": conversion_price_nzd.strip(),
 "payment_terms": "Invoiced on signature; paid pilot preferred (free pilots don't convert)",
 "data_residency": "Local-first / customer-controlled by default; no silent offshore export",
 "hitl": "Human sends offer and signs. Agent prepares drafts only.",
 "generated_on": date.today().isoformat(),
 }
 return offer


def write_pilot_pack(company_id: str, offer: dict[str, Any]) -> dict[str, Path]:
 company = ensure_exists(company_id)
 out = company / "commercial" / "pilots"
 out.mkdir(parents=True, exist_ok=True)
 safe = "".join(
 c if c.isalnum() or c in "-_" else "-" for c in offer["customer_name"]
 )[:40]
 stem = f"pilot-{safe}-{offer['start_date']}"

 md = format_offer_markdown(offer)
 md_path = out / f"{stem}.md"
 json_path = out / f"{stem}.json"
 md_path.write_text(md, encoding="utf-8", newline="\n")
 json_path.write_text(json.dumps(offer, indent=2) + "\n", encoding="utf-8")

 # Agreement outline filled lightly
 outline_src = templates_dir() / "pilot-agreement-outline.md"
 outline = (
 outline_src.read_text(encoding="utf-8")
 if outline_src.is_file()
 else "# Pilot Agreement Outline - DRAFT - NOT LEGAL ADVICE\n"
 )
 filled = (
 f"# Pilot agreement working copy - DRAFT - NOT LEGAL ADVICE\n\n"
 f"- Supplier company memory: `{company_id}`\n"
 f"- Customer: {offer['customer_name']}\n"
 f"- Champion: {offer.get('champion') or 'TBD'}\n"
 f"- Term: {offer['term_days']} days ({offer['start_date']} -> {offer['end_date']})\n"
 f"- Fees: NZ${offer['pilot_fee_nzd']} (paid pilot)\n"
 f"- Success criteria: {offer['success_criteria']}\n"
 f"- Conversion path: {offer['conversion_price_nzd']}\n\n"
 "---\n\n"
 + outline
 + "\n\n**Human must have NZ lawyer review before signature.**\n"
 )
 agr_path = out / f"{stem}-agreement-outline.md"
 agr_path.write_text(filled, encoding="utf-8", newline="\n")

 # Zip pack
 zip_path = out / f"{stem}-pack.zip"
 latest = out / "pilot-offer-latest.zip"
 with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
 zf.writestr("PILOT_OFFER.md", md)
 zf.writestr("offer.json", json.dumps(offer, indent=2) + "\n")
 zf.writestr("agreement-outline.md", filled)
 zf.writestr(
 "README.md",
 (
 "# Pilot offer pack\n\n"
 "DRAFT_NOT_SENT - human emails/sends and signs.\n"
 "Not legal advice.\n"
 ),
 )
 latest.write_bytes(zip_path.read_bytes())

 append_audit(
 company,
 actor="agent:gtm-pipeline-rep",
 skill="gtm-pipeline-rep",
 action="pilot_offer_prepare",
 summary=f"Pilot offer for {offer['customer_name']} fee={offer['pilot_fee_nzd']}",
 artefact_ref=str(md_path.relative_to(company)).replace("\\", "/"),
 tier="gold",
 hitl_required=True,
 hitl_status="pending",
 risk_level="medium",
 )
 return {
 "markdown": md_path,
 "json": json_path,
 "agreement_outline": agr_path,
 "zip": zip_path,
 "latest": latest,
 }


def format_offer_markdown(offer: dict[str, Any]) -> str:
 return f"""# Pilot offer - {offer['customer_name']}

**DRAFT_NOT_SENT** | **NOT LEGAL ADVICE** | Prepared for human send/signature only

## Parties
- Supplier (your company memory): `{offer['company_id']}`
- Customer: {offer['customer_name']}
- Customer champion: {offer.get('champion') or '_TBD_'}

## Scope
{offer['scope']}

## Commercials
| Item | Value |
|------|-------|
| Pilot fee (NZD) | {offer['pilot_fee_nzd']} |
| Term | {offer['term_days']} days |
| Start | {offer['start_date']} |
| End | {offer['end_date']} |
| Payment | {offer['payment_terms']} |
| Conversion path | {offer['conversion_price_nzd']} |

## Success criteria
{offer['success_criteria']}

## Data & sovereignty
{offer['data_residency']}

## What we will not do in the pilot
- Autonomous cold email / unsolicited bulk messages
- File IRD/Companies Office on your behalf
- Move money or act as tax agent
- Present drafts as legal or financial advice

## Next human steps
- [ ] Confirm fee and success criteria with customer champion
- [ ] Lawyer review of agreement outline
- [ ] Human sends offer from own email
- [ ] On signature: schedule weekly board cadence

---
{offer['hitl']}
Generated: {offer['generated_on']}
"""


def prepare_and_write(
 company_id: str,
 *,
 customer_name: str,
 **kwargs: Any,
) -> tuple[dict[str, Any], dict[str, Path]]:
 offer = build_pilot_offer(company_id, customer_name=customer_name, **kwargs)
 paths = write_pilot_pack(company_id, offer)
 return offer, paths
