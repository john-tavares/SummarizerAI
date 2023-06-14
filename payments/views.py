from flask import request, Blueprint
import libs.blip as blip
import os
import stripe

MESSAGE_SUBSCRIPTION = """Agora sim, meu amigo!\n\nEstou tão feliz por ter você aqui comigo no plano premium! 🤩\n\nVamos lá, agora estamos juntos 24/7 e você pode me mandar mensagem sempre que precisar de ajuda.\n\nO Programador vai ficar tão feliz em saber que você confia em mim para te ajudar! ❤️"""

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/webhook', methods=['POST'])
def webhook():
    stripe.api_key = os.environ['STRIPE_APIKEY']
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ['STRIPE_ENDPOINT_SECRET']
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        identifier = event['data']['object']["client_reference_id"]
        subscription_id = event['data']['object']['subscription']
        source = event['data']['object']['metadata']['Origem']
        reciver_id = blip.transform_identifier_in_reciver_id(identifier, source)
        response = blip.update_contact(os.environ['BLIP_APIKEY'], reciver_id, subscription_id)
        print('Salvando ID da Stripe...', response)
        response = blip.send_raw_message(os.environ['BLIP_APIKEY'], reciver_id, MESSAGE_SUBSCRIPTION)
        print(reciver_id, response, subscription_id)
    return {'event': event}

@payments_bp.route('/verify/<id>', methods=['GET'])
def verify(id):
    stripe.api_key = os.environ['STRIPE_APIKEY']
    try:
        response = stripe.Subscription.retrieve(id)
        status = response['status']
    except:
        status = "not_found"
    return {'status': status}