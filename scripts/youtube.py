#!/usr/bin/env python

import json
import socket
import subprocess


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    s.send(b"client\n")
    buf = s.recv(1)
    if buf == b"0":
        print("server not found")
        return
    s.send(b'{"type":"current"}\n')
    buf = s.recv(1024)
    subprocess.call(["mpv", json.loads(buf.decode("utf-8"))["payload"]])
    s.close()


if __name__ == "__main__":
    main()
