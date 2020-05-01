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


from flask import Flask, render_template, jsonify, request


app = Flask(__name__, static_folder=".",
            static_url_path="", template_folder=".")

curr_inventory = inventory.Inventory()


def calculate_order_amount(c):
    return c.get_total()


def create_cart(items):
    print('Creating cart')
    cart_items = {}

    for item in items:
        item_id = item['id']
        i = curr_inventory.get_item(item_id)
        i['qty'] = item['qty']
        cart_items[item_id] = i

    c = cart.Cart(cart_items)
    return c


def add_customer(customer):
    customers = stripe.Customer.list()
    email = customer['email']
    for c in customers:
        if c.email == email:
            return
    stripe.Customer.create(email=email)


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


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        c = create_cart(data['items'])
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(c),
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
