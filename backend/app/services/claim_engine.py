import re
import json
from typing import List, Dict, Any
from app.schemas.schemas import AtomicClaimSchema
from app.services.llm_service import GroqLLMService

class ClaimEngine:
    @staticmethod
    def decompose_claim(claim_statement: str) -> List[AtomicClaimSchema]:
        """
        Decomposes any complex claim statement into atomic verifiable propositions.
        Calls Groq Cloud API LLM model for dynamic semantic decomposition.
        """
        atomic_claims: List[AtomicClaimSchema] = []

        system_prompt = """You are a senior forensic investigator. Decompose the user's claim statement into AT LEAST 3 to 4 distinct, atomic, independently verifiable sub-claims.
For example, for a claim like 'Company A delivered 10,000 devices to Hospital X before Sept 15', break it down into:
1. Entity/Contract proposition (Company A delivered to Hospital X).
2. Quantity/Specification proposition (Ordered/delivered quantity is 10,000 medical devices).
3. Temporal/Deadline proposition (Delivery completed before September 15).

Return ONLY valid JSON matching this exact schema:
{
  "atomic_claims": [
    {
      "statement": "atomic statement describing one proposition",
      "subject": "subject entity",
      "predicate": "action/relationship",
      "object": "target entity/value",
      "constraints": {"date": "...", "location": "...", "quantity": 10000},
      "verification_requirements": ["list of required evidence types"]
    }
  ]
}"""

        user_prompt = f"User Claim: \"{claim_statement}\""

        # 1. Real LLM Call to Groq Cloud API
        json_res = GroqLLMService.generate_json_output(system_prompt, user_prompt)
        if json_res and "atomic_claims" in json_res:
            for item in json_res["atomic_claims"]:
                try:
                    atomic_claims.append(AtomicClaimSchema(**item))
                except Exception:
                    pass
            if atomic_claims:
                return atomic_claims

        # 2. Dynamic Rule-Based Fallback Engine
        statement = claim_statement.strip()

        subj_match = re.search(r'^(.*?)\s+(delivered|shipped|supplied|completed|signed|attended|acquired|provided|produced)', statement, re.IGNORECASE)
        subject = subj_match.group(1).strip() if subj_match else "Primary Entity"

        qty_match = re.search(r'(\d+[\d,]*)\s+([a-zA-Z\s]+)', statement, re.IGNORECASE)
        quantity_str = qty_match.group(1).replace(",", "") if qty_match else None
        item_name = qty_match.group(2).strip() if qty_match else "units"
        try:
            quantity = int(quantity_str) if quantity_str else None
        except ValueError:
            quantity = None

        loc_match = re.search(r'(to|at|in)\s+([A-Z0-9][a-zA-Z0-9\s]+?)(?=\s+(before|after|by|on|\.|$))', statement, re.IGNORECASE)
        location = loc_match.group(2).strip() if loc_match else "Target Facility"

        date_match = re.search(r'(before|by|on|after)\s+([A-Za-z]+\s+\d{1,2}(?:\s*,\s*\d{4})?|\d{4}-\d{2}-\d{2})', statement, re.IGNORECASE)
        deadline = date_match.group(2).strip() if date_match else "Specified Deadline"

        atomic_claims.append(AtomicClaimSchema(
            statement=f"{subject} is the designated entity for this transaction",
            subject=subject,
            predicate="is_contracted_entity",
            object=item_name,
            constraints={},
            verification_requirements=["Contract / Purchase Order / Master Agreement"]
        ))

        if quantity:
            atomic_claims.append(AtomicClaimSchema(
                statement=f"Total ordered quantity requirement is {quantity:,} {item_name}",
                subject=subject,
                predicate="required_quantity",
                object=str(quantity),
                constraints={"quantity": quantity},
                verification_requirements=["Purchase Order", "Commercial Invoice"]
            ))

        if location and location != "Target Facility":
            atomic_claims.append(AtomicClaimSchema(
                statement=f"Fulfillment occurred at {location}",
                subject=subject,
                predicate="delivered_to",
                object=location,
                constraints={"location": location},
                verification_requirements=["Carrier Bill of Lading", "Delivery Receipt"]
            ))

        if quantity:
            atomic_claims.append(AtomicClaimSchema(
                statement=f"Total verified fulfilled balance equals {quantity:,} {item_name}",
                subject=subject,
                predicate="total_fulfilled_quantity",
                object=str(quantity),
                constraints={"quantity": quantity},
                verification_requirements=["Receiving Log", "Inventory Ledger"]
            ))

        if deadline and deadline != "Specified Deadline":
            atomic_claims.append(AtomicClaimSchema(
                statement=f"Full completion satisfied before {deadline}",
                subject=subject,
                predicate="completed_before_deadline",
                object=deadline,
                constraints={"date_deadline": deadline, "location": location},
                verification_requirements=["Receiving Timestamp Record", "Delivery Sign-off"]
            ))

        if len(atomic_claims) < 2:
            atomic_claims.append(AtomicClaimSchema(
                statement=statement,
                subject=subject,
                predicate="asserts_condition",
                object="Claim Statement",
                constraints={},
                verification_requirements=["Primary Evidence Document"]
            ))

        return atomic_claims
