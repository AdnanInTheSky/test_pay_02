import os
import requests

INIT_URL = "https://sandbox.paystation.com.bd/initiate-payment"
STATUS_URL = "https://sandbox.paystation.com.bd/transaction-status"

def initiate_payment(payload):
    return requests.post(INIT_URL, files=payload, timeout=30)

def verify_payment(invoice, merchant_id):
    res = requests.post(
        STATUS_URL,
        headers={"merchantId": merchant_id},
        json={"invoice_number": invoice},
        timeout=30
    )
    return res.json()