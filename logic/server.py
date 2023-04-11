import socket, threading
import psycopg2

connections = []


def db_connection():

    conn = psycopg2.connect(dbname='chat', user='postgres', password='777', host='127.0.0.1', port='6050')
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE chat")
        conn.commit()
        cursor.execute('DROP TABLE if exists users cascade;')
        conn.commit()
        cursor.execute('''CREATE TABLE users (id varchar(15) PRIMARY KEY, name varchar(10), password char(6));''')
        conn.commit()
        print('Успешно созданы юзеры')


        cursor.execute("CREATE TABLE msgs (id int PRIMARY KEY, users_id varchar(15) references users, info text);")
        conn.commit()
        print('Успешно созданы сообщения')
    except:
        print('все ок')


    cursor.close()
    conn.close()


def handle_user_connection(socket_connection, address):

    while True:
        try:
            msg = socket_connection.recv(1024)
            if msg:
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                # msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
            else:
                remove_connection(socket_connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(socket_connection)
            break


def remove_connection(conn):

    if conn in connections:
        conn.close()
        connections.remove(conn)


def server() -> None:
    global socket_instance
    LISTENING_PORT = 12040

    try:

        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')

        db_connection()

        while True:
            socket_connection, address = socket_instance.accept()
            connections.append(socket_instance)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()

    conn = psycopg2.connect(dbname='chat', user='postgres', password='777', host='127.0.0.1', port='6050')
    cursor = conn.cursor()
    cursor.execute('drop table if exists users cascade;')
    cursor.execute('drop table if exists msgs cascade;')
    cursor.close()
    conn.close()



if __name__ == "__main__":
    server()