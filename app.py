from flask import Flask, jsonify
app = Flask(__name__)

ORDERS = {"1001": "Packed", "1002": "Shipped", "1003": "Delivered"}

@app.route("/")
def home():
    return "Order Tracking API - v3"

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/orders/<order_id>")
def order(order_id):
    status = ORDERS.get(order_id)
    if status is None:
        return jsonify(error="Order not found"), 404
    return jsonify(order_id=order_id, status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)