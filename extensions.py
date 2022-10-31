import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            base_tickr = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Введите число без пробелов.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_tickr}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[quote_ticker]) * float(amount)

        return total_base
