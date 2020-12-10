from crawler.common import *
from db_controller import stock_db

"""
id,date, fastening_time, fastening_price, " \
              "bid_price, ask_price, trading_volume
"""
def get_per_5_minutes_prices(index):
    # 1년 == 525600분
    # 1년 == 105,120개의 5분봉
    # 100년 == 10,512,000
    ###### 다음도 제한이 걸려 있다........ 최대 9일치.....

    url = "https://finance.daum.net/api/charts/A{}/5/minutes?limit=10512000&adjusted=true".format(index)
    headers = {
                    'Accept': 'application / json, text / plain, * / *',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'ko,ko-KR;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Cookie': '__T_=1; _ga=GA1.2.1299421046.1607615508; _gid=GA1.2.1738211097.1607615508; TIARA=fGqt5kbef7lgMA6HAX.4L.bPCUxlMhV.uZNN61F5tKirCdbHfI56lU4FoNtEq1QcugMy9d5-FEy8YTROfs7Nkw.j_sosPzRNosJ_wYvPtnc0; KAKAO_STOCK_RECENT=[%22A005930%22]; webid=f2fd3d86b61e4c8a9a495a6a3172ae28; webid_ts=1607615508973; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}]; KAKAO_STOCK_CHART_ENABLED_INDICATORS=[%22sma%22%2C%22column%22]; _dfs=M1RnaEJDVW1uU2lDM2ZkOVR6N05tQlRaZEJyLzJHaHYvenlkQ0dQaGgwRnlGWitUTkJnV3JvTTNRenBQVXlDVUVIVUhkNUV2Zkx1QmtWRElpSER1bVE9PS0tV0YrTUplYnBDejF3ZkVodHR3QWhTUT09--3c3c59765b6b57176929b5432c427de2fab24929; _gat_gtag_UA_128578811_1=1; _T_ANO=AP97Ql6fCj1m/udaJlSGCuQxRXfIj3mk5YFmRmATFysw1hW/yijMcAd+2EMJgDhERLqeCAQppTsCPgRBWfAxt1CfucxSY1RbfUlavRekbu+Q9I7dJkROdD2xRKnyZGntNGw/EdbWeILy8X7edWx57B/5/oOfHjsXEGrpnL4Oupd8dKUnRO3wF11/jezdn7ff2mtuPmDSp8hEw2fGErtgPsMlq9qIGuyv1dcSZavd+/o6U2ylHq8rFlUV7g7qBpeIYyzqlNgVfvTDKDYLG6zlduq0pk3/gMEO3CMrU/ZPzZch7pXnRvX6yAoVKsCI4LomWwKF2udxCRbPC9XH3Cw89Q==; webid_sync=1607616148333',
                    'dnt': '1',
                    'referer':'https://finance.daum.net/quotes/A{}'.format(index),
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch_cors': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    result = get_json_object(url, headers)
    dataset = result['data']

    dates = []
    fastening_times = []
    fastening_prices = []

    starting_prices = []
    high_prices = []
    low_prices = []

    trading_volumes = []
    for data in dataset:
        date = ''.join(data['date'].split("-"))
        dates.append(date)

        fastening_time = ''.join(data['candleTime'].split(" ")[1].split(":")[:2])
        fastening_times.append(fastening_time)

        trading_volume = data['candleAccTradeVolume']
        trading_volumes.append(int(trading_volume))
        fastening_price = data['tradePrice']
        fastening_prices.append(int(fastening_price))

        high_price = data["highPrice"]
        low_price = data["lowPrice"]

        high_prices.append(int(high_price))
        low_prices.append(int(low_price))

        start_price = data['openingPrice']
        starting_prices.append(int(start_price))

    stock_db.insert_timely_price(index, dates, fastening_times, fastening_prices, starting_prices,
                                 high_prices, low_prices, trading_volumes)



if __name__ == "__main__":
    get_per_5_minutes_prices("005930")