#!/usr/bin/env python
# -*- coding:utf-8 -*-
# cython : language_level=3
# @Time  : 2020-12-20, 0020 22:29
# @Author: 佚名
# @File  : tool.py
import asyncio
import difflib
import hashlib
import os
import time
import threading

from cdr.utils import Set


class Tool:

    @staticmethod
    def __start_loop(loop, is_run_forever):
        asyncio.set_event_loop(loop)
        if is_run_forever:
            loop.run_forever()

    @staticmethod
    def new_event_loop(is_run_forever: bool = True):
        loop = asyncio.new_event_loop()
        t = threading.Thread(target=Tool.__start_loop, args=(loop, is_run_forever))
        t.start()
        return loop

    @staticmethod
    async def run_tasks(task_list: list, loop):
        return await asyncio.gather(*task_list, loop=loop)

    @staticmethod
    def get_most_similar_word_in_list(aim_word: str, aim_list: list) -> str:
        max_ratio = 0.0
        word = ""
        for value in aim_list:
            value_ratio = difflib.SequenceMatcher(None, aim_word, value).quick_ratio()
            if max_ratio < value_ratio:
                max_ratio = value_ratio
                word = value
        return word

    @staticmethod
    def get_ratio_between_str(str_a: str, str_b: str) -> float:
        return difflib.SequenceMatcher(None, str_a, str_b).quick_ratio()

    @staticmethod
    def get_ratio_between_list(list_a: list, list_b: list) -> float:
        max_ratio = 0.0
        for a in list_a:
            for b in list_b:
                tem_ratio = difflib.SequenceMatcher(None, a, b).quick_ratio()
                max_ratio = tem_ratio if tem_ratio > max_ratio else max_ratio
        return max_ratio

    @staticmethod
    def is_str_in_list(content: str, aim: list) -> bool:
        for item in aim:
            if content.find(item) != -1 or item.find(content) != -1:
                return True
        return False

    @staticmethod
    def is_str_in_list_by_some_difference(content: str, aim: list) -> bool:
        ratio = 0.0
        for item in aim:
            tem = Tool.get_ratio_between_str(content, item)
            ratio = ratio if tem < ratio else tem
        return ratio >= 0.98

    @staticmethod
    def is_str_list_in_another(list_a: list, list_b: list) -> bool:
        for a in list_a:
            for b in list_b:
                if "".join(Set([s for s in a]) & Set([s for s in b])) == a:
                    return True
        return False

    # 答案匹配所需方法，无视可读性按字符大小排序
    @staticmethod
    def sort_str(s: str) -> str:
        li = list(s)
        li.sort()
        return "".join(li)

    # 答案匹配所需方法，计算所需单词数量
    @staticmethod
    def count_character_in_str(character, string):
        count = 0
        for c in string:
            if c == character:
                count = count + 1
        return count

    #   md5加密函数
    @staticmethod
    def md5(s: str) -> str:
        md5 = hashlib.md5()
        md5.update(s.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def convert_time(time_stamp: int) -> str:
        second = int(time_stamp / 1000)
        minute = int(second / 60)
        hour = int(minute / 60)
        if hour != 0:
            return f"{hour}小时{minute - hour * 60}分钟{second - minute * 60}秒"
        if minute != 0:
            return f"{minute}分钟{second - minute * 60}秒"
        return f"{second}秒"

    @staticmethod
    def time() -> int:
        return round(time.time() * 1000)

    @staticmethod
    def cls():
        tem = os.system('cls')
