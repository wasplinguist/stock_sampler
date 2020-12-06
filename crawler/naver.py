import requests
from bs4 import BeautifulSoup
import pandas as pd
from db_controller import stock_db
import tqdm
import datetime
import locale

locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')


def get_bs_obj(url):

    result = requests.get(url)
    return BeautifulSoup(result.content, "html.parser")

def get_last_page_num(bs_obj):

    table_navi = bs_obj.find("table", class_="Nnavi")
    td_last_page = table_navi.find("td", class_="pgRR")
    last_page = td_last_page.a.get('href').rsplit("&")[1]
    last_page = last_page.split("=")[1]
    last_page = int(last_page)
    return last_page

def get_kospi_200_names_and_indexes():

    indexes = []
    names = []

    url = "https://finance.naver.com/sise/entryJongmok.nhn?code=KPI200&page={}"
    bs_obj = get_bs_obj(url.format("1"))

    last_page_num = get_last_page_num(bs_obj)
    print("page: {}-{}".format(1, last_page_num))

    for i in range(1, last_page_num+1, 1):
        bs_obj = get_bs_obj(url.format(i))
        td_obj = bs_obj.find_all("td", class_="ctg")

        for td in td_obj:
            name = td.a.text
            if name == "":
                continue
            names.append(name)
            index = td.a.get("href").rsplit("=")[1]
            indexes.append(index)
            print("{} - {}: {}".format(i, name, index))
    print("size of indexes: {}".format(len(indexes)))
    stock_db.insert_indexes_and_names(names, indexes, "KOSPI200", True)


def get_daily_prices(index):

    print("get {} stock daily prices".format(index))
    url = "https://finance.naver.com/item/sise_day.nhn?code={}".format(index)
    url += "&page={}"
    bs_obj = get_bs_obj(url.format(1))

    last_page_num = get_last_page_num(bs_obj)
    print("page: {}-{}".format(1, last_page_num))

    dates = []
    closing_prices = []
    starting_prices = []
    high_prices = []
    low_prices = []
    trading_volumes = []

    latest_date = stock_db.select_latest_end_date(index)
    done = False
    for i in tqdm.tqdm(range(1, last_page_num+1, 1)):
        bs_obj = get_bs_obj(url.format(i))
        table = bs_obj.find("table", class_="type2")
        trs = table.find_all("tr")
        for i in range(2, len(trs), 1):
            tds = trs[i].find_all("td")
            datetime = tds[0].span
            if datetime is None:
                continue
            datetime = datetime.text

            if latest_date is not None and datetime == latest_date:
                done=True
                break

            dates.append(datetime)

            closing_price = tds[1].span.text
            closing_price="".join(closing_price.split(","))
            closing_prices.append(int(closing_price))

            starting_price = tds[3].span.text
            starting_price = "".join(starting_price.split(","))
            starting_prices.append(int(starting_price))

            high_price = tds[4].span.text
            high_price = "".join(high_price.split(","))
            high_prices.append(int(high_price))

            low_price = tds[5].span.text
            low_price = "".join(low_price.split(","))
            low_prices.append(int(low_price))

            trading_volume = tds[6].span.text
            trading_volume = "".join(trading_volume.split(","))
            trading_volumes.append(int(trading_volume))

        if done:
            break

    print("get {} days data".format(len(dates)))
    stock_db.insert_daily_price(index, dates, closing_prices, starting_prices, high_prices, low_prices, trading_volumes)


def get_available_date(date_string):

    # 기준 날짜 하루 전 평일 구하

    today = datetime.datetime.strptime(date_string, "%Y.%m.%d")
    day = today.strftime("%A")

    if day == "일요일":
        today = today-datetime.timedelta(days=2)
    elif day == "월요일":
        today = today-datetime.timedelta(days=3)
    else:
        today = today-datetime.timedelta(days=1)

    return today.strftime("%Y%m%d")+"1530"


def get_hourly_prices(index):
    # 하루 전 기준 데이터 받아오

    print("get {} stock hourly prices".format(index))

    # 마지막으로 저장된 날짜
    latest_hour = stock_db.select_latest_end_hour(index)

    url = f"https://finance.naver.com/item/sise_time.nhn?code={index}&thistime="
    url += "{}&page={}"

    fastening_times = []
    fastening_prices = []
    bid_prices = []
    ask_prices = []
    trading_volumes = []

    all_dates = stock_db.get_all_dates(index)

    done = False
    for date in all_dates:
        print("date: {}".format(date))
        timestamp = "".join(date.split("."))+"1530"

        bs_obj = get_bs_obj(url.format(timestamp, 1))

        last_page_num = get_last_page_num(bs_obj)
        print("page: {}-{}".format(1, last_page_num))

        for i in tqdm.tqdm(range(1, last_page_num+1, 1)):

            bs_obj = get_bs_obj(url.format(timestamp, i))
            table = bs_obj.find("table", class_="type2")
            trs = table.find_all("tr")
            for i in range(2, len(trs), 1):
                tds = trs[i].find_all("td")

                fastening_time = tds[0].span

                if fastening_time is None:
                    continue

                fastening_time = fastening_time.text
                fastening_time = ".".join(fastening_time.split(":"))
                fastening_time = f"{date}.{fastening_time}"

                if latest_hour is not None and fastening_time == latest_hour:
                    done = True
                    break

                fastening_times.append(fastening_time)

                fastening_price = tds[1].span.text
                fastening_price="".join(fastening_price.split(","))
                fastening_prices.append(int(fastening_price))

                bid_price = tds[3].span.text
                bid_price="".join(bid_price.split(","))
                bid_prices.append(int(bid_price))

                ask_price = tds[4].span.text
                ask_price="".join(ask_price.split(","))
                ask_prices.append(int(ask_price))

                trading_volume = tds[5].span.text
                trading_volume="".join(trading_volume.split(","))
                trading_volumes.append(int(trading_volume))

        if done:
            break

        stock_db.insert_hourly_price(index, fastening_times, fastening_prices, bid_prices, ask_prices, trading_volumes)
        fastening_times = []
        fastening_prices = []
        bid_prices = []
        ask_prices = []
        trading_volumes = []

    print("get {} days data".format(len(all_dates)))




if __name__ == "__main__":

    # get_kospi_200_names_and_indexes()
    # get_daily_prices("005930")
    # get_hourly_prices("005930")
    # get_available_date("2020.12.05")
    get_hourly_prices("005930")