
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Privremeno cuvamo async_url ovde (test varijanta)
async_urls = {}

@app.route("/wubook/ack", methods=["POST"])
def ack_handler():
    data = request.form
    transaction_id = data.get("transaction")
    async_url = data.get("async_ok_url")
    amount = data.get("deposit")
    currency = data.get("currency_iso") or "EUR"
    name = data.get("first_name", "") + " " + data.get("last_name", "")

    # Sacuvaj async URL
    async_urls[transaction_id] = async_url

    html = f'''
    <h2>Booking for {name}</h2>
    <p>Deposit: {amount} {currency}</p>
    <script src="https://checkout.bridgerpay.com/v2/launcher"
      data-checkout-key="0552953d-6f97-4682-a5fe-1583170022b3"
      data-currency="{currency}"
      data-country="IT"
      data-amount="{amount}"
      data-custom="{transaction_id}"
      data-currency-lock="true">
    </script>
    '''
    return render_template_string(html)

@app.route("/bp/webhook", methods=["POST"])
def bp_webhook():
    data = request.json
    transaction_id = data.get("custom")
    status = data.get("status")
    async_url = async_urls.get(transaction_id)

    if status == "APPROVED" and async_url:
        try:
            r = requests.get(async_url)
            print(f"WuBook async confirmation sent: {r.status_code}")
        except Exception as e:
            print(f"Failed to confirm WuBook: {e}")
    return "", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
