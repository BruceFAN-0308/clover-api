import random

import requests

from config import BASE_URL, HEADERS


# common request use the same headers, only the URL is different.
def base_request(url: str):
    url = BASE_URL + url
    headers = HEADERS
    response = requests.post(url, headers=headers)
    print(response.text)


# home page request, every payment finished, call this API.
def welcome():
    base_request("/device/welcome")


# successful request, after tap or insert the card, call this API.
def success():
    base_request("/device/thank-you")


def show_message():
    url = BASE_URL + "/device/display"

    payload = {
        "beep": False,
        "text": "test"
    }
    headers = HEADERS

    additional_headers = {
        "content-type": "application/json",
    }
    headers.update(additional_headers)
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


# payment request, let the FLEX device shows amount.
def payment():
    url = BASE_URL + "/payments"

    headers = HEADERS

    additional_headers = {
        "content-type": "application/json",
        # todo Idempotency-Key should be unique and idempotent
        "Idempotency-Key": str(random.randint(1, 100000000))
    }

    headers.update(additional_headers)

    payload = {
        "capture": True,
        "deviceOptions": {
            "disableCashback": False,
            "offlineOptions": {
                "allowOfflinePayment": False,
                "approveOfflinePaymentWithoutPrompt": False,
                "forceOfflinePayment": False
            },
            "cardEntryMethods": ["MAG_STRIPE", "EMV", "NFC"],
            "cardNotPresent": False
        },
        "final": True,
        # real payment money = amount // 100 (avoid processing the decimal problems)
        # todo number need to change
        "amount": 10000,
        # todo paymentId should be unique
        "externalPaymentId": "111"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def successful_payment_processing():
    # go to the home page
    welcome()
    # payment
    payment()
    # success
    success()
    # goto the home page
    welcome()

print("test")
