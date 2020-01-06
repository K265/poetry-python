# -*- coding: utf-8 -*-
# env: Python 3.7
# 1/2/2020
# inspired by: https://github.com/okcy1016/poetry-desktop/

import ctypes
import random
import sys
from os import path, linesep, chdir
from subprocess import call

import requests
from requests import Session


# {'author': '...', 'paragraphs': [...], ?'rhythmic': '...', ?'title': '...', 'tags': [...]}
def get_poetry():
    urls = [
        # 0 ~ 57000
        f"https://raw.githubusercontent.com/chinese-poetry/chinese-poetry-zhCN/master/poetry/poet.tang.{random.randrange(58) * 1000}.json",
        # 0 ~ 254000
        # f"https://raw.githubusercontent.com/chinese-poetry/chinese-poetry-zhCN/master/poetry/poet.song.{random.randrange(255) * 1000}.json",
        # 0 ~ 21000
        # f"https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/ci/ci.song.{random.randrange(22) * 1000}.json"
    ]
    url = random.choice(urls)
    print(f"Fetching {url}")
    try:
        with Session() as s:
            res = s.get(url)
            json = res.json()
    except requests.exceptions.RequestException:
        print(f"Failed to fetch {url}")
        sys.exit(0)
    return random.choice(json)


def generate_pic():
    # https://imagemagick.org/script/convert.php
    # convert [img] -font simkai.ttf -gravity center -fill rgba(0,0,0,0.8) -pointsize 25 -annotate "+0+0" "some text" [output]
    convert = path.abspath("./convert.exe")
    font = path.abspath("./fonts/simkai.ttf")
    image = path.abspath("./images/01.jpg")
    output = "out.jpg"
    poetry = get_poetry()
    title = poetry['title'] if 'title' in poetry else poetry['rhythmic']
    text = (linesep * 2).join([f"{title} - {poetry['author']}", *poetry['paragraphs']])
    print()
    print(text)
    cmd = f'''"{convert}" "{image}" -font "{font}" -gravity center -fill rgba(0,0,0,0.8) -pointsize 25 -annotate "+0+0" "{text}" {output}'''
    call(cmd)
    return


def set_wallpaper():
    image = path.abspath("out.jpg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
    return


chdir(sys.path[0])
generate_pic()
set_wallpaper()
