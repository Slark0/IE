from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
import sys
import os
import os.path
import time
import re
import datetime


class AnnotationAssist(object):

    def __init__(self):
        self.__data_path = 'D:\\dev\\src\\work\\brat\\cailianpress'
        self.__root_dir = 'D:\\dev\\src\\work\\brat\\cailianpress\\split'

    def get_all_a_stocks_name_from(self, path):
        if os.path.exists(path):
            if os.access(path, os.R_OK):
                work_book = load_workbook(filename=path)
                ws = work_book.get_active_sheet()

                stock_file_path = os.path.join(self.__data_path, '产品_股票.txt')
                try:
                    with open(file=stock_file_path, mode='w+', encoding='utf-8') as file:
                        for r in range(2, 3570):
                            stock = str(ws.cell(row=r, column=1).value).split('.')[0] + "，" + \
                                    str(ws.cell(row=r, column=2).value).replace('*', '') + '\n'
                            file.write(stock)
                except Exception as e:
                    print(str(e))

                work_book.close()
            else:
                print(path + " 不可读！")
        else:
            print(path + " 不存在！")

    def load_keywords_list_from(self, path):
        if os.path.exists(path):
            if os.access(path, os.R_OK):
                lines = None
                keywords = []
                try:
                    with open(file=path, mode='r', encoding='utf-8') as file:
                        lines = file.readlines()
                        print(path + "== 已读取行数:" + str(len(lines)))
                except Exception as e:
                    print(str(e))
                entity_type = path.split('\\')[-1].replace('.txt', '')
                print(entity_type)
                if not lines:
                    return None
                for line in lines:
                    if not line:
                        continue
                    words = line.split('，')
                    for word in words:
                        word = word.strip().replace('\n', '')
                        if ',' in word:
                            print(path + ' 发现英文逗号:' + word)
                        entity_pair = [word, entity_type]
                        #print(entity_pair[0] + '-' + entity_pair[1])
                        keywords.append(entity_pair)
                return keywords
            else:
                print(path + " 不可读！")
                return None
        else:
            print(path + " 不存在！")
            return None

    def load_all_keywords(self, path):
        keyword_list = []
        for root, dirs, files in os.walk(path):
            txt_pattern = re.compile(r'.*txt$')
            for file in files:
                if txt_pattern.match(file):
                    txt_file_path = os.path.join(root, file)
                    words = self.load_keywords_list_from(txt_file_path)
                    if not words:
                        continue
                    keyword_list.extend(words)
        idx = 0
        sorted_keyword_list = sorted(keyword_list, key=lambda x: (len(x[0])), reverse=True)

        for key in sorted_keyword_list:
            idx += 1
            if idx % 5 == 0:
                print(key[0] + '-' + key[1])
            else:
                print(key[0] + '-' + key[1] + '，', end='')

        return sorted_keyword_list


    def auto_annotation_of_entity(self, key_words):
        txt_pattern = re.compile(r'.*txt$')
        ann_pattern = re.compile(r'.*ann$')
        for root, dirs, files in os.walk(self.__root_dir):
            for file in files:
                if txt_pattern.match(file):
                    txt_file_path = os.path.join(root, file)
                    try:
                        with open(file=txt_file_path, mode='r', encoding='utf-8') as file:
                            line = file.readline()
                            line = line.strip('\n')
                            print(line)
                            for kw in key_words:
                                #print('kw:' + kw)
                                # a keyword could exist in a news more than one times
                                kw_match_iter = re.finditer(kw[0], line)
                                matched_kw_list = []  # [matched_kw_info, matched_kw_info, matched_kw_info]
                                for m_it in kw_match_iter:
                                    matched_kw_info = [kw, m_it.start(), m_it.end()]  # [keyword, start, end]
                                    matched_kw_list.append(matched_kw_list)

                                # print matched keyword list
                                for mkl in matched_kw_list:
                                    print(mkl[0] + ', ' + mkl[1] + ', ' + mkl[2])

                                # to check these keywords whether exists in annotation file
                                ann_file_path = txt_file_path.replace('.txt', '.ann')
                                entity_pattern = re.compile(r'T\d*\t\S* (\d*) (\d*)\t.*')
                                new_entity_records_list = []
                                record_idx = self.count_of_entities(ann_file_path) + 1
                                try:
                                    with open(file=ann_file_path, mode='r', encoding='utf-8') as file:
                                        lines = file.readlines()
                                        for mkl in matched_kw_list:
                                            is_founded = False
                                            for line in lines:
                                                entity_match = entity_pattern.match(line)
                                                if entity_match:
                                                    start = int(entity_match.group(1))
                                                    if mkl[1] == start:
                                                        is_founded = True
                                                        end = int(entity_match.group(2))
                                                        if end == mkl(2):
                                                            print(mkl[0] + ', ' + mkl[1] + ', ' +
                                                                  mkl[2] + ' 已存在')
                                                        elif end > mkl[2]:
                                                            print(mkl[0] + ', ' + mkl[1] + ', ' +
                                                                  mkl[2] + ' 被包含')
                                                        else:
                                                            print(mkl[0] + ', ' + mkl[1] + ', ' +
                                                                  mkl[2] + ' 非完整匹配')
                                                        break
                                                    else:
                                                        continue

                                            if not is_founded:
                                                record = 'T' + str(record_idx) + '\t' + kw[1] + ' ' + \
                                                         str(start) + ' ' + str(end) + '\t' + kw[0] + '\n'
                                                new_entity_records_list.append(record)
                                                record_idx += 1
                                except Exception as e:
                                    print(str(e))

                                # to write record into ann file
                                try:



                                '''
                                # this block code could only find a key word in one time
                                start = line.find(kw[0])
                                if start != -1:
                                    end = len(kw[0]) + start
                                    print(kw[0] + 'start:' + str(start) + ', ' + 'end:' + str(end))
                                    # to check this keyword whether exists in annotation file
                                    ann_file_path = txt_file_path.replace('.txt', '.ann')
                                    span_start, span_end = self.search_exists_span_in_annotation_file(start, ann_file_path)
                                    if span_start == -1:
                                        # to annotate this key word in a .ann file
                                        try:
                                            with open(file=ann_file_path, mode='a+', encoding='utf-8') as file:
                                                # build an annotation record
                                                record_idx = self.count_of_entities(ann_file_path) + 1
                                                record = 'T' + str(record_idx) + '\t' + kw[1] + ' ' + \
                                                         str(start) + ' ' + str(end) + '\t' + kw[0] + '\n'
                                                #file.write(record)
                                                print(record)
                                        except Exception as e:
                                            print(str(e))
                                    else:
                                        if int(span_end) == int(end):
                                            print(kw[0] + ' 已存在')
                                        else:
                                            print(kw[0] + ' 被包含')
                                else:
                                    continue
                                '''

                    except Exception as e:
                        print(str(e))
                elif ann_pattern.match(file):
                    file_path = os.path.join(root, file)
                else:
                    print('遇到非 .txt, .ann文件了，跳过')

    def count_of_entities(self, path):
        #entity_pattern = re.compile(r'T(\d*)\t(\S*) (\d*) (\d*)\t(\S*)\n')
        entity_pattern = re.compile(r'T(\d*)')
        count = 0
        try:
            with open(file=path, mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    entity_match = entity_pattern.match(line)
                    if entity_match:
                        count += 1
        except Exception as e:
            print(str(e))

        return count

    '''
    these code could only check a word in one time
    so, do not use it anymore
    '''
    def search_exists_span_in_annotation_file(self, start_idx, path):
        entity_pattern = re.compile(r'T\d*\t\S* (\d*) (\d*)\t.*')
        try:
            with open(file=path, mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    entity_match = entity_pattern.match(line)
                    if entity_match:
                        start = entity_match.group(1)
                        if int(start_idx) == int(start):
                            end = entity_match.group(2)
                            return start, end
                        else:
                            pass
        except Exception as e:
            print(str(e))
        return -1, -1

    @staticmethod
    def print_keywords(key_words):
        idx = 0
        for keyword in key_words:
            idx += 1
            if idx % 10 == 0:
                print(str(keyword[0]) + '-' + str(keyword[1]))
            else:
                print(str(keyword[0]) + '-' + str(keyword[1]) + '，', end='')

    @staticmethod
    def print_all_current_news(path):
        txt_pattern = re.compile(r'.*txt$')
        lines = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if txt_pattern.match(file):
                    txt_file_path = os.path.join(root, file)
                    try:
                        with open(file=txt_file_path, mode='r', encoding='utf-8') as file:
                            line = file.readline()
                            lines.append(line)
                    except Exception as e:
                        print(str(e))
        for line in lines:
            print(line)


aa = AnnotationAssist()
#aa.get_all_a_stocks_name_from('D:\\dev\\src\\work\\brat\cailianpress\\全部A股.xlsx')
#keywords = aa.load_keywords_list_from("D:\\dev\\src\\work\\brat\cailianpress\\中国人口中心.txt")
#aa.print_keywords(keywords)
#aa.auto_annotation_of_entity('', keywords)
#aa.print_all_current_news('D:\\dev\\src\\work\\brat\\cailianpress\\split')
keywords = aa.load_all_keywords(r'D:\dev\src\work\brat\cailianpress\keywords')
aa.auto_annotation_of_entity(keywords)
#count = aa.count_of_entities(r'D:\dev\src\work\brat\cailianpress\split\cailianpress_2018-05-31\2018-05-31_02_27_457.ann')
#print(count)
#keywords = aa.load_keywords_list_from(r'D:\dev\src\work\brat\cailianpress\keywords\地缘政治实体_人口中心.txt')
#aa.auto_annotation_of_entity('地缘政治实体_人口中心', keywords)
#aa.print_keywords(keywords)