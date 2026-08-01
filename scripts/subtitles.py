#!/usr/bin/env python
import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    s.send(b"client")
    buf = s.recv(1)
    if buf == b"0":
        print("server not found")
        return
    s.send(
        (
            b'{"type":"execute",'
            b'"code":"{{const s=document.querySelector(\'canvas\').style;'
            b"if(s)s.display=s.display==='none'?'':'none';}}\"}"
        )
    )
    s.recv(1)
    s.close()


if __name__ == "__main__":
    main()
