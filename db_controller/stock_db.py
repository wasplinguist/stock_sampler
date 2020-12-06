import pymysql
from pymysqlpool.pool import Pool


HOSTNAME = "localhost"
PORT     = 3306
USERNAME = "root"
PASSWORD = "12341234"
DATABASE = "stock"
CHARSET  = "utf8mb4"

pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, password=PASSWORD, db=DATABASE, charset=CHARSET, autocommit=True)
pool.init()

def insert_indexes_and_names(names, indexes, category=None, use=True):

    connection = pool.get_conn()
    cur = connection.cursor()

    command = "INSERT IGNORE INTO index_and_name (`id`, `name`, `category`, `use`) VALUES (%s, %s, %s, %s);"

    for i in range(len(names)):
        cur.execute(command, (indexes[i], names[i], category, use))

    pool.release(connection)
    print("Insert {} Success!".format("index_and_name"))


def insert_daily_price(index, dates, closing_prices, starting_prices, high_prices, low_prices, trading_volumes):

    command = "INSERT IGNORE INTO daily_price (id, date, closing_price, " \
              "starting_price, high_price, low_price, trading_volume)" \
              " VALUES "
    query_arr = []
    for i in range(len(dates)):
        query_arr.append(f"('{index}', '{dates[i]}', {closing_prices[i]}, {starting_prices[i]}, {high_prices[i]}, {low_prices[i]}, "
                         f"{trading_volumes[i]})")

    connection = pool.get_conn()
    cur = connection.cursor()
    command += ", ".join(query_arr)

    cur.execute(command)
    pool.release(connection)

    print("Insert {} to daily_price Success!".format(index))

def insert_hourly_price(index, fastening_times, fastening_prices, bid_prices, ask_prices, trading_volumes):

    command = "INSERT IGNORE INTO hourly_price (id, fastening_time, fastening_price, " \
              "bid_price, ask_price, trading_volume) VALUES "

    query_arr = []
    for i in range(len(fastening_times)):
        query_arr.append(f"('{index}', '{fastening_times[i]}', {fastening_prices[i]},"
                         f"{bid_prices[i]}, {ask_prices[i]}, {trading_volumes[i]})")

    connection = pool.get_conn()
    cur = connection.cursor()
    command += ", ".join(query_arr)

    cur.execute(command)
    pool.release(connection)

    print("Insert {} to hourly_price Success!".format(index))

def select_latest_end_date(index):

    command = "SELECT `date` FROM daily_price WHERE `id`=%s ORDER BY `date` DESC LIMIT 1;" %index

    connection = pool.get_conn()
    cur = connection.cursor()
    cur.execute(command)
    result = cur.fetchall()
    pool.release(connection)

    if len(result) == 0:
        return None
    return result[0]['date']

def get_all_dates(index):

    command = "SELECT `date` FROM daily_price WHERE `id`=%s ORDER BY `date` DESC;" %index

    connection = pool.get_conn()
    cur = connection.cursor()
    cur.execute(command)
    result = cur.fetchall()
    pool.release(connection)

    if len(result) == 0:
        return None

    date_list = []
    for data in result:
        date_list.append(data['date'])

    return date_list


def select_latest_end_hour(index):

    command = "SELECT `fastening_time` FROM hourly_price WHERE `id`=%s ORDER BY `fastening_time` DESC LIMIT 1;" %index

    connection = pool.get_conn()
    cur = connection.cursor()
    cur.execute(command)
    result = cur.fetchall()
    pool.release(connection)

    if len(result) == 0:
        return None
    return result[0]['fastening_time']

