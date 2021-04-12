import datetime
from random import random
from flask import jsonify
from main import browser_instance
from selenium.webdriver.support.ui import Select


class Scrapper:
    wait_time: int = 10
    login_input_class: str = "form-control ng-pristine ng-empty ng-invalid ng-invalid-required " \
                             "ng-valid-maxlength ng-touched"
    login_button_class: str = "btn btn-lg btn-block investa-login--btn-login btn-investa__medium--blue " \
                              "btn-investa__medium"
    remember_me_check: str = "rememberMeChkbox"
    scrappe_stock_uri: str = "https://www.investagrams.com/StockJockey/"
    logged_in: bool = False

    def __init__(self, app):
        self.username: str = app.config.DEFAULT_USERNAME
        self.password: str = app.config.DEFAULT_PASSWORD
        self.investagram_uri: str = app.config.INVESTAGRAM_HOME_URI
        self.login()

    def wait(self):
        browser_instance.implicitly_wait(time_to_wait=random(self.wait_time))

    @staticmethod
    def return_now_date() -> str:
        """

        :return: today date in string format
        """
        year: str = datetime.datetime.now().strftime("%Y")
        month: str = datetime.datetime.now().strftime("%m")
        day: str = datetime.datetime.now().strftime("%d")
        return "{}/{}/{}".format(year, month, day)
        # DEFAULT FORMAT = 2021/03/08

    def login(self, json_data: dict = None) -> tuple:
                k "username" in json_data and json_data['username'] != "":
            username: str = json_data.get("username")
        else:
            username: str = self.username

        if "password" in json_data and json_data['password'] != "":
            password: str = json_data.get('password')
        else:
            password: str = self.password

        if 'site_url' in json_data and json_data['site_url'] != "":
            site_url: str = json_data.get('site_url')
        else:
            site_url: str = self.investagram_uri

        browser_instance.get(url=site_url)
        self.wait()
        browser_instance.find_element_by_class_name(name='btn-login').click()
        input_elements = browser_instance.find_elements_by_class_name(name=self.login_input_class)
        if len(input_elements) > 1:
            input_elements[0].send_keys(value=username)
            input_elements[1].send_keys(value=password)
            self.wait()
            browser_instance.find_element_by_id(self.remember_me_check).click()
            browser_instance.find_element_by_class_name(self.login_button_class).click()
            self.wait()
            # login here
            self.logged_in = True
            return jsonify({'status': True, 'message': 'successfully logged in'}), 200
        return jsonify({'status': False, 'message': 'unable to login could not find login elements'}), 500

    def scrapper_stock(self, json_data: dict) -> tuple:
        search_stock_input_class: str = "form-control ng-pristine ng-valid ng-empty ng-touched"
        search_button_class: str = "btn btn-outline-secondary"
        select_date_range_class: str = "form-control ng-valid ng-not-empty ng-dirty ng-touched ng-valid-parse"

        if ("url" in json_data) and (json_data["url"] != "") and (json_data['url'] is not None):
            url: str = json_data.get('url')
        else:
            url: str = self.scrappe_stock_uri

        if ("symbol" in json_data) and (json_data["symbol"] != "") and (json_data['symbol'] is not None):
            symbol: str = json_data['symbol']
        else:
            return jsonify({"status": False, "message": "symbol is required"}), 500

        if "from_date" in json_data and json_data['from_date'] != "":
            from_date: str = json_data['from_date']
        else:
            from_date: str = self.return_now_date()

        if "to_date" in json_data and json_data['to_date'] != "":
            to_date: str = json_data["to_date"]
        else:
            to_date: str = self.return_now_date()

        browser_instance.get(url=url)
        self.wait()
        self.wait()
        #
        browser_instance.find_element_by_class_name(name=search_stock_input_class).send_keys(value=symbol)
        # find the first search button and click
        browser_instance.find_element_by_class_name(name=search_button_class).click()
        # selecting custom date range
        date_selector = browser_instance.find_element_by_class_name(name=select_date_range_class)
        select = Select(date_selector)
        select.select_by_value(value=4)
        self.wait()

        # Select custom date ranges
        from_to_inputs = browser_instance.find_elements_by_css_selector(css_selector="input[type='text']")
        if len(from_to_inputs) > 1:
            from_to_inputs[0].send_keys(value=from_date)
            from_to_inputs[1].send_keys(value=to_date)

            apply_button = browser_instance.find_element_by_class_name(name="w-100 btn btn-outline-secondary btn-sm ")
            apply_button.click()

            table = browser_instance.find_element_by_tag_name(name="table")
            return jsonify({'status': True,
                            'payload': {'data': table},
                            'message': 'successfully fetched parsed data'}), 200

        return jsonify({'status': False, 'message': 'unable to locate data'}), 500

    def scrapper_broker(self, json_data: dict) -> tuple:
        search_broker_input_class: str = "form-control ng-valid ng-touched ng-dirty ng-empty"
        search_button_class: str = "btn btn-outline-secondary"
        stock_broker_toggle: str = "btn btn-outline-info jockeyDashboard__btn"
        select_date_range_class: str = "form-control ng-valid ng-not-empty ng-dirty ng-touched ng-valid-parse"

        if ("url" in json_data) and (json_data["url"] != "") and (json_data["url"] is not None):
            url: str = json_data.get('url')
        else:
            url: str = self.scrappe_stock_uri

        if ("broker_code" in json_data) and (json_data["broker_code"] != "") and (json_data["broker_code"] is not None):
            broker_code: str = json_data.get("broker_code")
        else:
            return jsonify({"status": False, "message": "broker code is required"}), 500

        if ("from_date" in json_data) and (json_data['from_date'] != "") and (json_data['from_date'] is not None):
            from_date: str = json_data.get('from_date')
        else:
            from_date: str = self.return_now_date()

        if ("to_date" in json_data) and (json_data['to_date'] != "") and (json_data['to_date'] is not None):
            to_date: str = json_data.get("to_date")
        else:
            to_date: str = self.return_now_date()

        browser_instance.get(url=url)
        self.wait()

        # Selecting broker search option
        browser_instance.find_element_by_class_name(name=stock_broker_toggle).click()
        self.wait()

        #  Sending broker code to search options
        browser_instance.find_element_by_class_name(name=search_broker_input_class).send_keys(value=broker_code)
        self.wait()

        # find the first search button and click
        browser_instance.find_element_by_class_name(name=search_button_class).click()
        self.wait()

        # selecting custom date range
        date_selector = browser_instance.find_element_by_class_name(name=select_date_range_class)
        select = Select(date_selector)
        select.select_by_value(value=4)
        self.wait()

        # Select custom date ranges
        from_to_inputs = browser_instance.find_elements_by_css_selector(css_selector="input[type='text']")
        if len(from_to_inputs) > 1:
            from_to_inputs[0].send_keys(value=from_date)
            from_to_inputs[1].send_keys(value=to_date)

            apply_button = browser_instance.find_element_by_class_name(name="w-100 btn btn-outline-secondary btn-sm ")
            apply_button.click()

            # table element contains the returned data
            table = browser_instance.find_element_by_tag_name(name="table")
            return jsonify({'status': True,
                            'payload': {'data': table},
                            'message': 'successfully fetched parsed data'}), 200

        return jsonify({'status': False, 'message': 'unable to locate data'}), 500










