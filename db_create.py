<<<<<<< HEAD
# code to create database schema:
import mysql.connector

try:
    # configure connection: 
    config = {
        'user': 'root',
        'passwd': 'yourpassword',
        'host': 'localhost',
        'port': 3306,
        'database': 'store'    
    }   

    # connect:
    database = mysql.connector.connect(**config)
    # set cursor:
    cursor = database.cursor() 

    # create database:
    create_db = "CREATE DATABASE IF NOT EXISTS store;"
    cursor.execute(create_db)           # execute
    database.commit()

    # create prompt:
    create_products_table = '''
       CREATE TABLE IF NOT EXISTS products (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            removed INT NOT NULL DEFAULT 0
        );
    '''
    cursor.execute(create_products_table) # execute prompts

    database.commit()                       # saves all execution 
    print('Table has been created successfully.')

except mysql.connector.Error as err:
    print('Problem with database connection.')
    print('Error is: ', err)

=======
# code to create database schema:
import mysql.connector

try:
    # configure connection: 
    config = {
        'user': 'root',
        'passwd': 'yourpassword',
        'host': 'localhost',
        'port': 3306,
        'database': 'store'    
    }   

    # connect:
    database = mysql.connector.connect(**config)
    # set cursor:
    cursor = database.cursor() 

    # create database:
    create_db = "CREATE DATABASE IF NOT EXISTS store;"
    cursor.execute(create_db)           # execute
    database.commit()

    # create prompt:
    create_products_table = '''
       CREATE TABLE IF NOT EXISTS products (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            removed INT NOT NULL DEFAULT 0
        );
    '''
    cursor.execute(create_products_table) # execute prompts

    database.commit()                       # saves all execution 
    print('Table has been created successfully.')

except mysql.connector.Error as err:
    print('Problem with database connection.')
    print('Error is: ', err)

>>>>>>> 827a3b7c1efbcce4396bb1fd2279080a6f3459ee
