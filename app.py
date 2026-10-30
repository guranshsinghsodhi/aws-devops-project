from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = {"1001": "Packed", "1002": "Shipped", "1003": "Delivered"}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Order Tracking</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: Segoe UI, Arial, sans-serif; background: #f1f5f9; color: #0f172a; }
  header { background: linear-gradient(135deg, #1e3a8a, #7c3aed); color: #fff; padding: 48px 20px 80px; text-align: center; }
  header h1 { margin: 0 0 8px; font-size: 2rem; }
  header p { margin: 0; opacity: 0.85; }
  .tag { display: inline-block; margin-top: 14px; padding: 4px 12px; border-radius: 999px; background: rgba(255,255,255,0.18); font-size: 0.8rem; }
  main { max-width: 560px; margin: -48px auto 40px; padding: 0 16px; }
  .card { background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 10px 30px rgba(15,23,42,0.12); }
  .row { display: flex; gap: 10px; }
  input { flex: 1; padding: 12px 14px; font-size: 1rem; border: 2px solid #e2e8f0; border-radius: 10px; outline: none; }
  input:focus { border-color: #7c3aed; }
  button { padding: 12px 20px; font-size: 1rem; border: 0; border-radius: 10px; color: #fff; background: #7c3aed; cursor: pointer; }
  button:hover { background: #6d28d9; }
  .chips { margin-top: 14px; font-size: 0.9rem; color: #64748b; }
  .chip { display: inline-block; margin: 4px 6px 0 0; padding: 4px 12px; border-radius: 999px; background: #ede9fe; color: #5b21b6; cursor: pointer; }
  #result { margin-top: 22px; }
  .msg { padding: 14px; border-radius: 10px; background: #fee2e2; color: #991b1b; }
  .order { font-size: 1.1rem; margin-bottom: 14px; }
  .tracker { display: flex; gap: 8px; }
  .step { flex: 1; text-align: center; padding: 12px 6px; border-radius: 10px; background: #f1f5f9; color: #94a3b8; font-weight: 600; }
  .step.done { background: #dcfce7; color: #166534; }
  .step.now { background: #7c3aed; color: #fff; }
  footer { text-align: center; color: #94a3b8; font-size: 0.85rem; padding-bottom: 30px; }
</style>
</head>
<body>
<header>
  <h1>Order Tracking</h1>
  <p>Check where your order is, in one step.</p>
  <span class="tag">Running on AWS ECS Fargate &middot; v3</span>
</header>
<main>
  <div class="card">
    <div class="row">
      <input id="oid" placeholder="Enter order number, e.g. 1001">
      <button onclick="track()">Track</button>
    </div>
    <div class="chips">Try:
      <span class="chip" onclick="track('1001')">1001</span>
      <span class="chip" onclick="track('1002')">1002</span>
      <span class="chip" onclick="track('1003')">1003</span>
    </div>
    <div id="result"></div>
  </div>
</main>
<footer>Deployed automatically by GitHub Actions &middot; Infrastructure by CloudFormation</footer>
<script>
  const steps = ["Packed", "Shipped", "Delivered"];
  document.getElementById("oid").addEventListener("keydown", function (e) {
    if (e.key === "Enter") { track(); }
  });
  async function track(id) {
    const box = document.getElementById("oid");
    const out = document.getElementById("result");
    id = (id || box.value).trim();
    out.textContent = "";
    if (!id) { return; }
    box.value = id;
    const r = await fetch("/orders/" + encodeURIComponent(id));
    const data = await r.json();
    if (!r.ok) {
      const m = document.createElement("div");
      m.className = "msg";
      m.textContent = data.error || "Something went wrong.";
      out.appendChild(m);
      return;
    }
    const title = document.createElement("div");
    title.className = "order";
    title.textContent = "Order " + data.order_id + " is " + data.status;
    out.appendChild(title);
    const bar = document.createElement("div");
    bar.className = "tracker";
    const at = steps.indexOf(data.status);
    steps.forEach(function (s, i) {
      const d = document.createElement("div");
      d.className = "step" + (i < at ? " done" : "") + (i === at ? " now" : "");
      d.textContent = s;
      bar.appendChild(d);
    });
    out.appendChild(bar);
  }
</script>
</body>
</html>"""


@app.route("/")
def home():
    return PAGE


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
