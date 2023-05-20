import configparser
import psycopg2

config = configparser.ConfigParser()
config.read("setting.ini")

user = config["DB"]["user"]
password = config["DB"]["password"]
host = config["DB"]["host"]
port = config["DB"]["port"]
database = config["DB"]["database"]

def connect_DB():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")
        return connection
    except (Exception) as error:
        print("Ошибка при работе с PostgreSQL", error)

def close_connection_DB(connection):
    if connection:
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")