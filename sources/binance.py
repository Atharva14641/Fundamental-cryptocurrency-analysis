import logging
log = logging.getLogger('binance')

from datetime import datetime, timedelta

from sources.exchange import Exchange


class Binance(Exchange):
    URL_PRICES = "https://api.binance.com/api/v3/ticker/price"
    URL_PRICE = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT"

    @classmethod
    def prices(cls):
        data = cls.request(cls.URL_PRICES)
        return {sp['symbol'][:-4]: float(sp['price']) for sp in data if sp['symbol'].endswith("USDT")}

    @classmethod
    def price(cls, sym):
        data = cls.request(cls.URL_PRICE.format(sym))
        assert data['symbol'] == f'{sym}USDT'
        return float(data['price'])

    @classmethod
    def klines(cls, sym):
        data = cls.request("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000")
        ret = []
        for item in data:
            ret.append({
                'time': datetime.fromtimestamp(item[0] / 1000),
                'open': float(item[1]),
                'high': float(item[2]),
                'low': float(item[3]),
                'close': float(item[4]),
            })
        return ret


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    Binance.test()