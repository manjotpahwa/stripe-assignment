#! /usr/bin/env python3.6
"""
Main module for taking care of payment request, cart, order.
"""
import json
import os
import stripe
import cart
import config
import inventory

from flask import Flask, render_template, jsonify, request

stripe.api_key =  config.STRIPE_API_KEY
webhook_secret = config.WEBHOOK_SECRET


app = Flask(__name__, static_folder=".",
            static_url_path="", template_folder=".")

curr_inventory = inventory.Inventory()
# TODO(manjot): This cart is silly and a blanket one irrespective of customers.
# Add the option to have it on per customer basis.
curr_cart = cart.Cart()


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

    curr_cart.set_items(cart_items)
    return curr_cart


def create_customer(customer_email):
    # TODO(manjot): we should probably add a customer entry to our ecommerce
    # store's own database first.
    #
    customers = stripe.Customer.list()
    for c in customers:
        if c.email == customer_email:
            return c
    return stripe.Customer.create(email=customer_email)


def update_cart_post_payment():
    curr_cart.set_items({})


def update_inventory_post_payment():
    curr_inventory.update_inventory(curr_cart)


def is_failed_event(event_type):
    if event_type == 'charge.failed' or \
            event_type == 'payment_intent.payment_failed':
                return True
    return False


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello world!', 200


@app.route('/get-products-in-stock', methods=['GET'])
def get_products_in_stock():
    return curr_inventory.get_products_in_stock(), 200


@app.route('/get-cart', methods=['GET'])
def get_cart():
    try:
        app.logger.info("Showing cart: ")
        app.logger.info(curr_cart.get_items())
        return curr_cart.get_items(), 200
    except Exception as e:
        app.logger.error("Error showing cart: " + str(e))
        return jsonify(error=str(e)), 403


@app.route('/get-total', methods=['GET'])
def get_total():
    try:
        return jsonify({
            'total': calculate_order_amount(curr_cart)
            })
    except Exception as e:
        app.logger.error("Error showing total: " + str(e))
        return jsonify(error=str(e)), 403


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data.decode("utf-8")
    received_sig = request.headers.get("Stripe-Signature", None)

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, received_sig, webhook_secret)
    except ValueError:
        app.logger.error("Error while decoding event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        app.logger.error("Invalid signature!")
        return "Bad signature", 400

    app.logger.debug(
        "Received event: id={id}, type={type}".format(
            id=event.id, type=event.type
        )
    )

    if event.type == 'charge.succeeded':
        # TODO(manjot): Potentially crearte rewards for customer based on
        # their purchase history.
        update_inventory_post_payment()
        update_cart_post_payment()

    elif is_failed_event(event.type):
        # handle failures and do retries.
        app.logger.error("Payment failed event type " + event.type)

    return "Webhook event received", 200


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        curr_cart = create_cart(data['items'])
        customer = create_customer(data['email'])
        app.logger.debug(customer)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(curr_cart) * 100,
            currency=data['currency'],
            customer=customer.id,
            metadata={
                'integration_check': 'accept_a_payment'
                },
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
