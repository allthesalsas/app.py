from flask import Flask, request, jsonify
from datetime import datetime
import uuid  # for generating unique ids
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask_socketio import SocketIO


app = Flask(__name__)


@app.route("/")
def index():
    with open('templates/index.html', "r") as file:
        chart_html = file.read()
    return f"<p>Hello, World!</p>{chart_html}"


model_name = "microsoft/DialoGPT-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


socketio = SocketIO(app, async_mode='eventlet')


user_info = [
    {
        "id": "0",
        "name": "Gina",
        "email": "email",
        "telegram": "ackerman",
        "preferred contact method": "email",
        "organization name": "Judge Research",
        "signup datetime": "2021-01-01 00:00:00",
        "password": "password",
        "jr-apikey": "jr-apikey",



    },
]


@app.route("/demo", methods=["GET", "POST"])
def demo():
    if request.method == "GET":
        if len(user_info) > 0:
            return jsonify(user_info)
        else:
            return "No users found", 404

    if request.method == "POST":
        new_id = str(uuid.uuid4())
        new_name = request.form["name"]
        new_email = request.form["email"]
        new_telegram = request.form["telegram"]
        new_preferred_contact_method = request.form["preferred contact method"]
        new_organization_name = request.form["organization name"]
        signup_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_password = request.form["password"]
        new_jr_apikey = request.form["jr_apikey"]

        new_obj = {
            'id': new_id,
            'name': new_name,
            'email': new_email,
            'telegram': new_telegram,
            'preferred contact method': new_preferred_contact_method,
            'organization name': new_organization_name,
            'signup datetime': signup_datetime,
            'password': new_password,
            'jr_apikey': new_jr_apikey,
        }
        user_info.append(new_obj)
        return jsonify(user_info), 201


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8000)
