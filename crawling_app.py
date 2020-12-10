from db_controller import stock_db
from crawler import naver, daum
stock_db.create_tables()


naver.get_kospi_200_names_and_indexes()
indexes = stock_db.select_all_indexes()

