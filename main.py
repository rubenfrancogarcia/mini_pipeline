from DBUtils import DBUtils
from CLIService import CLIService

def main():
    connection = DBUtils().get_db_connection()
    if connection is None: 
        raise Exception("db connection failed")

    try: 
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("connected", cursor.fetchone())
        DBUtils().load_third_party(connection, 'third_party_sales_1 - third_party_sales_1 (1).csv')
        cursor.close()
        CLIService().run_menu(connection)



    finally: 
        connection.close()

if __name__ == "__main__":
    main()