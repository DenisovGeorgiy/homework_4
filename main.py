import psycopg2
from pprint import pprint


def create_db(cur: object) -> object:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        lastname VARCHAR(30),
        email VARCHAR(254)
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone_numbers(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    return


def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phone_numbers CASCADE;
        """)


def insert_tel(cur, client_id, tel):
    cur.execute("""
        INSERT INTO phone_numbers(number, client_id)
        VALUES (%s, %s)
        """, (tel, client_id))
    return client_id


def insert_client(cur, name=None, surname=None, email=None, tel=None):
    cur.execute("""
        INSERT INTO clients(name, lastname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if tel is None:
        return id
    else:
        insert_tel(cur, id, tel)
        return id


def update_client(cur, id, name=None, surname=None, email=None):
    cur.execute("""
        SELECT * from clients
        WHERE id = %s
        """, (id, ))
    info = cur.fetchone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET name = %s, lastname = %s, email =%s 
        where id = %s
        """, (name, surname, email, id))
    return id


def delete_phone(cur, number):
    cur.execute("""
        DELETE FROM phone_numbers 
        WHERE number = %s
        """, (number, ))
    return number


def delete_client(cur, id):
    cur.execute("""
        DELETE FROM phone_numbers
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE FROM clients 
        WHERE id = %s
       """, (id,))
    return id


def find_client(cur, name=None, surname=None, email=None, tel=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone_numbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone_numbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number like %s
            """, (name, surname, email, tel))
    return cur.fetchall()


if __name__ == '__main__':
    conn = psycopg2.connect(database="netology_db", user="postgres", password="gosha23452453")
    with conn.cursor() as curs:
        create_db(curs)
        delete_db(curs)
        create_db(curs)
        print("БД создана")
        print("Добавлен клиент id: ",
              insert_client(curs, "Дмитрий", "Новиков", "letik23525@gmail.com"))
        print("Добавлен клиент id: ",
              insert_client(curs, "Валентин", "Демчук",
                            "tsetst43@mail.ru", 89162362346))
        print("Добавлен клиент id: ",
              insert_client(curs, "Гордон", "Рамзи",
                            "c0pu@outlook.com", 89987568052))
        print("Добавлен клиент id: ",
              insert_client(curs, "Владислав", "Дарвин",
                            "eyer4yeh46@mail.ru", 89458620988))
        print("Добавлена клиент id: ",
              insert_client(curs, "Вениамин", "Зеедорф",
                            "saetnheo552@ramble.ru"))
        print("Данные в таблицах")
        curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone_numbers p ON c.id = p.client_id
            ORDER by c.id
            """)
        pprint(curs.fetchall())
        print("Телефон добавлен клиенту id: ",
              insert_tel(curs, 1, 89877876543))
        print("Телефон добавлен клиенту id: ",
              insert_tel(curs, 2, 89621994802))

        print("Данные в таблицах")
        curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone_numbers p ON c.id = p.client_id
            ORDER by c.id
            """)
        pprint(curs.fetchall())
        print("Изменены данные клиента id: ",
              update_client(curs, 4, "Иван", None, 'jfdghd554@outlook.com'))
        print("Телефон удалён c номером: ",
              delete_phone(curs, '89987568052'))
        print("Данные в таблицах")
        curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone_numbers p ON c.id = p.client_id
            ORDER by c.id
            """)
        pprint(curs.fetchall())
        print("Клиент c id удалён: ",
              delete_client(curs, 2))
        curs.execute("""
                        SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                        LEFT JOIN phone_numbers p ON c.id = p.client_id
                        ORDER by c.id
                        """)
        pprint(curs.fetchall())
        print('Найден клиент по имени:')
        pprint(find_client(curs, 'Вениамин'))

        print('Найден клиент по email:')
        pprint(find_client(curs, None, None, "letik23525@gmail.com"))

        print('Найден клиент по имени, фамилии и email:')
        pprint(find_client(curs, "Гордон", "Рамзи",
                            "c0pu@outlook.com"))

        print('Найден клиент по имени, фамилии, телефону и email:')
        pprint(find_client(curs, 'Иван', 'Дарвин', 'jfdghd554@outlook.com', '89458620988'))

        print('Найден клиент по имени, фамилии, телефону:')
        pprint(find_client(curs, None, None, None, '89458620988'))