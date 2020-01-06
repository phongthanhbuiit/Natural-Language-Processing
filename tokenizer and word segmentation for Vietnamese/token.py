# -*- coding: utf-8 -*-

# author: Bui Thanh Phongg - 51600063
# version: 2.2
# date-update: 11-09-2019

# specials = ["->", "\.\.\.", ">>"]
# digit = "\d+([\.,_]\d+)+"
# email = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
# web = "^(http[s]?://)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
# word = "\w+"
# non_word = "[^\w\s]"

import re
from readfile import *


class TokenAndWordSeg():
    def __init__(self, vn_dic_path='vnDictionary.txt'):
        self.vn_dic_list = load_vn_dic(vn_dic_path)
        self.tokens_in_dic = []
        self.tokens_in_dic_four_words = []
        self.tokens_in_dic_three_words = []
        self.tokens_in_dic_two_words = []

        for index in self.vn_dic_list:
            self.tokens_in_dic.append(self.tokenizer(index))

        for index in self.tokens_in_dic:
            # words = 4 - length = 7
            # words = 3 - length = 5
            # words = 2 - length = 3
            if (len(index) == 7):
                self.tokens_in_dic_four_words.append(index)
            if (len(index) == 5):
                self.tokens_in_dic_three_words.append(index)
            if (len(index) == 3):
                self.tokens_in_dic_two_words.append(index)

    # phan tich ra cac tokenizer
    def tokenizer(self, text):
        words_list = []
        string_cut_space = re.split(r'(["->", "\.\.\.", ">>"])', text)
        words_list = string_cut_space
        return words_list

    # tach chuoi ra thanh cac list bi phan cac boi cac dau cau . hoac : hoac ""
    # Ham tra ve list gom cac list da duoc phan tach
    def sparateToList(self, tokens):
        r_lsit = []
        temp_list = []
        check_after_doc = False
        for index in tokens:
            if index is '.' or index is '\n' or index is ':':
                if len(temp_list) > 2:
                    r_lsit.append(temp_list)
                temp_list = []
                check_after_doc = True
            elif check_after_doc == True:
                check_after_doc = False
            elif index is '"':
                if len(temp_list) > 2:
                    r_lsit.append(temp_list)
                temp_list = []
            else:
                temp_list.append(index)
        return r_lsit

    def segmentationWord(self, sparate_to_list):
        result_list = []
        for index in sparate_to_list:
            len_tokens = len(index)
            curr_index = 0
            temp_list = []
            done = False
            print(len_tokens)
                               temp_list.append(curr_words)
                    temp_list.append(index[curr_index + 1])
                    temp_list.append(index[curr_index + 2])
                    print(temp_list)
                    if (curr_index >= len_tokens - 2):
                        if temp_list in self.tokens_in_dic_two_words:
                            result_list.append(next_list)
                            curr_index = curr_index + 2
                        else:
                            result_list.append(curr_words)
                            curr_index = curr_index + 1
                    else:
                        temp_list.append(index[curr_index + 3])
                        temp_list.append(index[curr_index + 4])
                        print(temp_list)
                done = True
        return result_list


def test():
    s = 'Ông ấy nói: "Tốc độ truyền thông tin của chúng ta ngày càng nâng cao". Tôi là học sinh.'
    tokenizer_test = TokenAndWordSeg()
    tokens = tokenizer_test.tokenizer(s)
    sparate_to_list = tokenizer_test.sparateToList(tokens)
    r = tokenizer_test.segmentationWord(sparate_to_list)
    print(r)


if __name__ == '__main__':
    test()
