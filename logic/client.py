import socket, threading
import psycopg2

registered = []


def db_connection():
    conn = psycopg2.connect(dbname='chat', user='postgres', password='777', host='127.0.0.1', port='6050')
    cursor = conn.cursor()
    cursor.close()
    conn.close()

def handle_messages(connection):

    while True:
        try:
            msg = connection.recv(1024)

            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break


def sign_up():
    print('Hi there! Please fill in the info about you')
    usr_id = input('Enter your unique id, so others can find you by it: ')
    usr_name = input('Enter your name, so others will see who sends messages: ')
    usr_pswd = input('Enter your password (6 characters): ')
    conn = psycopg2.connect(dbname='chat', user='postgres', password='777', host='127.0.0.1', port='6050')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (id, name, password) VALUES ({usr_id}, {usr_name}, {usr_pswd});")
    conn.commit()
    cursor.close()
    conn.close()


def sign_in():
    usr_id = input('Nickname: ')
    usr_psswd = input('Password: ')
    conn = psycopg2.connect(dbname='chat', user='postgres', password='777', host='127.0.0.1', port='6050')
    cursor = conn.cursor()
    if usr_id in cursor.execute("SELECT id FROM users"):
        if usr_psswd == cursor.execute(f"SELECT password FROM users WHERE id = {usr_id}"):
            conn.commit()
            pass
    else:
        print('Invalid id or password')
    cursor.close()
    conn.close()

def client():

    global socket_instance
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12040

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        threading.Thread(target=handle_messages, args=[socket_instance]).start()


        if not socket_instance in registered:
            sign_up()
        else:
            sign_in()

        print('Connected to chat!')


        while True:
            msg = input()
            if msg == 'quit':
                break
            socket_instance.send(msg.encode())

        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()