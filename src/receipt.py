import json


class ReceiptFactory:
    class Receipt:
        def __init__(self, conf, customer):
            self.conf = conf
            self.customer = customer
        
        def get_name(self):
            return self.conf["item"]["description"]
        
        def get_description(self):
            return self.conf["description"]
        
        def get_currency(self):
            return self.conf["item"]["amount"]["currency"]
        
        def get_amount(self):
            return self.conf["item"]["amount"]["value"]
        
        def get_provider_data(self):
            provider_data = {
                "receipt": {
                    "customer": self.customer,
                    "items": [self.conf["item"]]
                }
            }
            return json.dumps(provider_data)

    def __init__(self, conf_file_path, customer_file_path):
        with open(conf_file_path, "r") as conf_file:
            self.conf = json.loads(conf_file.read())
        with open(customer_file_path, "r") as file:
            self.customer = json.loads(file.read())

    def get_receipt(self, id):
        conf = self.conf.get(id)
        if conf is None:
            raise AttributeError
        return self.Receipt(conf, self.customer)
