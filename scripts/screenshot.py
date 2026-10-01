#!/bin/python

import json
import os
import re
import socket
import subprocess
import urllib.request
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8080))
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
        title = s.recv(1024)
        s.send(b'{"type":"text","query":"h1"}')
        buf = s.recv(1024)
        s.close()
        maim(
            json.loads(title.decode())["payload"],
            json.loads(buf.decode())["payload"].split("-")[0].lstrip("E"),
        )
    elif re.search("hidive.com/video", url):
        s.send(b'{"type":"text","query":".player-title"}')
        buf = s.recv(1024)
        s.close()
        with urllib.request.urlopen(
            urllib.request.Request(
                f"https://www.hidive.com/season/{
                    parse_qs(urlparse(url).query)['seasonId'][0]
                }"
            ),
            timeout=10,
        ) as response:
            html = response.read().decode()
        parser = MetadataParser()
        parser.feed(html)
        maim(
            "-".join(parser.title.split("-")[:-1]),
            json.loads(buf.decode())["payload"].split()[0].lstrip("E"),
        )
    else:
        s.close()
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


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.title = data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False


if __name__ == "__main__":
    main()
