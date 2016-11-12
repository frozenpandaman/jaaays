from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def send_report():

    out = open("out.txt", 'r')

    resp = twilio.twiml.Response()
    resp.message(out.read())

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
