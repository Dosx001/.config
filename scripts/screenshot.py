#!/usr/bin/env python

import json
import os
import re
import socket
import subprocess


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    s.send(b"client")
    buf = s.recv(1)
    if buf == b"0":
        print("server not found")
        return
    s.send(b'{"type":"current"}')
    buf = s.recv(1024)
    url: str = json.loads(buf.decode())["payload"]
    if re.search("crunchyroll.com/watch", url):
        s.send(b'{"type":"text","query":".show-title-link"}')
        buf = s.recv(1024)
        title = json.loads(buf.decode())["payload"]
        s.send(b'{"type":"text","query":"h1"}')
        buf = s.recv(1024)
        maim(
            title,
            json.loads(buf.decode())["payload"].split("-")[0].lstrip("E"),
        )
    elif re.search("hidive.com/video", url):
        s.send(
            b'{"type":"property",'
            b'"query":"meta[property=\'og:title\']",'
            b'"prop":"content"}'
        )
        buf = s.recv(1024)
        title = json.loads(buf.decode("utf-8"))["payload"]
        s.send(b'{"type":"text","query":".player-title"}')
        buf = s.recv(1024)
        maim(title, json.loads(buf.decode())["payload"].split()[0].lstrip("E"))
    else:
        with subprocess.Popen(
            ["ps", "-AF"],
            stdout=subprocess.PIPE,
            text=True,
        ) as ps:
            with subprocess.Popen(
                ["rg", "-e", "mpv", "-e", "Games"],
                stdin=ps.stdout,
                stdout=subprocess.PIPE,
                text=True,
            ) as rg:
                stdout, _ = rg.communicate()
                out = stdout.split("\n")
                if len(out) == 2:
                    spectacle("other")
                    return
                if re.search(r"mpv", out[0]):
                    title = (
                        re.search(r"Anime\/.*\/", out[0].split("--")[-1])
                        .group(0)
                        .split("/")[1]
                    )
                    match = re.search(r"S\d+E\d+", out[0])
                    if match:
                        maim(title, match[0].split("E")[1])
                    else:
                        maim(title, re.search(r"- \d+", out[0]).group(0).lstrip("- "))
                elif re.search(r"Games", out[0]):
                    title = re.search(r"[\w\s-]+/drive_c", out[0]).group(0)
                    title = title.split("/")[:-1]
                    spectacle("games/" + "_".join(title))
    s.close()


def maim(title: str, ep: str):
    path = "/home/dosx/Pictures/anime/" + title + "/" + ep + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    subprocess.call(
        [
            "maim",
            "-g",
            "2560x1440+1280+0",
            f"{path}{len(os.listdir(path))}.png",
        ]
    )


def spectacle(folder: str):
    path = "/home/dosx/Pictures/" + folder + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    subprocess.call(["spectacle", "-bo", f"{path}{len(os.listdir(path))}.png"])


if __name__ == "__main__":
    main()
