# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "AC2dfff936b0900c536e0ce86aa53f5584"
auth_token = "b87fa5b6e1981e6c055ec5aa1828a0d4"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+17192872292", from_="+14842545297",
                                     body="Testing!")