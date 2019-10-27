import json


class SaltEdgeHelper:
    def __init__(self):
        self.parent_path = "https://www.saltedge.com/"
        self.customers_path = "https://www.saltedge.com/api/v5/customers"
        self.connect_session_path = "https://www.saltedge.com/api/v5/connect_sessions/create"
        self.connection_path = "https://www.saltedge.com/api/v5/connections"
        self.accounts_path = "https://www.saltedge.com/api/v5/accounts"
        self.transactions_path = "https://www.saltedge.com/api/v5/transactions"

    @staticmethod
    def create_customer_data(name):
        data = {"data": {"identifier": name}}
        return json.dumps(data)

    @staticmethod
    def create_session_data(customer_id):
        data = {
            "data": {"customer_id": customer_id, "consent": {"scopes": ["account_details", "transactions_details"]}}
        }
        return json.dumps(data)


saltedge = SaltEdgeHelper()
