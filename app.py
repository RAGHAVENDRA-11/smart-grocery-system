from flask import Flask, render_template, request, redirect, url_for, session
from services.inventory import add_product, view_products, search_product
from services.orders import place_order
from services.auth import authenticate

app = Flask(__name__)
app.secret_key = "secret123"  # session key

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = authenticate(
            request.form["username"],
            request.form["password"]
        )
        if role:
            session["role"] = role
            return redirect(url_for("dashboard"))
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect(url_for("login"))

    products = view_products()
    return render_template(
        "dashboard.html",
        role=session["role"],
        products=products
    )

@app.route("/add", methods=["POST"])
def add():
    if session.get("role") != "admin":
        return "Access Denied"

    add_product(
        request.form["name"],
        request.form["category"],
        request.form["aisle"],
        float(request.form["price"]),
        int(request.form["stock"])
    )
    return redirect(url_for("dashboard"))

@app.route("/search", methods=["POST"])
def search():
    results = search_product(request.form["name"])
    return render_template("search.html", results=results)

@app.route("/order", methods=["POST"])
def order():
    place_order(
        1,  # single demo customer
        int(request.form["product_id"]),
        int(request.form["quantity"])
    )
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

