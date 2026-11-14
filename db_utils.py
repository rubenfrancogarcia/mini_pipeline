import mysql.connector
import csv 
import os 
from pathlib import Path
from dotenv import load_dotenv

class db_utils:
    load_dotenv()
    def get_db_connection(self):
        connection = None
        try: 
            connection = mysql.connector.connect(host=os.getenv("DB_HOST", "127.0.0.1"), user= os.environ["MYSQL_USER"], password=os.environ["MYSQL_USER_PASSWORD"], port=3306, database=os.environ["MYSQL_DATABASE"])
        except Exception as error: 
            print("Error db connection", error)
        return connection

    def load_third_party(self, connection, file_path_csv):
            cursor = connection.cursor
            ##todo
            with open(file_path_csv) as thirdPatryData:
                 reader = csv.reader(thirdPatryData)
                 for row in reader: 
                      print(', '.join(row))
            connection.commit()
            cursor.close()
            return

    if __name__ == "__db_utils__":
            print("setup") 