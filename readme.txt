Crypto Tracker Web App
This is a Crypto Tracker Web Application built using Flask, Python, and the CoinGecko API. It allows users to view live cryptocurrency prices, track their favorite coins, and explore detailed information about individual cryptocurrencies.

Features
Home Page: Displays a list of top 10 cryptocurrencies with their current prices and the option to view more details.

Coin Details: Shows detailed information for each coin, including its price, market cap, 24h high/low, and more.

User Authentication: Login system with a hardcoded user (for demonstration purposes).

Favorites: Users can add or remove cryptocurrencies from their favorites list.

Bootstrap Styling: The app is styled using Bootstrap for a clean and responsive design.

CoinGecko API: Fetches real-time cryptocurrency data from the CoinGecko API.

Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.6+

Flask

Requests library

Installation
1. Clone the Repository
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/crypto-tracker.git
cd crypto-tracker
2. Set up Virtual Environment
It is recommended to use a virtual environment to isolate dependencies. You can set up a virtual environment as follows:

bash
Copy code
python -m venv .venv
Activate the virtual environment:

Windows:

bash
Copy code
.\.venv\Scripts\activate
Mac/Linux:

bash
Copy code
source .venv/bin/activate
3. Install Dependencies
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
4. Running the Application
To run the app locally, use the following command:

bash
Copy code
python app.py
By default, the app will be accessible at:

cpp
Copy code
http://127.0.0.1:5000/
Usage
Login
The application includes a simple login form with the credentials:

Username: jimpinto

Password: jimpinto

After logging in, you will be able to see the list of cryptocurrencies and can add/remove them from your favorites.

Home Page
The home page displays the top 10 cryptocurrencies sorted by market cap.

You can see the price of each cryptocurrency in USD.

Each coin has a "Details" button that links to the coin’s detailed page with more information like market cap, 24h high/low, etc.

You can also add or remove coins from your favorites list.

Coin Details
Clicking on a coin from the home page takes you to the coin’s detail page.

It shows:

Current price

Market cap

24h high/low prices

Coin image and name

View Favorites
You can view your favorites list by clicking the "View Favorites" button in the navigation bar.

Logout
You can log out at any time using the "Logout" button.

Project Structure
bash
Copy code
/crypto-tracker
│
├── app.py                    # Main Flask app file
├── requirements.txt           # Python dependencies
├── templates/                 # Jinja templates (embedded in app.py)
├── .venv/                     # Virtual environment folder
└── README.md                  # Project README file
Dependencies
Flask: A lightweight WSGI web application framework for Python.

Requests: A simple HTTP library for Python to fetch data from the CoinGecko API.

Jinja2: Templating engine for Python used for rendering HTML with dynamic content.