from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_shopping_key'


PRODUCTS = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 250, 'stock': 12, 'image': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400'},
    {'id': 2, 'name': 'Mechanical Keyboard', 'price': 790, 'stock': 5, 'image': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400'},
    {'id': 3, 'name': 'USB', 'price': 350, 'stock': 8, 'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400'},
    {'id': 4, 'name': 'HD Monitor', 'price': 18900, 'stock': 3, 'image': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400'}
]


BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Shop</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800">
    <nav class="bg-white shadow p-4 flex justify-between items-center px-8">
        <a href="/" class="text-xl font-bold text-blue-600">⚡ QuickShop</a>
        <a href="/cart" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition">
            🛒 Cart (<span>{{ session.get('cart', {}) | length }}</span>)
        </a>
    </nav>
    <main class="max-w-6xl mx-auto p-6">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
"""

CATALOG_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1 class="text-2xl font-bold mb-6">Product Catalog</h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
        {% for product in products %}
        <div class="bg-white p-4 rounded-xl shadow border border-gray-100 flex flex-col justify-between">
            <div>
                <img src="{{ product.image }}" alt="{{ product.name }}" class="w-full h-40 object-cover rounded-lg mb-3">
                <h2 class="font-semibold text-lg">{{ product.name }}</h2>
                <p class="text-blue-600 font-bold mt-1">${{ "%.2f"|format(product.price) }}</p>
            </div>
            <a href="/add/{{ product.id }}" class="mt-4 block text-center bg-gray-900 text-white py-2 rounded-lg hover:bg-gray-800 transition">
                Add to Cart
            </a>
        </div>
        {% endfor %}
    </div>
""")

CART_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1 class="text-2xl font-bold mb-6">Your Shopping Cart</h1>
    {% if cart_items %}
    <div class="bg-white rounded-xl shadow overflow-hidden">
        <table class="w-full text-left border-collapse">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
                <tr>
                    <th class="p-4">Product</th>
                    <th class="p-4">Price</th>
                    <th class="p-4">Quantity</th>
                    <th class="p-4">Subtotal</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                {% for item in cart_items %}
                <tr>
                    <td class="p-4 font-medium">{{ item.name }}</td>
                    <td class="p-4">${{ "%.2f"|format(item.price) }}</td>
                    <td class="p-4">{{ item.qty }}</td>
                    <td class="p-4 font-bold">${{ "%.2f"|format(item.subtotal) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="p-6 bg-gray-50 flex justify-between items-center border-t">
            <span class="text-xl font-bold">Total: ${{ "%.2f"|format(total) }}</span>
            <div class="space-x-4">
                <a href="/" class="text-blue-600 hover:underline">Continue Shopping</a>
                <a href="/checkout" class="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition">
                    Checkout
                </a>
            </div>
        </div>
    </div>
    {% else %}
    <div class="text-center py-16 bg-white rounded-xl shadow">
        <p class="text-gray-500 text-lg mb-4">Your cart is currently empty.</p>
        <a href="/" class="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700">Start Shopping</a>
    </div>
    {% endif %}
""")

@app.route('/')
def catalog():
    return render_template_string(CATALOG_TEMPLATE, products=PRODUCTS)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('catalog'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for prod_id, qty in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(prod_id)), None)
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            cart_items.append({
                'name': product['name'],
                'price': product['price'],
                'qty': qty,
                'subtotal': subtotal
            })
            
    return render_template_string(CART_TEMPLATE, cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return """
    <body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#f9fafb;">
        <h1 style="color:#16a34a;">Order Placed Successfully! 🎉</h1>
        <p>Thank you for testing the shopping system.</p>
        <a href="/" style="color:#2563eb; text-decoration:none; font-weight:bold;">Return to Store</a>
    </body>
    """

if __name__ == '__main__':
    app.run(debug=True)
