#!/usr/bin/env python
import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    s.send(b"client\n")
    buf = s.recv(1)
    if buf == b"0":
        print("server not found")
        return
    s.send(
        (
            b'{"type":"execute","frame":true,'
            b'"code":"{{const e=document.querySelector(\'canvas\');'
            b"if(e)e.style.display=e.style.display==='none'?'':'none';}}\"}\n"
        )
    )
    s.close()


if __name__ == "__main__":
    main()
