#!/bin/python

import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8080))
    s.send(b"client")
    buf = s.recv(1)
    if buf == b"0":
        print("server not found")
        return
    s.send(b'{"type":"reload","tab":{"title":"/*"}}')
    buf = s.recv(1024)
    print(buf.decode("utf-8"))
    s.close()


if __name__ == "__main__":
    main()
