from typing import List, Dict, Any, Union

class NumericalEngine:
    @staticmethod
    def sum_quantities(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Calculates total quantity deterministically."""
        return sum(numbers)

    @staticmethod
    def calculate_delta(expected: Union[int, float], actual: Union[int, float]) -> Dict[str, Any]:
        """Calculates variance delta and percentage discrepancy."""
        diff = actual - expected
        pct = (diff / expected * 100.0) if expected != 0 else 0.0
        return {
            "expected": expected,
            "actual": actual,
            "difference": diff,
            "percentage_diff": round(pct, 2),
            "matches": diff == 0
        }

    @staticmethod
    def reconcile_shipments(ordered_qty: int, shipments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Reconciles multiple partial shipments against ordered quantity deterministically.
        Shipments list example: [{"shipment_id": "1", "qty": 8500}, {"shipment_id": "2", "qty": 1500}]
        """
        delivered_total = sum(s.get("qty", 0) for s in shipments)
        shortfall = ordered_qty - delivered_total
        return {
            "ordered_quantity": ordered_qty,
            "total_delivered": delivered_total,
            "shortfall": shortfall if shortfall > 0 else 0,
            "excess": abs(shortfall) if shortfall < 0 else 0,
            "is_fully_delivered": delivered_total >= ordered_qty,
            "shipment_count": len(shipments)
        }
