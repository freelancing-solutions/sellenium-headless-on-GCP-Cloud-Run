import datetime
from random import random
from flask import jsonify
from config import Config
from main import browser
from selenium.webdriver.support.ui import Select


def login(json_data: dict) -> tuple:

    implicit_wait_time: int = 10
    input_class: str = "form-control ng-pristine ng-empty ng-invalid ng-invalid-required ng-valid-maxlength ng-touched"
    login_button_class: str = "btn btn-lg btn-block investa-login--btn-login btn-investa__medium--blue btn-investa__medium"

    if "username" in json_data and json_data['username'] != "":
        username = json_data.get("username")
    else:
        username = Config.DEFAULT_USERNAME

    if "password" in json_data and json_data['password'] != "":
        password = json_data.get('password')
    else:
        password = Config.DEFAULT_PASSWORD

    if 'site_url' in json_data and json_data['site_url'] != "":
        site_url = json_data.get('site_url')
    else:
        site_url = Config.INVESTAGRAM_HOME_URI

    go_to_url = site_url

    browser.get(url=go_to_url)
    browser.implicitly_wait(time_to_wait=random(implicit_wait_time))
    browser.find_element_by_class_name(name='btn-login').click()
    browser.implicitly_wait(time_to_wait=random(implicit_wait_time))
    input_elements = browser.find_elements_by_class_name(name=input_class)
    if len(input_elements) > 1:
        input_elements[0].send_keys(value=username)
        browser.implicitly_wait(time_to_wait=random(implicit_wait_time))
        input_elements[1].send_keys(value=password)
        browser.implicitly_wait(time_to_wait=random(implicit_wait_time))
        browser.find_element_by_id('rememberMeChkbox').click()
        browser.implicitly_wait(time_to_wait=random(implicit_wait_time))
        browser.find_element_by_class_name(login_button_class).click()
        browser.implicitly_wait(time_to_wait=random(implicit_wait_time))
        # login here
        return jsonify({'status': True, 'message': 'successfully logged in'}), 200


def parse_stock(json_data: dict) -> tuple:
    wait: int = 10
    search_stock_input_class: str = "form-control ng-pristine ng-valid ng-empty ng-touched"
    search_button_class: str = "btn btn-outline-secondary"
    stock_broker_toggle_selected: str = "btn btn-outline-info jockeyDashboard__btn active"
    stock_broker_toggle: str = "btn btn-outline-info jockeyDashboard__btn"
    select_date_range_class: str = "form-control ng-valid ng-not-empty ng-dirty ng-touched ng-valid-parse"

    if "url" in json_data and json_data["url"] != "":
        url = json_data['url'] or "https://www.investagrams.com/StockJockey/"
    else:
        url = "https://www.investagrams.com/StockJockey/"

    if "symbol" in json_data and json_data["symbol"] != "":
        symbol = json_data['symbol']
    else:
        return jsonify({"status": False, "message": "symbol is required"}), 500

    if "broker_code" in json_data and json_data["broker_code"] != "":
        broker_code = json_data["broker_code"]

    if "from_date" in json_data and json_data['from_date'] != "":
        from_date = json_data['from_date']
    else:
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        from_date = "{}/{}/{}".format(year, month, day)
        #DEFAULT FORMAT = 2021/03/08

    if "to_date" in json_data and json_data['to_date'] != "":
        to_date = json_data["to_date"]
    else:
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        to_date = "{}/{}/{}".format(year, month, day)
        #DEFAULT FORMAT = 2021/03/08

    browser.get(url=url)
    browser.implicitly_wait(time_to_wait=random(random(wait)))
    #
    browser.find_element_by_class_name(name=search_stock_input_class).send_keys(value=symbol)
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # find the first search button and click
    browser.find_element_by_class_name(name=search_button_class).click()
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # selecting custom date range
    date_selector = browser.find_element_by_class_name(name=select_date_range_class)
    select = Select(date_selector)
    select.select_by_value(value=4)
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # Select custom date ranges
    from_to_inputs = browser.find_elements_by_css_selector(css_selector="input[type='text']")
    if len(from_to_inputs) > 1:
        from_to_inputs[0].send_keys(value=from_date)
        from_to_inputs[1].send_keys(value=to_date)

        apply_button = browser.find_element_by_class_name(name="w-100 btn btn-outline-secondary btn-sm ")
        apply_button.click()

        table = browser.find_element_by_tag_name(name="table")
        return jsonify({'status': True,
                        'payload': {'data': table},
                        'message': 'successfully fetched parsed data'}), 200

    return jsonify({'status': False, 'message': 'unable to locate data'}), 500


def parse_broker(json_data: dict) -> tuple:
    wait: int = 30
    search_stock_input_class: str = "form-control ng-pristine ng-valid ng-empty ng-touched"
    search_broker_input_class: str = "form-control ng-valid ng-touched ng-dirty ng-empty"
    search_button_class: str = "btn btn-outline-secondary"
    stock_broker_toggle_selected: str = "btn btn-outline-info jockeyDashboard__btn active"
    stock_broker_toggle: str = "btn btn-outline-info jockeyDashboard__btn"
    select_date_range_class: str = "form-control ng-valid ng-not-empty ng-dirty ng-touched ng-valid-parse"

    if "url" in json_data and json_data["url"] != "":
        url = json_data['url'] or "https://www.investagrams.com/StockJockey/"
    else:
        url = "https://www.investagrams.com/StockJockey/"

    if "symbol" in json_data and json_data["symbol"] != "":
        symbol = json_data['symbol']
    else:
        return jsonify({"status": False, "message": "symbol is required"}), 500

    if "broker_code" in json_data and json_data["broker_code"] != "":
        broker_code = json_data["broker_code"]
    else:
        return jsonify({"status": False, "message": "broker code is required"}), 500

    if "from_date" in json_data and json_data['from_date'] != "":
        from_date = json_data['from_date']
    else:
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        from_date = "{}/{}/{}".format(year, month, day)
        #DEFAULT FORMAT = 2021/03/08

    if "to_date" in json_data and json_data['to_date'] != "":
        to_date = json_data["to_date"]
    else:
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        to_date = "{}/{}/{}".format(year, month, day)
        #DEFAULT FORMAT = 2021/03/08

    browser.get(url=url)
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # Selecting broker search option
    browser.find_element_by_class_name(name=stock_broker_toggle).click()
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    #  Sending broker code to search options
    browser.find_element_by_class_name(name=search_broker_input_class).send_keys(value=broker_code)
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # find the first search button and click
    browser.find_element_by_class_name(name=search_button_class).click()
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # selecting custom date range
    date_selector = browser.find_element_by_class_name(name=select_date_range_class)
    select = Select(date_selector)
    select.select_by_value(value=4)
    browser.implicitly_wait(time_to_wait=random(random(wait)))

    # Select custom date ranges
    from_to_inputs = browser.find_elements_by_css_selector(css_selector="input[type='text']")
    if len(from_to_inputs) > 1:
        from_to_inputs[0].send_keys(value=from_date)
        from_to_inputs[1].send_keys(value=to_date)

        apply_button = browser.find_element_by_class_name(name="w-100 btn btn-outline-secondary btn-sm ")
        apply_button.click()

        table = browser.find_element_by_tag_name(name="table")
        return jsonify({'status': True,
                        'payload': {'data': table},
                        'message': 'successfully fetched parsed data'}), 200

    return jsonify({'status': False, 'message': 'unable to locate data'}), 500










