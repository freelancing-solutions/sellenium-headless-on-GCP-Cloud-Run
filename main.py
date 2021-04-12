import os
from flask import Flask, request, jsonify, render_template
from config import Config
chrome_app = Flask(__name__, template_folder='templates', static_folder='static')
chrome_app.config.from_object(Config)

with chrome_app.app_context():
    # Initialize a new browser
    from scrapper.scrapper import Scrapper
    scrapper_instance = Scrapper.init_app()


@chrome_app.route("/", methods=["GET"])
def home() -> tuple:
    return render_template('index.html'), 200


@chrome_app.route("/browse/<path:path>", methods=["POST", "GET"])
def browse(path: str) -> tuple:
    """
        parse_stock and parse_broker will return tables filled with parsed data
        :param path:
        :return:
    """
    if request.method == "POST":
        if path == "login":
            json_data: dict = request.get_json()
            return scrapper_instance.login(json_data=json_data)

        elif path == "parse-stock":
            json_data: dict = request.get_json()
            return scrapper_instance.scrapper_stock(json_data=json_data)

        elif path == "parse_broker":
            json_data: dict = request.get_json()
            return scrapper_instance.scrapper_broker(json_data=json_data)
        else:
            return jsonify({'status': False, 'message': 'Bad Request'}), 500


if __name__ == "__main__":
    chrome_app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8082)))
