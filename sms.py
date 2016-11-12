from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def send_report():

    VALID_COMMANDS = [ "open", "line" ]

    user_text = request.values.get('Body', None)
    resp = twilio.twiml.Response()

    if jays_is_open() and "open" in user_text:
        process_sms_command("open", resp)
    elif jays_is_open() and "line" in user_text:
        print "line boop"
        process_sms_command("line", resp)
    elif not jays_is_open(): # closed
        print "thinks it's clsoed"
        process_sms_command("open", resp)
    else: # unrecognized command and open
        process_sms_command("open", resp)
        process_sms_command("line", resp)

    return str(resp)

def jays_is_open():
    out = open("out_open.txt", 'r')
    openness = (out.read().strip().split(" ")[-1] == "open!")
    out.close()
    return openness

def process_sms_command(text, response):
    out = open("out_" + text + ".txt", 'r')
    response.message(out.read())
    out.close()

if __name__ == "__main__":
    app.run(debug=True)
