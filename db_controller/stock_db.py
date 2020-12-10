import pymysql
from pymysqlpool.pool import Pool


HOSTNAME = "localhost"
PORT     = 3306
USERNAME = "root"
DATABASE = "stock"
CHARSET  = "utf8mb4"


def create_tables():

    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

    connection = pool.get_conn()
    cur = connection.cursor()

    index_and_name = "CREATE TABLE IF NOT EXISTS index_and_name(" \
              "id VARCHAR(10) NOT NULL," \
              "name VARCHAR(100) NOT NULL," \
              "category VARCHAR(50) NOT NULL," \
              "use TINYINT(1) NOT NULL," \
              "CONSTRAINT index_and_name_PK PRIMARY KEY(id)" \
              ");"

    daily_price = "CREATE TABLE IF NOT EXISTS daily_price(" \
                  "id VARCHAR(10) NOT NULL," \
                  "date VARCHAR(8) NOT NULL," \
                  "closing_price INT NOT NULL," \
                  "starting_price INT NOT NULL," \
                  "high_price INT NOT NULL," \
                  "low_price INT NOT_NULL," \
                  "trading_volume INT NOT_NULL," \
                  "CONSTRAINT daily_price_PK PRIMARY KEY(id, date)" \
                  ");"

    hourly_price = "CREATE TABLE IF NOT EXISTS timely_price(" \
                   "id VARCHAR(10) NOT NULL," \
                   "date VARCHAR(8) NOT NULL," \
                   "fastening_time VARCHAR(4) NOT NULL," \
                   "fastening_price INT NOT NULL," \
                   "starting_price INT,"\
                   "high_price INT," \
                   "low_price INT," \
                   "trading_volume INT," \
                   "CONSTRAINT hourly_price_PK PRIMARY KEY(id, date, fastening_time)" \
                   ");"

    cur.execute(index_and_name)
    cur.execute(daily_price)
    cur.execute(hourly_price)
    print("CREATE TABLES !")


def insert_indexes_and_names(names, indexes, category=None, use=True):
    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

    connection = pool.get_conn()
    cur = connection.cursor()

    command = "INSERT IGNORE INTO index_and_name (`id`, `name`, `category`, `use`) VALUES (%s, %s, %s, %s);"

    for i in range(len(names)):
        cur.execute(command, (indexes[i], names[i], category, use))

    pool.release(connection)
    print("Insert {} Success!".format("index_and_name"))

def select_all_indexes():

    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

    connection = pool.get_conn()
    cur = connection.cursor()

    command = "SELECT `id` FROM index_and_name;"
    cur.execute(command)
    result = cur.fetchall()

    if len(result) == 0:
        return None

    index_list = []
    for data in result:
        index_list.append(data['id'])

    return index_list


def insert_daily_price(index, dates, closing_prices, starting_prices, high_prices, low_prices, trading_volumes):
    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

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


def select_latest_end_date(index):
    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

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
    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

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


def insert_timely_price(index, dates, fastening_times, fastening_prices, starting_prices, high_prices, low_prices, trading_volumes):

    pool = Pool(host=HOSTNAME, port=PORT, user=USERNAME, db=DATABASE, charset=CHARSET, autocommit=True)
    pool.init()

    command = "INSERT IGNORE INTO timely_price (id, date, fastening_time, fastening_price, starting_price," \
              "high_price, low_price, trading_volume) VALUES "

    query_arr = []
    for i in range(len(fastening_times)):
        query_arr.append(f"('{index}', '{dates[i]}', '{fastening_times[i]}', "
                         f"{fastening_prices[i]}, {starting_prices[i]}"
                         f"{high_prices[i]}, {low_prices[i]}, {trading_volumes[i]})")

    connection = pool.get_conn()
    cur = connection.cursor()
    command += ", ".join(query_arr)

    cur.execute(command)
    pool.release(connection)

    print("Insert {} to hourly_price Success!".format(index))

