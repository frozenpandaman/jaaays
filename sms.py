from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def send_report():

    VALID_COMMANDS = [ "open", "line" ]

    user_text = request.values.get('Body', None)

    open_file = lambda x: open("out_" + x + ".txt", 'r')

    if user_text in VALID_COMMANDS:
        out = open_file(user_text)
        resp = twilio.twiml.Response()
        resp.message(out.read())
    else:
        resp = twilio.twiml.Response()
        outs = map(open_file, VALID_COMMANDS)
        map(lambda x: resp.message(x.read()), outs)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
