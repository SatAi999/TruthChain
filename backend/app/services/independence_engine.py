from typing import List, Dict, Any

class SourceIndependenceEngine:
    @staticmethod
    def analyze_lineage(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Filters duplicate/derived sources to ensure multi-counting does not occur.
        Returns independent source groups and derived source counts.
        """
        primary_sources = []
        derived_sources = []

        for src in sources:
            stype = src.get("source_type", "PRIMARY")
            if stype == "DERIVED" or stype == "COPIED" or src.get("derived_from_source_id"):
                derived_sources.append(src)
            else:
                primary_sources.append(src)

        independent_count = len(primary_sources)
        total_count = len(sources)

        return {
            "total_sources": total_count,
            "independent_primary_sources": primary_sources,
            "derived_or_copied_sources": derived_sources,
            "independent_source_count": independent_count,
            "independence_ratio": round(independent_count / total_count, 2) if total_count > 0 else 1.0
        }
