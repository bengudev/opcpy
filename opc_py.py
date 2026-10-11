import socket
import threading
from threading import Semaphore

def port_checker():

    mode = input("Enter mode: ")

    if mode == "1":
        ip = input("Enter IP: ")
        port = int(input("Enter port: "))

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            print(port, " is open")
            s.close()
        except(socket.timeout, ConnectionRefusedError, OSError):
            print(" is closed")

    elif mode == "2":
        ip = input("Enter IP: ")
        semaphore = threading.Semaphore(100)
        def scan(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect((ip, port))
                print(port, " is open")
                s.close()
            except (socket.timeout, ConnectionRefusedError, OSError):
                pass
            finally:
                semaphore.release()
    try:
        threads = []
        for port in range(65536):
            semaphore.acquire()
            t = threading.Thread(target=scan, args=(port,), daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\nScan cancelled")

port_checker()