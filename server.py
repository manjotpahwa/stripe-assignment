#! /usr/bin/env python3.6
"""
Main module for taking care of payment request, cart, order.
"""
import json
import os
import stripe
import cart
import inventory
stripe.api_key = "sk_test_edhurKZR5OMK0Wvl7uYLyu1n"
webhook_secret = "whsec_K8reb65yXmHSEyKkSMx8h84rozwb5R69"



from flask import Flask, render_template, jsonify, request


app = Flask(__name__, static_folder=".",
            static_url_path="", template_folder=".")

curr_inventory = inventory.Inventory()


def calculate_order_amount(c):
    return c.get_total()


def create_cart(items):
    app.logger.debug('Creating cart')
    cart_items = {}

    for item in items:
        item_id = item['id']
        i = curr_inventory.get_item(item_id)
        i['qty'] = item['qty']
        cart_items[item_id] = i

    c = cart.Cart(cart_items)
    return c


def create_customer(customer_email):
    customers = stripe.Customer.list()
    for c in customers:
        if c.email == customer_email:
            return c
    return stripe.Customer.create(email=customer_email)


@app.route('/get-products-in-stock', methods=['GET'])
def get_products_in_stock():
    return curr_inventory.get_products_in_stock()


@app.route('/show-total', methods=['GET'])
def show_total(items):
    try:
        data = json.loads(request.data)
        c = create_cart(data['items'])
        return jsonify({
            'total': calculate_order_amount(c)
            })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data.decode("utf-8")
    print(payload)
    received_sig = request.headers.get("Stripe-Signature", None)

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, received_sig, webhook_secret)
    except ValueError:
        print("Error while decoding event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        print("Invalid signature!")
        return "Bad signature", 400

    print(
        "Received event: id={id}, type={type}".format(
            id=event.id, type=event.type
        )
    )

    return "Webhook event received", 200


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        c = create_cart(data['items'])
        customer = create_customer(data['email'])
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(c),
            currency=data['currency'],
            metadata={'integration_check': 'accept_a_payment'},
        )
        app.logger.debug("Intent")
        app.logger.debug(intent)

        return jsonify({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


if __name__ == '__main__':
    app.run(debug=True)
