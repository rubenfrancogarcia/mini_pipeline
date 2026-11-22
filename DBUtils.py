import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
import csv 
import os 
from tickets import ticket
from pathlib import Path
from dotenv import load_dotenv

class DBUtils:
    load_dotenv()
    def get_db_connection(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_USER_PASSWORD"],
            port=3306,
            database=os.environ["MYSQL_DATABASE"],
        )
         

    def load_third_party(self, connection: PooledMySQLConnection, file_path_csv: str):
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS ticket (
                id INT,
                transaction_date INT, 
                event_id INT,
                event_name VARCHAR(100),
                event_date DATE,
                event_type VARCHAR(50),
                event_city VARCHAR(100),
                customer_id INT, 
                price DECIMAL(10, 2),
                num_tickets INT
            )""")
            cursor.execute("SELECT EXISTS (SELECT 1 FROM ticket)") 
            populated = bool(cursor.fetchone()[0])
            if not populated:
                print("populating db with csv data")
                with open(file_path_csv) as thirdPatryData:
                    reader = csv.reader(thirdPatryData)
                    for row in reader:
                        item = ticket.from_csv_row(row)
                        cursor.execute(self.insert_sql, (
                            item.id,
                            item.transaction_date,
                            item.event_id,
                            item.event_name,
                            item.event_date,
                            item.event_type,
                            item.event_city,
                            item.customer_id,
                            item.price,
                            item.num_tickets,
                        ))
                    connection.commit()
            else: 
                print("db already populated with csv data")
    insert_sql = """
        INSERT INTO ticket (
            id, transaction_date, event_id, event_name, event_date, event_type,
            event_city, customer_id, price, num_tickets
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """                      
    def _print_rows(self, cursor, empty_message="No results found."):
        rows = cursor.fetchall()
        if not rows:
            print(empty_message)
            return
        columns = cursor.column_names
        for row in rows:
            print(" | ".join(f"{col}: {val}" for col, val in zip(columns, row)))

    def _query(self, connection, sql, params=(), title=None, empty_message="No results found."):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, params)
            if title:
                print(title)
            self._print_rows(cursor, empty_message)
        finally:
            cursor.close()

    def find_by_most_tickets(self, connection: PooledMySQLConnection):
        self._query(connection,
            "SELECT event_name, num_tickets FROM ticket ORDER BY num_tickets DESC LIMIT 3",
            title="Events with the most tickets ordered:")

    def find_by_least_tickets(self, connection: PooledMySQLConnection):
        self._query(connection,
            "SELECT event_name, num_tickets FROM ticket ORDER BY num_tickets ASC LIMIT 3",
            title="Events with the least tickets ordered:")

    def return_all_results(self, connection: PooledMySQLConnection):
        self._query(connection, "SELECT * FROM ticket", title="All tickets:")

    def revenue_by_city(self, connection: PooledMySQLConnection):
        self._query(connection,
            "SELECT event_city, SUM(price * num_tickets) AS revenue FROM ticket GROUP BY event_city ORDER BY revenue DESC",
            title="Revenue by city:")

    def tickets_for_customer(self, connection: PooledMySQLConnection):
        try:
            customer_id = int(input("Customer id: "))
        except ValueError:
            print("Customer id must be a number.")
            return
        self._query(connection,
            "SELECT * FROM ticket WHERE customer_id = %s", (customer_id,),
            empty_message=f"No tickets found for customer {customer_id}.")

    if __name__ == "__db_utils__":
            print("setup") 