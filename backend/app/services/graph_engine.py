import networkx as nx
from typing import List, Dict, Any

class GraphEngine:
    @staticmethod
    def build_evidence_graph(
        claim_statement: str,
        atomic_claims: List[Dict[str, Any]],
        sources: List[Dict[str, Any]],
        facts: List[Dict[str, Any]],
        entities: List[Dict[str, Any]],
        events: List[Dict[str, Any]],
        contradictions: List[Dict[str, Any]],
        evidence_gaps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Builds a NetworkX evidence graph connecting Claims, AtomicClaims, Sources, Facts, Entities, Events, Contradictions, and EvidenceGaps.
        Outputs node and edge structures tailored for React Flow.
        """
        G = nx.DiGraph()
        nodes = []
        edges = []

        # 1. Main Claim Node
        claim_node_id = "node_main_claim"
        nodes.append({
            "id": claim_node_id,
            "type": "claimNode",
            "position": {"x": 400, "y": 50},
            "data": {
                "label": "USER CLAIM",
                "title": claim_statement[:80] + ("..." if len(claim_statement) > 80 else ""),
                "full_text": claim_statement,
                "node_type": "CLAIM"
            }
        })

        # 2. Atomic Sub-Claim Nodes
        for idx, ac in enumerate(atomic_claims):
            ac_id = f"node_ac_{ac.get('id', idx)}"
            nodes.append({
                "id": ac_id,
                "type": "atomicClaimNode",
                "position": {"x": 100 + (idx * 260), "y": 180},
                "data": {
                    "label": f"SUBCLAIM #{idx+1}",
                    "statement": ac.get("statement"),
                    "status": ac.get("status", "UNVERIFIED"),
                    "confidence": ac.get("confidence", 0.0),
                    "node_type": "SUBCLAIM"
                }
            })
            edges.append({
                "id": f"edge_claim_{ac_id}",
                "source": claim_node_id,
                "target": ac_id,
                "label": "DECOMPOSED_INTO",
                "animated": True,
                "style": {"stroke": "#64748b"}
            })

        # 3. Source Nodes
        for idx, src in enumerate(sources):
            src_id = f"node_src_{src.get('id', idx)}"
            is_derived = src.get("source_type") in ["DERIVED", "COPIED"]
            nodes.append({
                "id": src_id,
                "type": "sourceNode",
                "position": {"x": 50 + (idx * 200), "y": 340},
                "data": {
                    "label": src.get("name"),
                    "file_type": src.get("file_type"),
                    "source_type": src.get("source_type", "PRIMARY"),
                    "node_type": "SOURCE"
                }
            })

        # 4. Fact Nodes & Links
        for idx, fact in enumerate(facts[:15]):  # Cap at top 15 facts for graph clarity
            fact_id = f"node_fact_{fact.get('id', idx)}"
            nodes.append({
                "id": fact_id,
                "type": "factNode",
                "position": {"x": 120 + (idx * 180), "y": 480},
                "data": {
                    "label": f"Fact #{idx+1}",
                    "value": fact.get("value"),
                    "source_span": fact.get("source_span"),
                    "node_type": "FACT"
                }
            })

        # 5. Contradiction Nodes
        for idx, c in enumerate(contradictions):
            c_id = f"node_contra_{c.get('id', idx)}"
            severity_color = "#ef4444" if c.get("severity") == "HIGH" else "#f59e0b"
            nodes.append({
                "id": c_id,
                "type": "contradictionNode",
                "position": {"x": 400 + (idx * 300), "y": 620},
                "data": {
                    "label": f"CONTRADICTION #{idx+1}",
                    "contradiction_type": c.get("contradiction_type"),
                    "statement_a": c.get("statement_a"),
                    "statement_b": c.get("statement_b"),
                    "status": c.get("status"),
                    "node_type": "CONTRADICTION"
                }
            })

        # 6. Evidence Gap Nodes
        for idx, gap in enumerate(evidence_gaps):
            gap_id = f"node_gap_{gap.get('id', idx)}"
            nodes.append({
                "id": gap_id,
                "type": "gapNode",
                "position": {"x": 150 + (idx * 350), "y": 740},
                "data": {
                    "label": f"EVIDENCE GAP #{idx+1}",
                    "description": gap.get("description"),
                    "why_it_matters": gap.get("why_it_matters"),
                    "next_best_evidence": gap.get("next_best_evidence"),
                    "node_type": "EVIDENCE_GAP"
                }
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges)
            }
        }
