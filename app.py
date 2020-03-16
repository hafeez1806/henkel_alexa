import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session
import requests


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg).reprompt(render_template('reprom'))


@ask.intent("SalesIntent",convert={'InvOne': str, 'InvTwo': str, 'csname':str},default={'InvOne': 'None','InvTwo': 'None','csname': 'None'})

def Sales(InvOne, InvTwo,csname):
    print(csname)
    final_sentence = ""
    if InvOne != 'None' and InvTwo != 'None' and csname == 'None':
        url = "http://122.179.136.81:4000/henkel/sale"
        params = {"SalOne": InvOne, "SalTwo": InvTwo}
        data = requests.get(url=url, params=params)
        data = data.json()
        final_sentence = data["Response"]
    elif InvOne == 'None' and InvTwo == 'None' and csname != 'None':
        url = "http://122.179.136.81:4000/henkel/customer"
        params = {"CusId": str(csname)}
        data = requests.get(url=url, params=params)
        data = data.json()
        final_sentence = data["Response"]
    else:
        final_sentence = "Kindly provide customer name"
    return question(final_sentence).reprompt(render_template('reprom'))


@ask.intent("InventoryIntent", convert={'InvOne': str, 'InvTwo': str})

def inventory(InvOne, InvTwo):
    final_sentence = ""
    url = "http://122.179.136.81:4000/henkel/inventory"
    params = {"InvOne":InvOne,"InvTwo":InvTwo}
    data = requests.get(url=url,params=params)
    data = data.json()
    final_sentence = data["Response"]
    return question(final_sentence).reprompt(render_template('reprom'))


@ask.intent("OpenOrdersIntent", convert={'InvOne': str, 'InvTwo': str,'InvThree':str},default={'InvThree': 'None'})

def order(InvOne, InvTwo,InvThree):
    final_sentence = ""
    url = "http://122.179.136.81:4000/henkel/order"
    params = {"OrdOne":InvOne,"OrdTwo":InvTwo,"OrdThree":InvThree}
    data = requests.get(url=url,params=params)
    data = data.json()
    final_sentence = data["Response"]
    return question(final_sentence).reprompt(render_template('reprom'))


@ask.intent("AMAZON.StopIntent")

def stop():
    final_sentence = "Alright then, Thank you for using insight bot. Bye."
    return statement(final_sentence)


@ask.intent("AMAZON.YesIntent")

def yes():
    final_sentence = "Okay. what else you want to know ?"
    return question(final_sentence).reprompt(render_template('reprom'))


@ask.intent("CustomerIntent",convert={'number': str},default={'number': 'None'})

def customer_val(csname):
    print(csname)
    final_sentence = ""
    url = "http://122.179.136.81:4000/henkel/customer"
    params = {"CusId": csname}
    data = requests.get(url=url, params=params)
    data = data.json()
    final_sentence = data["Response"]
    return question(final_sentence)


@ask.intent("AMAZON.NoIntent")

def no():
    final_sentence = "Alright then, Thank you for using insight bot. Bye."
    return question(final_sentence)


# @ask.intent("AMAZON.NoIntent")
#
# def no():
#     final_sentence = "Alright then, Thank you for using henkel bot. Bye Bye"
#     return statement(final_sentence)

if __name__ == '__main__':

    app.run(debug=True)