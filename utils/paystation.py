import requests

INIT_URL = "https://sandbox.paystation.com.bd/initiate-payment"
STATUS_URL = "https://sandbox.paystation.com.bd/transaction-status"


def initiate_payment(payload):
    # PayStation requires form-data fields
    return requests.post(INIT_URL, data=payload, timeout=30)


def verify_payment(invoice, merchant_id_header):
    res = requests.post(
        STATUS_URL,
        headers={"merchantId": merchant_id_header},
        json={"invoice_number": invoice},
        timeout=30
    )
    return res.json()