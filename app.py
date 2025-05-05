# Jim Pinto
# Final Project
# 05/01/2025
# app.py
# Flask Crypto Tracker App with CoinGecko API
# Features: Login, Favorites, Coin Details, Bootstrap Styling

from flask import Flask, render_template_string, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample user (in real apps, use a database and hashed passwords)
users = {
    'jimpinto': 'jimpinto'
}

# Helper to get top 10 coins from CoinGecko API
def get_top_cryptos():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Ensure all coins have a valid 'current_price'
    for coin in data:
        coin['current_price'] = coin.get('current_price', 0)  # Default to 0 if missing

    return data

# Helper to get coin details
def get_coin_details(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    response = requests.get(url)
    return response.json()

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            session['favorites'] = []
            return redirect(url_for('home'))
        return 'Invalid credentials'
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login - Crypto Tracker</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #0d1117;
                color: white;
            }
            .login-card {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container d-flex flex-column align-items-center justify-content-center" style="height: 100vh;">
            <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png" alt="Crypto Logo" width="100" class="mb-4">
            <div class="login-card p-5 shadow" style="min-width: 320px;">
                <h3 class="text-center mb-4">Login</h3>
                <form method="POST">
                    <div class="mb-3">
                        <input type="text" class="form-control" name="username" placeholder="Username" required>
                    </div>
                    <div class="mb-3">
                        <input type="password" class="form-control" name="password" placeholder="Password" required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-success">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    """)

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Route: Home Page (list of coins)
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    cryptos = get_top_cryptos()
    favorites = session.get('favorites', [])
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>💲 Crypto Tracker 💲</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f0f2f5;
            }
            .coin-card {
                border: 1px solid #dee2e6;
                border-radius: 12px;
                transition: transform 0.2s ease;
                background: #fff;
            }
            .coin-card:hover {
                transform: translateY(-5px);
            }
            .coin-logo {
                height: 50px;
            }
        </style>
    </head>
    <body>
        <div class="container py-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>💲 Crypto Tracker 💲</h1>
                <div>
                    <a href="{{ url_for('view_favorites') }}" class="btn btn-outline-success me-2">View Favorites</a>
                    <a href="{{ url_for('logout') }}" class="btn btn-outline-danger">Logout</a>
                </div>
            </div>
            <div class="row">
                {% for coin in cryptos %}
                <div class="col-md-4 mb-4">
                    <div class="p-3 shadow-sm coin-card h-100 text-center">
                        <img src="{{ coin.image }}" alt="{{ coin.name }} Logo" class="coin-logo mb-2">
                        <h5>{{ coin.name }} ({{ coin.symbol.upper() }})</h5>
                        <p>Price: ${% if coin.current_price is not none %}{{ '{:,.2f}'.format(coin.current_price) }}{% else %}N/A{% endif %}</p>
                        <a href="{{ url_for('coin_detail', coin_id=coin.id) }}" class="btn btn-sm btn-primary mb-2">Details</a>
                        {% if coin.id in favorites %}
                            <a href="/remove_favorite/{{ coin.id }}" class="btn btn-sm btn-danger">Remove Favorite</a>
                        {% else %}
                            <a href="/add_favorite/{{ coin.id }}" class="btn btn-sm btn-success">Add Favorite</a>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, cryptos=cryptos, favorites=favorites)

# Route: Add Favorite
@app.route('/add_favorite/<coin_id>')
def add_favorite(coin_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    if coin_id not in session['favorites']:
        session['favorites'].append(coin_id)
    return redirect(url_for('home'))

# Route: Remove Favorite
@app.route('/remove_favorite/<coin_id>')
def remove_favorite(coin_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    session['favorites'] = [c for c in session['favorites'] if c != coin_id]
    return redirect(url_for('home'))

# Route: View Favorites
@app.route('/favorites')
def view_favorites():
    if 'user' not in session:
        return redirect(url_for('login'))
    favorites = session.get('favorites', [])
    cryptos = get_top_cryptos()
    favorite_cryptos = [coin for coin in cryptos if coin['id'] in favorites]
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>💰 Favorite Coins 💰</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f8f9fa;
            }
            .coin-card {
                background: #fff;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                transition: transform 0.2s;
            }
            .coin-card:hover {
                transform: scale(1.02);
            }
        </style>
    </head>
    <body>
        <div class="container py-4">
            <h1 class="text-center mb-4">💰 Your Favorites 💰</h1>
            <div class="row">
                {% for coin in cryptos %}
                <div class="col-md-4 mb-4">
                    <div class="coin-card">
                        <img src="{{ coin.image }}" alt="{{ coin.name }}" height="50" class="mb-2">
                        <h5>{{ coin.name }}</h5>
                        <p>Price: ${% if coin.current_price is not none %}{{ '{:,.2f}'.format(coin.current_price) }}{% else %}N/A{% endif %}</p>
                        <a href="/remove_favorite/{{ coin.id }}" class="btn btn-danger btn-sm">Remove</a>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="text-center mt-4">
                <a href="/" class="btn btn-secondary">Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """, cryptos=favorite_cryptos)

# Route: Coin Details
@app.route('/coin/<coin_id>')
def coin_detail(coin_id):
    coin = get_coin_details(coin_id)
    coin_name = coin['name']
    coin_image = coin['image']['large']
    coin_current_price = coin['market_data']['current_price']['usd']
    coin_market_cap = coin['market_data']['market_cap']['usd']
    coin_24h_high = coin['market_data']['high_24h']['usd']
    coin_24h_low = coin['market_data']['low_24h']['usd']
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{coin_name} Details</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light text-dark">
        <div class="container py-5">
            <div class="card shadow p-4">
                <div class="text-center">
                    <img src="{coin_image}" alt="{coin_name}" height="100" class="mb-3">
                    <h2>{coin_name}</h2>
                    <p class="lead">Current Price: ${coin_current_price:,}</p>
                    <p>Market Cap: ${coin_market_cap:,}</p>
                    <p>24h High: ${coin_24h_high:,}</p>
                    <p>24h Low: ${coin_24h_low:,}</p>
                    <a href="/" class="btn btn-primary mt-3">Back to List</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
