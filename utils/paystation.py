import requests

BASE = "https://sandbox.paystation.com.bd"

def initiate_payment(payload):
    res = requests.post(
        f"{BASE}/initiate-payment",
        data=payload,
        timeout=30
    )
    return res.json()


def verify_payment(invoice, merchant_id):
    res = requests.post(
        f"{BASE}/transaction-status",
        headers={"merchantId": merchant_id},
        data={"invoice_number": invoice},
        timeout=30
    )
    return res.json()