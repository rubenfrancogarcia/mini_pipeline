from db_utils import db_utils

def main(): 
    connection = db_utils().get_db_connection()
    if connection is None: 
        raise Exception("db connection failed")

    try: 
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("connected", cursor.fetchone())
        cursor.close()
    finally: 
        connection.close()

if __name__ == "__main__":
    main()