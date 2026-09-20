import pytest
from app.services.numerical_engine import NumericalEngine

def test_partial_shipment_reconciliation():
    shipments = [
        {"shipment_id": "1", "qty": 8500},
        {"shipment_id": "2", "qty": 1500}
    ]
    res = NumericalEngine.reconcile_shipments(10000, shipments)
    
    assert res["ordered_quantity"] == 10000
    assert res["total_delivered"] == 10000
    assert res["is_fully_delivered"] is True
    assert res["shortfall"] == 0

def test_warehouse_intake_delta():
    res = NumericalEngine.calculate_delta(8500, 8470)
    assert res["expected"] == 8500
    assert res["actual"] == 8470
    assert res["difference"] == -30
    assert res["matches"] is False
