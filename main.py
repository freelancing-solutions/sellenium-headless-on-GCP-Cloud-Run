from flask import Flask, request, jsonify, render_template
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

from functions.parsers import login, parse_stock, parse_broker

app = Flask(__name__, template_folder='templates', static_folder='static')

# The following options are required to make headless Chrome
# work in a Docker container
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

# Initialize a new browser
browser = webdriver.Chrome(chrome_options=chrome_options)


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@app.route("/browse/<path:path>", methods=["POST", "GET"])
def browse(path: str):
    """
        parse_stock and parse_broker will return tables filled with parsed data
    :param path:
    :return:
    """
    if request.method == "POST":
        if path == "login":
            json_data = request.get_json()
            return login(json_data=json_data)

        elif path == "parse-stock":
            json_data = request.get_json()
            return parse_stock(json_data=json_data)

        elif path == "parse_broker":
            json_data = request.get_json()
            return parse_broker(json_data=json_data)
        else:
            return jsonify({'status': False, 'message': 'Bad Request'}), 500
