
from app import app

def test_home():
    assert app.test_client().get("/").status_code == 200

def test_health():
    assert app.test_client().get("/health").json["status"] == "ok"

def test_order_found():
    r = app.test_client().get("/orders/1001")
    assert r.status_code == 200
    assert r.json["status"] == "Packed"

def test_order_missing():
    assert app.test_client().get("/orders/9999").status_code == 404
