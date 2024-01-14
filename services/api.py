import requests
from requests import Response
from config import Config


class DataProcessor:
    def __init__(self) -> None:
        self.token = Config().get_api_token()
        self.base_url = "https://fbtool.pro/api"

    def get_response(self, acc_id: int):
        url = f"{self.base_url}/get-statistics?key={self.token}&account={acc_id}&mode=adsets"
        response = requests.get(url)
        print(response.text)
        return response

    def get_spend_by_name(self, target_name: str, response: Response):
        if response.status_code == 200:
            data = response.json()

            for account in data.get("data", []):
                for adset in account.get("adsets", {}).get("data", []):
                    if adset.get("name") == target_name:
                        return adset.get("insights", {}).get("data", [{}])[0].get("spend")
        return None

    def get_all_accounts(self):
        url = f"{self.base_url}/get-accounts?key={self.token}&account=17233976"
        response = requests.get(url)
        data = response.json()
        ids = [item['id'] for item in data.values() if isinstance(item, dict) and 'id' in item]
        return ids