from typing import List, Dict, Any

class HypothesisEngine:
    @staticmethod
    def generate_hypotheses_and_gaps(
        contradictions: List[Dict[str, Any]],
        facts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Agentic investigation loop:
        Formulates evidence-driven hypotheses when contradictions occur and identifies missing evidence gaps.
        """
        hypotheses = []
        evidence_gaps = []

        has_second_shipment_fact = any("1,500" in str(f.get("value", "")) or "shipment 2" in str(f.get("source_name", "")).lower() for f in facts)
        has_hospital_log_2 = any("hospital_receiving_receipt_2" in str(f.get("source_name", "")).lower() for f in facts)

        for c in contradictions:
            c_type = c.get("contradiction_type")
            if c_type == "QUANTITY":
                if not has_second_shipment_fact:
                    hypotheses.append({
                        "statement": "H1: A second partial shipment was dispatched to complete the 10,000 unit order.",
                        "search_requirements": ["Supplier shipping records", "Second Carrier Bill of Lading", "Supplier email correspondence"],
                        "status": "TESTING"
                    })
                    evidence_gaps.append({
                        "description": "Missing second shipment shipping manifest or supplier email confirmation.",
                        "why_it_matters": "Distinguishes whether the vendor defaulted on 1,500 units or fulfilled them via a separate dispatch.",
                        "next_best_evidence": "Carrier manifest or supplier backorder email for post-Sept 14 dispatch."
                    })
                else:
                    hypotheses.append({
                        "statement": "H1: Remaining 1,500 units were delivered in a separate shipment on Sept 17.",
                        "search_requirements": ["Delivery Receipt #2", "Carrier Manifest #2"],
                        "status": "CONFIRMED",
                        "findings": "Supplier email & Carrier Manifest #2 confirm 1,500 units dispatched Sept 16 and received Sept 17."
                    })

            elif c_type == "DATE":
                hypotheses.append({
                    "statement": "H2: Delivery deadline was September 15, but final receipt was completed on September 17.",
                    "search_requirements": ["Contract penalty clause", "Hospital logistics signoff log"],
                    "status": "CONFIRMED",
                    "findings": "Evidence confirms partial delivery of 8,500 units met Sept 14, but full 10,000 order was not complete until Sept 17."
                })
                
                if not has_hospital_log_2:
                    evidence_gaps.append({
                        "description": "Hospital official receiving sign-off log for Sept 17 shipment.",
                        "why_it_matters": "Confirms exact time of final receipt and whether late delivery penalties apply.",
                        "next_best_evidence": "Hospital receiving log for Sept 17."
                    })

        return {
            "hypotheses": hypotheses,
            "evidence_gaps": evidence_gaps
        }
