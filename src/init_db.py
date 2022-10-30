
import psycopg2

conn = psycopg2.connect(
        host="ec2-54-155-110-181.eu-west-1.compute.amazonaws.com",
        database="d3phv792lca812",
        user='jueeadhvgqftvn',
        password='b6fcbd3432d01827ecbe5845c3cfe62275cdd218e46a2f4d786c515fb702d66f')

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS persons;')
cur.execute('CREATE TABLE persons (id serial PRIMARY KEY,'
                                 'name varchar (100) NOT NULL,'
                                 'address varchar (200) NOT NULL,'
                                 'work varchar (200) NOT NULL,'
                                 'age integer NOT NULL);'   
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