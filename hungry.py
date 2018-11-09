#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pythonスクリプトの記述例

# 関数の定義
# 関数が呼び出されたときにのみ実行される
def say_hungry():
    print("I'm very Hungry!!!")

# メインルーチンとして実行される場合のみ実行する
# pythonインタプリタから直接実行される場合に実行される．
# 他のファイルから import されるときは実行されない
#
# Jupyter Notebookのセルの中に記述した場合にも実行される
if __name__ == "__main__":
    print("main start!")

