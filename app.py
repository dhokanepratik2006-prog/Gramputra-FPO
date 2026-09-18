import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, abort, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MESSAGES_FILE = BASE_DIR / "messages.json"

PRODUCTS = [
    {
        "slug": "gramputra-pavdar",
        "name": "Gramputra Pavdar",
        "price": "₹320",
        "weight": "1 kg",
        "packaging": "Plastic Jar",
        "description": "Premium quality gram product sourced and packed with care for healthy and fresh farming produce.",
        "image": "gramputra-product.svg",
    },
    {
        "slug": "gramputra-lojang",
        "name": "Gramputra Lojang",
        "price": "₹340",
        "weight": "1 kg",
        "packaging": "Plastic Jar",
        "description": "Nutrient-rich and cleanly packed product made for daily kitchen needs and quality household use.",
        "image": "gramputra-product.svg",
    },
    {
        "slug": "gramputra-jalebi-gram",
        "name": "Gramputra Jalebi Gram",
        "price": "₹300",
        "weight": "1 kg",
        "packaging": "Plastic Jar",
        "description": "A trusted farm produce item ideal for kitchen use, value, and freshness with consistent quality.",
        "image": "gramputra-product.svg",
    },
    {
        "slug": "gramputra-mixed-product",
        "name": "Gramputra Mixed Farm Product",
        "price": "₹350",
        "weight": "1 kg",
        "packaging": "Plastic Jar",
        "description": "Carefully selected quality produce from farmer communities, packed for freshness and reliability.",
        "image": "gramputra-product.svg",
    },
]


def load_messages():
    if not MESSAGES_FILE.exists():
        return []
    try:
        with MESSAGES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_messages(messages):
    with MESSAGES_FILE.open("w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=2)


def send_contact_email(name, sender_email, message):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient_email = os.getenv("CONTACT_EMAIL", "pratikdhokane623@gmail.com")

    if not smtp_username or not smtp_password or not recipient_email:
        return False

    email_message = EmailMessage()
    email_message["Subject"] = "New website contact message"
    email_message["From"] = smtp_username
    email_message["To"] = recipient_email
    email_message["Reply-To"] = sender_email
    email_message.set_content(
        f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"
    )

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
        return True
    except (OSError, smtplib.SMTPException, ValueError):
        return False


@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    email_sent = False
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if name and email and message:
            messages = load_messages()
            messages.append({
                'name': name,
                'email': email,
                'message': message,
            })
            save_messages(messages)
            email_sent = send_contact_email(name, email, message)
            success = True

    return render_template('contact.html', success=success, email_sent=email_sent)


@app.route('/messages')
def messages_page():
    abort(404)


@app.route('/products')
def products():
    return render_template('products.html', products=PRODUCTS)


@app.route('/product/<slug>')
def product_detail(slug):
    product = next((item for item in PRODUCTS if item['slug'] == slug), None)
    if product is None:
        return "Product not found", 404
    return render_template('product.html', product=product)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
