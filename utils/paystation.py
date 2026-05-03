import os
import requests

MERCHANT_ID = os.getenv("MERCHANT_ID")
PASSWORD = os.getenv("PAYSTATION_PASSWORD")

INIT_URL = "https://sandbox.paystation.com.bd/initiate-payment"
STATUS_URL = "https://sandbox.paystation.com.bd/transaction-status"


def initiate_payment(payload: dict):
    return requests.post(INIT_URL, files=payload)


def verify_payment(invoice: str):
    res = requests.post(
        STATUS_URL,
        headers={"merchantId": MERCHANT_ID},
        json={"invoice_number": invoice},
        timeout=20
    )
    return res.json()