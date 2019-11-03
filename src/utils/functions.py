import json
import urllib.parse
import webbrowser

import pandas as pd
import requests

from src.utils.config import config
from src.utils.dataframe import add_column_if_not_exists
from src.utils.dataframe import saltedge_columns
from src.utils.helper import saltedge


def validate_content(function_name, content):
    if "error" in content:
        error = content["error"]
        error_class = error["class"] if "class" in error else ""
        error_message = error["message"] if "message" in error else ""
        error_documentation = error["documentation_url"] if "documentation_url" in error else ""
        raise ValueError(
            "Error detected in {}. Details are as follows: Class - {}, Message - {}, Documentation - {}".format(
                function_name, error_class, error_message, error_documentation
            )
        )
    else:
        pass


def get_customer(name):
    r = requests.get(saltedge.customers_path, headers=config.headers)
    content = json.loads(r.content)
    validate_content("get_customer_information", content)
    assert r.status_code == 200
    data = content["data"]
    identifiers = [x["identifier"] for x in data]
    if name in identifiers:
        customer_id = [x["id"] for x in data if x["identifier"] == name][0]
        customer_secret = [x["secret"] for x in data if x["identifier"] == name][0]
    else:
        r = requests.post(saltedge.customers_path, headers=config.headers, data=saltedge.create_customer_data(name))
        content = json.loads(r.content)
        validate_content("get_customer_information", content)
        assert r.status_code == 200
        data = content["data"]
        customer_id = data["id"]
        customer_secret = data["secret"]
    return customer_id, customer_secret


def connect_session(customer_id):
    r = requests.post(
        saltedge.connect_session_path, headers=config.headers, data=saltedge.create_session_data(customer_id)
    )
    content = json.loads(r.content)
    validate_content("connect_session", content)
    assert r.status_code == 200
    data = content["data"]
    connect_url = data["connect_url"]
    webbrowser.open_new_tab(connect_url)


def get_connections(customer_id):
    r = requests.get(saltedge.connection_path, headers=config.headers, params={"customer_id": customer_id})
    content = json.loads(r.content)
    validate_content("get_connections", content)
    assert r.status_code == 200
    data = content["data"]
    if len(data) == 0:
        raise ValueError(
            "The Data under `get_connection` is empty. It might be because the `connect_session` procedure"
            " has failed"
        )
    elif len(data) > 1:
        raise NotImplementedError(
            "Multiple Connections Detected. The logic for mutliple connections have yet to be implemented"
        )
    else:
        connection_id = data[0]["id"]
        connection_info = data[0]
    return connection_id, connection_info


def get_accounts(connection_id):
    r = requests.get(saltedge.accounts_path, headers=config.headers, params={"connection_id": connection_id})
    content = json.loads(r.content)
    validate_content("get_accounts", content)
    assert r.status_code == 200
    data = content["data"]
    if len(data) == 0:
        raise ValueError(
            "The Data under `get_connection` is empty. It might be "
            "because the Bank connected does not contain any active accounts"
        )
    accounts_id = []
    accounts_info = []
    for account in data:
        accounts_id.append(account["id"])
        accounts_info.append(account)
    return accounts_id, accounts_info


def populate_transactions(r, transaction_df):
    content = json.loads(r.content)
    validate_content("get_transactions", content)
    assert r.status_code == 200
    data = content["data"]
    meta = content["meta"]
    if len(data) == 0:
        transaction_df = transaction_df[saltedge_columns]
        cont = False
        return transaction_df, meta, cont
    else:
        tmp_df = pd.DataFrame(data)
        tmp_df = add_column_if_not_exists(tmp_df, saltedge_columns)
        tmp_df["type"] = tmp_df["extra"].apply(lambda x: x["type"] if "type" in x else "")
        tmp_df["account_balance_snapshot"] = tmp_df["extra"].apply(
            lambda x: x["account_balance_snapshot"] if "account_balance_snapshot" in x else ""
        )
        tmp_df = tmp_df[saltedge_columns]
        transaction_df = transaction_df.append(tmp_df)
        transaction_df = transaction_df[saltedge_columns]
        cont = True
        return transaction_df, meta, cont


def get_transactions(connection_id, account_id):
    transaction_df = pd.DataFrame(columns=saltedge_columns)
    r = requests.get(
        saltedge.transactions_path,
        headers=config.headers,
        params={"connection_id": connection_id, "account_id": account_id},
    )
    transaction_df, meta, cont = populate_transactions(r, transaction_df)
    if not cont:
        return transaction_df.drop(columns="extra")
    while meta["next_page"] is not None:
        r = requests.get(urllib.parse.urljoin(saltedge.parent_path, meta["next_page"]), headers=config.headers)
        transaction_df, meta, cont = populate_transactions(r, transaction_df)
        if not cont:
            return transaction_df.drop(columns="extra")
    return transaction_df.drop(columns="extra")
