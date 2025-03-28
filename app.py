from flask import Flask, request

app = Flask(__name__)

@app.route('/wubook/ack', methods=['POST'])
def ack_test():
    print("✅ WuBook ACK pingovan!")
    print("📦 Podaci:", request.form.to_dict())

    return """
        <h2>✅ ACK RECEIVED</h2>
        <p>WuBook nas je uspešno kontaktirao.</p>
        <pre>{}</pre>
    """.format(request.form.to_dict())

# Ako Render koristi port promenljivu:
if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

