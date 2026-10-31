from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

GOOD = {
    "tenure_months": 12,
    "monthly_charges": 70.5,
    "contract": "month-to-month",
    "internet_service": "fiber",
    "support_calls": 1,
}


def test_health_reports_version():
    """Protects the /health contract: load balancers and K8s probes call it."""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model_version"] == "1.0.0"


def test_model_loads_and_predicts():
    """Protects model loading: a broken joblib file would fail here."""
    r = client.post("/predict", json=GOOD)
    assert r.status_code == 200
    assert "churn_probability" in r.json()


def test_rejects_negative_tenure():
    """Input schema: negative tenure must be a 422, not a 500."""
    bad = {**GOOD, "tenure_months": -1}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_rejects_missing_contract():
    """Input schema: missing contract must be rejected."""
    bad = {k: v for k, v in GOOD.items() if k != "contract"}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_output_is_a_probability():
    """Output contract: must be between 0 and 1."""
    p = client.post("/predict", json=GOOD).json()["churn_probability"]
    assert 0.0 <= p <= 1.0


def test_edge_case_zero_tenure():
    """Edge case: a brand-new customer (0 months) must still score."""
    edge = {**GOOD, "tenure_months": 0}
    r = client.post("/predict", json=edge)
    assert r.status_code == 200
    assert 0.0 <= r.json()["churn_probability"] <= 1.0


def test_deterministic_prediction():
    """Identical inputs must give identical outputs."""
    p1 = client.post("/predict", json=GOOD).json()["churn_probability"]
    p2 = client.post("/predict", json=GOOD).json()["churn_probability"]
    assert p1 == p2
