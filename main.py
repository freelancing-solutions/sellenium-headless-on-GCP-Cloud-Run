from flask import Flask, request, jsonify, render_template
from scrapper.scrapper import Scrapper
from browser.browser import WebBrowser
chrome_app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize a new browser
browser_instance = WebBrowser().init_app(app=chrome_app)
scrapper_instance = Scrapper(app=chrome_app)


@chrome_app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@chrome_app.route("/browse/<path:path>", methods=["POST", "GET"])
def browse(path: str) -> tuple:
    """
        parse_stock and parse_broker will return tables filled with parsed data
    :param path:
    :return:
    """
    if request.method == "POST":
        if path == "login":
            json_data = request.get_json()
            return scrapper_instance.login(json_data=json_data)

        elif path == "parse-stock":
            json_data = request.get_json()
            return scrapper_instance.scrapper_stock(json_data=json_data)

        elif path == "parse_broker":
            json_data = request.get_json()
            return scrapper_instance.scrapper_broker(json_data=json_data)
        else:
            return jsonify({'status': False, 'message': 'Bad Request'}), 500
