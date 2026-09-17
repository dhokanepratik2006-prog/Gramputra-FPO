from flask import Flask, render_template

app = Flask(__name__)

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


@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


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
