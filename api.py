from flask import Flask, request, jsonify
from services.inventory import view_products, search_product
from services.orders import place_order
from services.auth import authenticate

app = Flask(__name__)

# 🔐 Login API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    role = authenticate(data["username"], data["password"])

    if role:
        return jsonify({
            "status": "success",
            "role": role
        })
    return jsonify({
        "status": "fail",
        "message": "Invalid credentials"
    }), 401

# 📦 Get all products
@app.route("/api/products", methods=["GET"])
def products():
    products = view_products()
    result = []

    for p in products:
        result.append({
            "id": p[0],
            "name": p[1],
            "category": p[2],
            "aisle": p[3],
            "price": p[4],
            "stock": p[5]
        })

    return jsonify(result)

# 🔍 Search product
@app.route("/api/search", methods=["GET"])
def search():
    name = request.args.get("name")
    results = search_product(name)

    data = []
    for r in results:
        data.append({
            "name": r[0],
            "aisle": r[1],
            "price": r[2],
            "stock": r[3]
        })

    return jsonify(data)

# 🧾 Place order
@app.route("/api/order", methods=["POST"])
def order():
    data = request.json

    try:
        place_order(
            customer_id=1,
            product_id=data["product_id"],
            quantity=data["quantity"]
        )
        return jsonify({
            "status": "success",
            "message": "Order placed"
        })
    except Exception as e:
        return jsonify({
            "status": "fail",
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(debug=True)
