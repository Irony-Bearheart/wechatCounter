# -*- encoding: utf-8 -*-
from time import sleep

from wxcounter import *

def main():

    print("Open WeChat chat window and maximize it\n"
          "打开微信聊天窗口并最大化")
    sleep(5)
    focus2center()
    left = []
    right = []
    for image in scroll_screenshot():
        left.append(count_rows(image)[0])
        right.append(count_rows(image)[1])
    print(f"左{sum(left)}，右{sum(right)}")
    return 0


if __name__ == '__main__':
    main()
