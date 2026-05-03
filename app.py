import os
import uuid
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
from utils.paystation import initiate_payment, verify_payment

load_dotenv()
app = Flask(__name__)

# ENV
MONGO_URI = os.getenv("MONGO_URI")
MERCHANT_ID = os.getenv("MERCHANT_ID")
PAYSTATION_PASSWORD = os.getenv("PAYSTATION_PASSWORD")
BASE_URL = os.getenv("BASE_URL")

client = MongoClient(MONGO_URI)
db = client["paystation_demo"]
orders = db["orders"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/buy", methods=["POST"])
def buy():
    invoice = str(uuid.uuid4())

    orders.insert_one({
        "invoice": invoice,
        "status": "pending",
        "amount": 100
    })

    payload = {
        "merchantId": MERCHANT_ID,
        "password": PAYSTATION_PASSWORD,
        "invoice_number": invoice,
        "currency": "BDT",
        "payment_amount": "100",
        "reference": "Single Product",
        "cust_name": request.form["name"],
        "cust_phone": request.form["phone"],
        "cust_email": request.form["email"],
        "cust_address": "N/A",
        "callback_url": f"{BASE_URL}/payment/callback",
        "checkout_items": "Single Product"
    }

    res = initiate_payment(payload)

    if res.get("status") != "success":
        return f"Error: {res}"

    # redirect to checkout page
    return redirect(res["payment_url"])


@app.route("/payment/callback")
def payment_callback():
    invoice = request.args.get("invoice_number")

    result = verify_payment(invoice, MERCHANT_ID)

    trx_status = result.get("data", {}).get("trx_status")

    if trx_status == "success":
        orders.update_one(
            {"invoice": invoice},
            {"$set": {"status": "paid"}}
        )
        return "Payment Successful"

    orders.update_one(
        {"invoice": invoice},
        {"$set": {"status": trx_status}}
    )
    return f"Payment {trx_status}"