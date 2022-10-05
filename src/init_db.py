import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="persons",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS persons;')
cur.execute('CREATE TABLE persons (id serial PRIMARY KEY,'
                                 'name varchar (100) NOT NULL,'
                                 'address varchar (200) NOT NULL,'
                                 'work varchar (200) NOT NULL,'
                                 'age integer NOT NULL,);'   
                                 )

cur.execute('INSERT INTO persons (name, address, work, age)'
            'VALUES (%s, %s, %s, %s)',
            ('Ivanov Ivan',
             'Moscow, Pervomayskaya street',
             'Sberbank',
             26)
            )

cur.execute('INSERT INTO persons (name, address, work, age)'
            'VALUES (%s, %s, %s, %s)',
            ('Petrov Petr',
             'Saint Petersburg, Noname street',
             'Tinkoff',
             35)
            )


conn.commit()

cur.close()
conn.close()