import json
import os
from time import sleep
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

"""Sample pure Lambda function

Parameters
----------
event: dict, required
    API Gateway Lambda Proxy Input Format

    Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

context: object, required
    Lambda Context runtime methods and attributes

    Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

Returns
------
API Gateway Lambda Proxy Output Format: dict

    Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
"""
def lambda_handler(event, context):

    """Create Twilio Client

    Whatsapp template format doc: https://www.twilio.com/docs/whatsapp/api#whatsapp-message-template-format
    """
    client = Client(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])

    """Print payload sent from Pinpoint. 

    Custom Channels doc: https://docs.aws.amazon.com/pinpoint/latest/developerguide/channels-custom.html
    """
    print(event)

    # A valid invocation of this channel by the Pinpoint Service will include Endpoints in the event payload.
    if 'Endpoints' not in event:
        return response_obj(500, f'Payload does not contain endpoints. Event: {event}')

    endpoints = event['Endpoints']

    for endpoint_id in endpoints:

        """The endpoint profile contains the entire endpoint definition.

        Attributes and UserAttributes can be interpolated into your message for personalization.
        """
        endpoint_profile = endpoints[endpoint_id]

        """Any Valid phone number
        """
        address = endpoint_profile['Address']

        """Construct your message here.  You have access to the endpoint profile to personalize the message with Attributes.
        
        `message = "Hello {name}!".format(name=endpoint_profile["Attributes"]["FirstName"])`
        """
        message = 'Hello World! - Pinpoint Whatsapp Channel'

        try:
            """Twilio Whatsapp documentation: https://www.twilio.com/docs/whatsapp/quickstart/python
            """
            response = client.messages.create(
              from_='whatsapp:+14155238886',
              body=message,
              to=f'whatsapp:{address}'
            )
            print(response)
            return response_obj(200, response.status)
        except TwilioRestException as e:
            return response_obj(500, f"{e}")

        """Required to avoid hitting rate limit."""
        sleep(1)

    return(response_obj(200, "Complete"))


def response_obj(statusCode, message):
    return {
        'statusCode': statusCode,
        'body': json.dumps({
            'message': message,
        }),
    }