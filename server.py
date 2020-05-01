#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import os
import stripe
import inventory
stripe.api_key = "sk_test_edhurKZR5OMK0Wvl7uYLyu1n"


from flask import Flask, render_template, jsonify, request


app = Flask(__name__, static_folder=".",
            static_url_path="", template_folder=".")

inventory = inventory.Inventory()


def calculate_order_amount(items):
    return inventory.get_products_total_cost(items)


def add_customer(customer):
    customers = stripe.Customer.list()
    email = customer['email']
    for c in customers:
        if c.email == email:
            return
    stripe.Customer.create(email=email)


@app.route('/get-products-in-stock', methods=['GET'])
def get_products_in_stock():
    return inventory.get_products_in_stock()


@app.route('/show-total', methods=['GET'])
def show_total(items):
    try:
        data = json.loads(request.data)
        return jsonify({
            'total': calculate_order_amount(data['items'])
            })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency=data['currency'],
            metadata={'integration_check': 'accept_a_payment'},
        )
        print("Intent")
        print(intent)

        return jsonify({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


if __name__ == '__main__':
    app.run()
