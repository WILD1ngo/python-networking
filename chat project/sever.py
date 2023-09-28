import socket
import select
import json
import threading

open_client_sockets = []
connected_clients = []

def start_server():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 82))
    server_socket.listen(5)

    open_client_sockets.append(server_socket)
    print("Server is running (Write 'help' to get help)")

    while True:
        rlist, _, _ = select.select(open_client_sockets, [], [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)
                print(f"New connection from {address}")
            else:
                rec = current_socket.recv(1024).decode('utf-8')
                if not rec:
                    print(f"Connection from {current_socket.getpeername()} closed")
                    current_socket.close()
                    open_client_sockets.remove(current_socket)
                else:
                    (name, msg, typ) = json.loads(rec)
                    if typ == 0:
                        print(name + " joined the server")
                        connected_clients.append({"socket": current_socket, "name": name, "muted": False, "admin": False})
                    elif typ == 1:
                        if not is_user_muted(name):
                            print(name + ": " + msg)
                            send_message([client["socket"] for client in connected_clients], json.dumps((name, msg, typ)))

def get_command():
    while True:
        command = input("Enter command ('help' for available commands): ")
        if command == "help":
            print("Available commands: 'kick', 'mute', 'exit', 'admin', 'is_muted' ")
        elif command == "exit":
            for client in connected_clients:
                client_socket = client["socket"]
                client_socket.close()
                open_client_sockets.remove(client_socket)
            break
        elif command == "kick":
            username = input("Enter username to kick: ")
            kick_user(username)
        elif command == "mute":
            username = input("Enter username to mute: ")
            mute_user(username)
        elif command == "admin":
            username = input("Enter username to promote to admin: ")
            Set_admin(username)
        elif command == "is_muted":
            username = input("Enter username to check if muted: ")
            print(is_user_muted(username))
        else:
            print("Invalid command. Use 'help' for available commands.")
def Set_admin(username):
    for client in connected_clients:
        if client["name"] == username:
            client["admin"] = True
            print(f"{username} has been premoted to admin.")
def send_message(client_sockets, message):
    for client_socket in client_sockets:
        client_socket.send(message.encode('utf-8'))

def is_user_muted(username):
    for client in connected_clients:
        if client["name"] == username:
            return client["muted"]
    return False

def kick_user(username):
    for client in connected_clients:
        if client["name"] == username:
            client_socket = client["socket"]
            client_socket.close()
            open_client_sockets.remove(client_socket)
            connected_clients.remove(client)
            print(f"{username} has been kicked from the server.")

def mute_user(username):
    for client in connected_clients:
        if client["name"] == username:
            client["muted"] = not client["muted"]
            print(f"{username} has been muted/unmuted.")

if __name__ == "__main__":
    t1 = threading.Thread(target=start_server)
    t2 = threading.Thread(target=get_command)
    t1.start()
    t2.start()
