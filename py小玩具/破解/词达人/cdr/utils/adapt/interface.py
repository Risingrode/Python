#!/usr/bin/env python
# -*- coding:utf-8 -*-
# cython : language_level=3
# @Time  : 2020-12-23, 0023 17:53
# @Author: 佚名
# @File  : interface.py
import re

from .. import Set
from ..tool import Tool


# 接口基类
class IOrigin:

    # 处理传入的content, remark混合问题
    @staticmethod
    def process_content_and_remark(content: str, remark: str):
        return content, remark

    # 处理不同情况下的翻译以从例句列表中得到对应的英语例句
    @staticmethod
    def is_remark_or_sentence_in_example(example_dict: dict, remark: str, sentence: str) -> bool:
        return example_dict.get(remark) is not None

    # 处理不同情况下的翻译以从短语列表中得到对应的英语短语数组
    @staticmethod
    def phrase_get_remark(phrase_dict: dict, remark: str) -> list:
        pass

    # 处理不同情况下的翻译以从短语列表中得到对应的英语短语数组
    @staticmethod
    def phrase_get_remark_by_ratio(phrase_dict: dict, remark_list: list, ratio: float, adapter) -> list:
        pass

    # 处理选项中单词词义
    @staticmethod
    def process_option_mean(mean: str) -> list:
        return []

    # 处理题库中单词词义
    @staticmethod
    def process_word_mean(mean: str) -> list:
        return []

    # 处理选项中英语例句的特殊情况（目前只是遇见多空格）
    @staticmethod
    def process_option_sentence(sentence: str) -> str:
        pass

    # 处理选项中短语翻译的特殊情况（如多出莫名其妙的符号）
    @staticmethod
    def process_option_phrase(phrase: str) -> str:
        return phrase

    # 处理题库中短语单词自带逗号的问题
    @staticmethod
    def process_answer_phrase(phrase: list[str]) -> list[str]:
        pass

    # 处理题型11中精确匹配失败的情况
    # 为例句翻译添加模糊匹配
    @staticmethod
    def answer_11_1(remark: str, skip_times: int, options: list, answer_list: list, adapter) -> str:
        pass

    # 处理题型11中精确匹配失败的情况
    # 为选项翻译添加模糊匹配
    @staticmethod
    def answer_11_2(sentence: str, remark: str, skip_times: int, options: list, answer_list: list, adapter) -> str:
        pass

    # 处理题型15中精确匹配失败的情况
    # 为选项翻译添加模糊匹配
    @staticmethod
    def answer_15_1(answer_list: list, options: list, adapter) -> str:
        pass

    # 处理题型15中模糊匹配失败的情况
    # 选项4个选项中可信度最高的作为返回值
    @staticmethod
    def answer_15_2(answer_list: list, options: list, adapter) -> tuple[str, float]:
        pass

    # 处理题型17中精确匹配失败的情况
    # 为选项翻译添加模糊匹配
    @staticmethod
    def answer_17_1(content_list: list, options: list, answer_dict: dict, adapter) -> str:
        pass

    # 处理题型32中一个选项中包含多个单词的情况
    @staticmethod
    def answer_32_1(options: list, phrase: list) -> str:
        pass

    # 处理题型32中选项中包含奇怪的情况
    @staticmethod
    def answer_32_2(options: list, phrase: list) -> str:
        """
        :param options: 原选项
        :param phrase: 已经匹配出来的短语
        :return: 合成好的答案
        """
        pass

    # 处理题型32，题库短语比选项多出一个a/an/the或者题库短语比选项少一个a/an/the
    @staticmethod
    def answer_32_3(options: list, phrase_list: list[list], blank_count: int, skip_times: int, adapter) -> str:
        pass

    # 处理题型32，题目中倍数包含一部分短语的问题
    @staticmethod
    def answer_32_4(content: str, remark: str, options: list, blank_count: int, skip_times: int, answer_dict: dict, adapter) -> str:
        pass

    @staticmethod
    def answer_51(option_word: str, word: str) -> str:
        return word

    @staticmethod
    def answer_51_1(answer: dict, remark: str, skip_times: int, phrase_list: list, phrase_list_set: Set, adapter) -> str:
        pass

    @staticmethod
    def answer_51_2(answer: dict, remark: str, skip_times: int, phrase_list: list, phrase_list_set: Set, adapter) -> str:
        pass


# 代码重构适配
class AnswerPattern1(IOrigin):

    @staticmethod
    def process_content_and_remark(content: str, remark: str):
        # 21.3.17修复由群友转交给115***706提交的BUG，我们仍未知道那天是哪位群友的贡献
        # 这个就离谱了，把remark内容放到content中可还行？？？
        if remark is None and content.find("\n") != -1:
            tem_list = content.split("\n")
            content = tem_list[0]
            remark = tem_list[1]
        return content, remark

    @staticmethod
    def is_remark_or_sentence_in_example(example_dict: dict, remark: str, sentence: str) -> bool:
        sentence = " ".join(sentence.split())
        for value in example_dict.values():
            if value == sentence:
                return True
        for key in example_dict.keys():
            if Tool.get_ratio_between_str(key, remark) >= 0.9:
                return True
        return False

    @staticmethod
    def phrase_get_remark(phrase_dict: dict, remark: str) -> list:
        tem = remark.replace('.', ' ').replace("…", " ").replace("-", " ").replace(",", " ")
        # 处理因清理"..."而造成的多余空格
        tem = " ".join(tem.split())
        return phrase_dict.get(tem) or phrase_dict.get(remark.replace("…", "", 1).strip())

    # 处理不同情况下的翻译以从短语列表中得到对应的英语短语数组
    @staticmethod
    def phrase_get_remark_by_ratio(phrase_dict: dict, remark_list: list, ratio: float, adapter) -> list:
        for key, value in phrase_dict.items():
            if Tool.get_ratio_between_list(
                remark_list,
                adapter.process_word_mean(key)
            ) > ratio:
                return value

    @staticmethod
    def process_option_mean(mean: str) -> list:
        return [Tool.sort_str(mean), mean + "；", Tool.sort_str(mean + "；")]

    @staticmethod
    def process_word_mean(mean: str) -> list:
        return [Tool.sort_str(mean)]

    @staticmethod
    def process_option_sentence(sentence: str) -> str:
        return re.sub(r'\s\s', ' ', sentence)

    @staticmethod
    def process_option_phrase(phrase: str) -> str:
        # 去除ZZ的图标字符串
        tem = re.sub(r"[\ue000-\uefff()]", "", phrase)
        tem = tem.replace('.', ' ').replace("…", " ").replace("-", " ").replace(",", " ").replace("\n", "").strip()
        return " ".join(tem.split())

    @staticmethod
    def process_answer_phrase(phrase: list[str]) -> list[str]:
        if " ".join(phrase).find(",") == -1:
            return None
        result = []
        for phrase_word in phrase:
            result.append(re.sub(",", "", phrase_word))
        return result

    # 模糊匹配
    @staticmethod
    def answer_11_1(remark: str, skip_times: int, options: list, answer_list: list, adapter) -> str:
        for answer in answer_list:
            for content in answer["content"]:
                for key in content["example"].keys():
                    if Tool.get_ratio_between_str(key, remark) < 0.75:
                        continue
                    for mean in options:
                        tem_list = adapter.process_option_mean(mean["content"])
                        # 若选项集合与题库集合的相似度超过3/4，则该选项有可能等于题库中的选项
                        if len(set(tem_list) & set(adapter.process_word_mean(content["mean"]))) != 0:
                            if skip_times != 0:
                                skip_times -= 1
                                continue
                            return str(mean["answer_tag"])

    @staticmethod
    def answer_11_2(sentence: str, remark: str, skip_times: int, options: list, answer_list: list, adapter) -> str:
        lowest_ratio = 0.7  # 若选项集合与题库集合的相似度超过3/4，则该选项有可能等于题库中的选项
        if len(answer_list) == 1:   # 若题库集合仅1个，降低匹配率，仅需确保不会匹配到非
            lowest_ratio = 0.5
        for answer in answer_list:
            for content in answer["content"]:
                if adapter.is_remark_or_sentence_in_example(content["example"], remark, sentence):
                    for mean in options:
                        tem_list = adapter.process_option_mean(mean["content"])
                        if Tool.get_ratio_between_list(tem_list,
                                                       adapter.process_word_mean(content["mean"])) >= lowest_ratio:
                            if skip_times != 0:
                                skip_times -= 1
                                continue
                            return str(mean["answer_tag"])

    @staticmethod
    def answer_15_1(answer_list: list, options: list, adapter) -> str:
        for mean in options:
            if Tool.is_str_in_list(mean["content"], answer_list) \
                    or Tool.get_ratio_between_list(adapter.process_option_mean(mean["content"]),
                                                   answer_list
                                                   ) >= 0.65:
                return str(mean["answer_tag"])

    @staticmethod
    def answer_15_2(answer_list: list, options: list, adapter) -> tuple[str, float]:
        result = None
        for mean in options:
            option_mean = re.sub(r"^[a-zA-Z]+\s?", "", mean["content"])
            trust_ratio = Tool.get_ratio_between_list(adapter.process_option_mean(option_mean), answer_list)
            if result is None:
                result = (mean["answer_tag"], trust_ratio)
            elif result[1] <= trust_ratio:
                result = (mean["answer_tag"], trust_ratio)
        return result

    @staticmethod
    def answer_17_1(content_list: list, options: list, answer_dict: dict, adapter) -> str:
        for word in options:
            answer = answer_dict.get(word["content"])
            if answer is None:  # 选项中可能存在不在课程中的单词，故查询结果可能为空
                continue
            #   创建一个临时列表
            tem_list = []
            for mean in answer["content"]:
                tem_list.extend(adapter.process_word_mean(mean["mean"]))
            if Tool.get_ratio_between_list(tem_list, content_list) >= 0.8:
                return str(word["answer_tag"])

    @staticmethod
    def answer_32_1(options: list, phrase: list) -> str:
        result = []
        tem_map = {}
        for index, option in enumerate(options):
            for tem_value in re.split(r"\s+", option["content"].strip()):
                tem_map[tem_value] = index
        for word in phrase:
            if len(result) == 0 or tem_map.get(result[len(result) - 1]) != tem_map.get(word):
                result.append(word)
            else:
                result[len(result) - 1] = Tool.get_most_similar_word_in_list(
                    result[len(result) - 1] + word, list(tem_map.keys()))
        return ",".join(result)

    @staticmethod
    def answer_32_2(options: list, phrase: list) -> str:
        for index, value in enumerate(phrase):
            for v in options:
                if value == AnswerPattern1.process_option_phrase(v["content"]):
                    phrase[index] = v["content"]
        return ",".join(phrase)

    @staticmethod
    def answer_32_3(options: list, phrase_list: list[list], blank_count: int, skip_times: int, adapter) -> str:
        flag = ["a", "an", "the"]
        # 选项预处理
        option_list = []  # 存放选项中的短语，短语由规定顺序的单词数组构成
        for phrase in options:
            content, _ = adapter.process_content_and_remark(phrase["content"], None)
            option_list.extend(re.split(r"\s+", adapter.process_option_phrase(content)))
        option_set = Set(option_list)
        wrong_set = set()

        for phrase in phrase_list:
            # 题库短语比选项多出一个a/an/the
            if len(option_set & Set(phrase)) == len(phrase) - 1 and phrase[0] in flag:
                if skip_times != 0 or adapter.answer_32_2(options, phrase) in wrong_set:
                    skip_times -= 1
                    wrong_set.add(adapter.answer_32_2(options, phrase))
                    continue
                phrase = phrase[1:]
                if len(phrase) == blank_count:
                    # 因原选项中可能会出现多出空格问题
                    return adapter.answer_32_2(options, phrase)
            # 题库短语比选项少出一个a/an/the
            if len(option_set & Set(phrase)) == len(phrase) and len(set(option_list) & set(flag)) != 0:
                for word in flag:
                    real_phrase = phrase.copy()
                    real_phrase.insert(0, word)
                    if len(option_set & Set(real_phrase)) == len(phrase) + 1:
                        break
                else:
                    break
                if skip_times != 0 or adapter.answer_32_2(options, real_phrase) in wrong_set:
                    skip_times -= 1
                    wrong_set.add(adapter.answer_32_2(options, real_phrase))
                    continue
                if len(real_phrase) == blank_count:
                    # 因原选项中可能会出现多出空格问题
                    return adapter.answer_32_2(options, real_phrase)

    @staticmethod
    def answer_32_4(question_content: str, remark: str, options: list, blank_count: int, skip_times: int, answer_dict: dict, adapter) -> str:
        content_list = re.split("\s+", question_content)
        # 选项预处理
        option_list = []  # 存放选项中的短语，短语由规定顺序的单词数组构成
        for phrase in options:
            content, _ = adapter.process_content_and_remark(phrase["content"], None)
            option_list.extend(re.split(r"\s+", adapter.process_option_phrase(content)))
        for content_word in content_list:
            if content_word.find("_") == -1:
                option_list.extend(re.split(r"\s+", adapter.process_option_phrase(content_word)))
        option_set = Set(option_list)
        wrong_set = set()

        for key, value in answer_dict.items():
            for content in value["content"]:
                phrase_list = content["phrase"].get(remark) or adapter.phrase_get_remark(content["phrase"], remark)
                if phrase_list is None:
                    break
                for answer_phrase in phrase_list:
                    for phrase in adapter.process_answer_phrase(answer_phrase):
                        if len(option_set & Set(phrase)) == len(phrase):
                            if skip_times != 0 or adapter.answer_32_2(options, phrase) in wrong_set:
                                skip_times -= 1
                                wrong_set.add(adapter.answer_32_2(options, phrase))
                                continue
                            result_fix = []
                            if len(content_list) < len(phrase):
                                # 选项中存在一个选项包含多个单词的情况
                                # tem_map = {}
                                # for index, option in enumerate(options):
                                #     for tem_value in re.split(r"\s+", option["content"].strip()):
                                #         tem_map[tem_value] = {
                                #             "index": index,
                                #             "origin": option["content"]
                                #         }
                                # last_index = 0
                                # fix_index = 0
                                # skip = 0
                                # for word in phrase:
                                #     if question_content.find(word, last_index) != -1:
                                #         last_index = question_content.find(word) + len(word)
                                #         continue
                                #     if skip != 0:
                                #         skip = skip - 1
                                #         continue
                                #     if len(result_fix) == 0 \
                                #             or tem_map.get(word) \
                                #             and (
                                #             tem_map.get(result_fix[-1])
                                #             and tem_map[result_fix[-1]]["index"] != tem_map[word]["index"] \
                                #         or tem_map[word]["index"] ==
                                #     ):
                                #         result_fix.append(word)
                                #     else:
                                #         fix_index = fix_index + 1
                                #         result_fix[-1] = tem_map[word]["origin"]
                                #         skip = len(tem_map[word]["origin"].split(" ")) - 2
                                # return ",".join(result_fix)
                                return None
                            for index, phrase_word in enumerate(phrase):
                                if content_list[index].find("_") != -1:
                                    result_fix.append(phrase_word)
                            if len(result_fix) != blank_count:
                                break
                            return ",".join(result_fix)

    @staticmethod
    def answer_51(option_word: str, word: str) -> str:
        return word.replace(option_word.replace("{", "").replace("}", ""), "")

    @staticmethod
    def answer_51_1(answer: dict, remark: str, skip_times: int, phrase_list: list, phrase_list_set: Set, adapter) -> str:
        if len(phrase_list) <= 1:
            return None
        for key, value in answer.items():
            for content_list in value["content"]:
                phrases = content_list["phrase"].get(remark)\
                         or adapter.phrase_get_remark(content_list["phrase"], remark)
                if phrases is not None:
                    for phrase in phrases:
                        if abs(len(phrase) - len(phrase_list)) != 1:
                            continue
                        max_set = Set(phrase)
                        min_set = phrase_list_set
                        if len(max_set) < len(min_set):
                            tem = max_set
                            max_set = min_set
                            min_set = tem
                        tem = max_set - min_set - Set(["an", "a", "the"])
                        if len(max_set) == 1 and len(min_set) == len(Set(max_set) - tem):
                            if skip_times != 0:
                                skip_times -= 1
                                continue
                            return list(tem)[0]


# 20.12.29修复由群友183***092提交的BUG
# 处理选项中莫名其妙多出来的一个"，"
class AnswerPattern2(IOrigin):

    # 模糊匹配
    @staticmethod
    def answer_11_2(sentence: str, remark: str, skip_times: int, options: list, answer_list: list, adapter) -> str:
        for answer in answer_list:
            for content in answer["content"]:
                if adapter.is_remark_or_sentence_in_example(content["example"], remark, sentence):
                    mean_list = [content["mean"]]
                    for mean in options:
                        tem_list = adapter.process_option_mean(mean["content"])
                        if Tool.is_str_list_in_another(mean_list, tem_list):
                            if skip_times != 0:
                                skip_times -= 1
                                continue
                            return str(mean["answer_tag"])

    @staticmethod
    def process_word_mean(mean: str) -> list:
        tem = mean.replace("，", "").replace(" ", "")
        return [tem, Tool.sort_str(tem)]

    @staticmethod
    def process_option_mean(mean: str) -> list:
        tem = mean.replace("，", "").replace(" ", "")
        return [tem, Tool.sort_str(tem)]


# 20.12.29修复由群友253***814提交的BUG
# 这是他在看着电视没事干时试出来的
# 处理选项中括号及括号中的内容
class AnswerPattern3(IOrigin):

    @staticmethod
    def process_option_mean(mean: str) -> list:
        # 去除多余的<>
        tem = re.sub(r"[<(（].*?[）)>]", "", mean)
        return [tem, Tool.sort_str(tem)]


# 21.3.17修复由群友253***349提交的BUG
# 处理填空时根据单词翻译填单词，翻译中多出单词类型的问题
class AnswerPattern4(IOrigin):

    @staticmethod
    def process_option_mean(mean: str) -> list:
        tem = mean.replace("…", "")
        return [tem, Tool.sort_str(tem)]

    @staticmethod
    def process_word_mean(mean: str) -> list:
        return [re.sub(r"(?:[A-Za-z-]*)?\s?", "", mean)]


# 21.3.23修复由群友839***272提交的BUG
# 处理短语翻译多出符号问题
class AnswerPattern5(IOrigin):

    @staticmethod
    def phrase_get_remark(phrase_dict: dict, remark: str) -> list:
        is_more = re.compile(r"(.*…)\s(…[^a-zA-Z]*)")
        if is_more.match(remark) is None:
            matcher = re.match(r"([0-9A-Za-z.\s(){}'/&‘’,（）…-]*)?\s(.*)", remark)
        else:
            matcher = re.match(r"([0-9A-Za-z.\s(){}'/&‘’,（）…-]*)?\s(….*)", remark)
        if matcher is None:
            return None
        return phrase_dict.get(matcher.group(2).strip())


# 21.3.25修复由群友224***087提交的BUG
# 这是他在看着电视没事干时试出来的
# 处理选项中多余的中文括号
class AnswerPattern6(IOrigin):

    @staticmethod
    def process_option_mean(mean: str) -> list:
        # 去除多余的中文括号
        tem = re.sub(r"([A-Za-z\s]+)?(（?(?:(?!（).)+）)", r"\1", mean)
        return [tem, Tool.sort_str(tem)]


# 21.4.17修复由群友148***020提交的BUG
# 处理多余空格并乱序
class AnswerPattern7(IOrigin):

    @staticmethod
    def process_option_mean(mean: str) -> list:
        # 移除所有空格并排序
        return [Tool.sort_str(re.sub(r"\s+", "", mean))]

    @staticmethod
    def process_word_mean(mean: str) -> list:
        # 移除所有空格并排序
        return [Tool.sort_str(re.sub(r"\s+", "", mean))]


# 21.5.12修复由群友530***887提交的BUG
class AnswerPattern8(IOrigin):

    @staticmethod
    def answer_51_1(answer: dict, remark: str, skip_times: int, phrase_list: list, phrase_list_set: Set, adapter) -> str:
        if len(phrase_list) <= 1:
            return None
        remark_set = set(adapter.process_option_mean(remark))
        for key, value in answer.items():
            for content_list in value["content"]:
                if len(set(adapter.process_word_mean(content_list["mean"])) & remark_set) != 0:
                    phrases = content_list["phrase"].get(remark) \
                             or adapter.phrase_get_remark(content_list["phrase"], remark)
                    for phrase in phrases:
                        if len(phrase_list) - 1 != len(phrase_list_set & Set(phrase)) \
                                or len(phrase_list) != len(phrase):
                            continue
                        for index, word in enumerate(phrase):
                            if word != phrase_list[index]:
                                if skip_times != 0:
                                    skip_times -= 1
                                    continue
                                return phrase[index]

    @staticmethod
    def answer_51_2(answer: dict, remark: str, skip_times: int, phrase_list: list, phrase_list_set: Set, adapter) -> str:
        if len(phrase_list) <= 1:
            return None
        for key, value in answer.items():
            for content_list in value["content"]:
                phrases = content_list["phrase"].get(remark) \
                         or adapter.phrase_get_remark_by_ratio(content_list["phrase"],
                                                               adapter.process_option_mean(remark))
                if phrases is not None:
                    for phrase in phrases:
                        if abs(len(phrase) - len(phrase_list)) != 1:
                            continue
                        max_set = Set(phrase)
                        min_set = phrase_list_set
                        if len(max_set) < len(min_set):
                            tem = max_set
                            max_set = min_set
                            min_set = tem
                        tem = max_set - min_set - Set(["an", "a", "the", "oneself"])
                        if len(max_set) == 1 and len(min_set) == len(Set(max_set) - tem):
                            if skip_times != 0:
                                skip_times -= 1
                                continue
                            return list(tem)[0]
