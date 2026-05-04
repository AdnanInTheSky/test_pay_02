import os
import uuid
from flask import Flask, request, render_template, redirect, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from utils.paystation import initiate_payment, verify_payment
from products import PRODUCTS

load_dotenv()
app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
MERCHANT_ID = os.getenv("MERCHANT_ID")
PAYSTATION_PASSWORD = os.getenv("PAYSTATION_PASSWORD")
BASE_URL = os.getenv("BASE_URL")

client = MongoClient(MONGO_URI)
db = client["paystation_demo"]
orders = db["orders"]


@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)


@app.route("/buy", methods=["POST"])
def buy():
    data = request.json

    name = data["name"]
    phone = data["phone"]
    email = data["email"]
    address = data["address"]
    cart = data["cart"]  # list of product IDs

    # Secure total calculation
    total = 0
    items = []
    for pid in cart:
        product = PRODUCTS.get(pid)
        if not product:
            return jsonify({"error": "Invalid product"}), 400
        total += product["price"]
        items.append(product["name"])

    invoice = str(uuid.uuid4())

    orders.insert_one({
        "invoice": invoice,
        "status": "pending",
        "amount": total,
        "items": items,
        "customer": {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
    })

    payload = {
        "merchantId": MERCHANT_ID,
        "password": PAYSTATION_PASSWORD,
        "invoice_number": invoice,
        "currency": "BDT",
        "payment_amount": str(total),
        "reference": ", ".join(items),
        "cust_name": name,
        "cust_phone": phone,
        "cust_email": email,
        "cust_address": address,
        "callback_url": f"{BASE_URL}/payment/callback",
        "checkout_items": ", ".join(items)
    }

    res = initiate_payment(payload)

    if res.get("status") != "success":
        return jsonify(res), 400

    return jsonify({"payment_url": res["payment_url"]})


@app.route("/payment/callback")
def payment_callback():
    invoice = request.args.get("invoice_number")
    result = verify_payment(invoice, MERCHANT_ID)
    trx_status = result.get("data", {}).get("trx_status")

    orders.update_one(
        {"invoice": invoice},
        {"$set": {"status": trx_status}}
    )

    return "OK"