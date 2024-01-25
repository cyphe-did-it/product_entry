import mysql.connector
from faker import Faker
import random


# create fake contents using faker:
fake = Faker()      # crate instance to generate fake data

# test data for product names and category:
products = {
    'laptop': 'Technology',
    'notebook': 'School Supplies',
    'sunglasses': 'Accessories',
    'toothbrush': 'Miscellaneous',
    'smartphone': 'Technology',
    'eraser': 'School Supplies',
    'bracelet': 'Accessories',
    'umbrella': 'Miscellaneous',
    'headphones': 'Technology',
    'pen': 'School Supplies',
    'wallet': 'Accessories',
    'candle': 'Miscellaneous',
    'camera': 'Technology',
    'folder': 'School Supplies',
    'hat': 'Accessories',
    'soap': 'Miscellaneous',
    'desktop computer': 'Technology',
    'scissors': 'School Supplies',
    'necklace': 'Accessories',
    'flashlight': 'Miscellaneous',
    'printer': 'Technology',
    'ruler': 'School Supplies',
    'watch': 'Accessories',
    'towel': 'Miscellaneous',
    'tablet': 'Technology',
    'calculator': 'School Supplies',
    'backpack': 'Accessories',
    'umbrella': 'Miscellaneous',
    'keyboard': 'Technology',
    'highlighter': 'School Supplies',
    'belt': 'Accessories',
    'mirror': 'Miscellaneous',
    'mouse': 'Technology',
    'glue stick': 'School Supplies',
    'sunglasses': 'Accessories',
    'hand sanitizer': 'Miscellaneous',
    'fitness tracker': 'Technology',
    'pencil case': 'School Supplies',
    'scarf': 'Accessories',
    'kitchen sponge': 'Miscellaneous',
    'wearable camera': 'Technology',
    'notebook paper': 'School Supplies',
    'hat': 'Accessories',
    'picture frame': 'Miscellaneous',
    'drones': 'Technology',
    'pencil sharpener': 'School Supplies',
    'gloves': 'Accessories',
    'keychain': 'Miscellaneous',
    'external hard drive': 'Technology',
    'index cards': 'School Supplies',
    'earrings': 'Accessories',
    'tissue paper': 'Miscellaneous',
    'virtual reality headset': 'Technology',
    'binders': 'School Supplies',
    'watch': 'Accessories',
    'dish rack': 'Miscellaneous',
    'robot vacuum': 'Technology',
    'ballpoint pen': 'School Supplies',
    'backpack': 'Accessories',
    'coasters': 'Miscellaneous',
    'fitness watch': 'Technology',
    'markers': 'School Supplies',
    'ring': 'Accessories',
    'lint roller': 'Miscellaneous',
    'wireless router': 'Technology',
    'planner': 'School Supplies',
    'sunglasses case': 'Accessories',
    'air freshener': 'Miscellaneous',
    'smartwatch': 'Technology',
    'whiteboard': 'School Supplies',
    'headphones case': 'Accessories',
    'coffee mug': 'Miscellaneous',
    'gaming console': 'Technology',
    'pencil holder': 'School Supplies',
    'scarf': 'Accessories',
    'wall clock': 'Miscellaneous',
    'portable charger': 'Technology',
    'notebook cover': 'School Supplies',
    'hairbrush': 'Accessories',
    'luggage tag': 'Miscellaneous',
    'digital camera': 'Technology',
    'stapler': 'School Supplies',
    'watch band': 'Accessories',
    'napkin holder': 'Miscellaneous',
    'wireless earbuds': 'Technology',
    'composition book': 'School Supplies',
    'tie': 'Accessories',
    'candle holder': 'Miscellaneous',
    'USB drive': 'Technology',
    'pencil grips': 'School Supplies',
    'glasses case': 'Accessories',
    'picture hanger': 'Miscellaneous',
    'graphic tablet': 'Technology',
    'sticky notes': 'School Supplies',
    'hat box': 'Accessories',
    'keyboard cover': 'Miscellaneous',
}

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
    cursor = database.cursor()  # like ... USE dbname;

    keys = list(products.keys())
    values = list(products.values())

    # generate and insert dummy data:
    # table: id, name, category, price
    for i in range(len(products)):
        # generate fake data:
        id = fake.unique.random_int(min=1, max=len(products))    # generate random for product ID
        name = keys[i]
        category = values[i]
        price = round(random.uniform(5.0, 1000.0), 2)   # generate random for prices

        # create prompt:
        insert_query = '''
            INSERT INTO products (id, name, category, price)
            VALUES (%s, %s, %s, %s)
        '''

        # insert:
        cursor.execute(insert_query, (id, name, category, price))
        
    database.commit()                   # after adding everything, commit. 


    print('Data has been added successfully.')

except mysql.connector.Error as err:
    print('Failed in creating database')