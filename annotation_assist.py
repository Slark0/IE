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
        '''
        for key in sorted_keyword_list:
            idx += 1
            if idx % 5 == 0:
                print(key[0] + '-' + key[1])
            else:
                print(key[0] + '-' + key[1] + '，', end='')
        '''
        return sorted_keyword_list

    def auto_annotation_of_entity(self, key_words):
        txt_pattern = re.compile(r'.*txt$')
        ann_pattern = re.compile(r'.*ann$')
        for root, dirs, files in os.walk(self.__root_dir):
            entity_pattern = re.compile(r'T\d*\t\S* (\d*) (\d*)\t.*')

            for file in files:
                if txt_pattern.match(file):
                    txt_file_path = os.path.join(root, file)
                    try:
                        with open(file=txt_file_path, mode='r', encoding='utf-8') as f:
                            text = f.readline()
                            text = text.strip('\n')
                            print(text)
                            ann_file_path = txt_file_path.replace('.txt', '.ann')
                            record_idx = self.count_of_entities(ann_file_path) + 1
                            #test_str = '标普500指数上涨1.2%，完全收复周二失地。美股能源股大幅上涨，埃克森美孚涨3.4%，壳牌石油存托涨逾3%，雪弗龙涨2.65%，道达尔涨3.37%，中石油涨3.14%，康菲石油涨逾4%，英国石油、中石化、斯伦贝谢涨逾2%。'
                            # to match a confenrence, such as, 2017年第10界中国各种博览会, 第10界中国各种大会
                            confenrence_pattern = re.compile(
                                r'((\d{2,4}年)|(第\S*界))(第\S界)?\S*?(大会|会议|博览会|展览会|讨论会|研讨会|展销会|小组会|年会|论坛|峰会)')
                            # to match a date
                            date_pattern = re.compile(
                                r'(((去年|今年|\d{2,4}年)?(\d{1,2}|本|上)月(\d{1,2}(日|号))?)|(\d{1,2}(日|号)))(上午|下午|中午|晚间|夜晚|凌晨)?')
                            # to match a stock index, percentage number
                            percent_pattern = r'\d+(\.\d+)?(%|点关口|关口|点大关|大关|个百分点|个点|点)'

                            # to check all the keywords
                            for kw in key_words:
                                #print('kw:' + kw)
                                #print(kw[0])
                                # a keyword could exist in a news more than one times
                                keyword_pattern = re.compile(kw[0])
                                kw_match_iter = re.finditer(keyword_pattern, text)
                                matched_kw_list = []  # [matched_kw_info, matched_kw_info, matched_kw_info]
                                for m_it in kw_match_iter:
                                    matched_kw_info = [kw[0], str(m_it.start()), str(m_it.end())]  # [keyword, start, end]
                                    print('--' + matched_kw_info[0] + ',' + matched_kw_info[1] + ',' + matched_kw_info[2])
                                    matched_kw_list.append(matched_kw_info)

                                # to check these keywords whether exists in annotation file
                                new_entity_records_list = []
                                try:
                                    with open(file=ann_file_path, mode='r', encoding='utf-8') as af:
                                        lines = af.readlines()
                                        if len(matched_kw_list) > 0:
                                            for mkl in matched_kw_list:
                                                is_founded = False
                                                for line in lines:
                                                    entity_match = entity_pattern.match(line)
                                                    if entity_match:
                                                        start = int(entity_match.group(1))
                                                        end = int(entity_match.group(2))
                                                        mkl1 = int(mkl[1])
                                                        mkl2 = int(mkl[2])
                                                        if mkl1 == start:
                                                            is_founded = True
                                                            if end == mkl2:
                                                                print(mkl[0] + ', ' + mkl[1] + ', ' +
                                                                      mkl[2] + ' 已存在')
                                                            elif end > mkl2:
                                                                print(mkl[0] + ', ' + mkl[1] + ', ' +
                                                                      mkl[2] + ' 被包含匹配')
                                                            else:
                                                                print(mkl[0] + ', ' + mkl[1] + ', ' +
                                                                      mkl[2] + ' 包含匹配')
                                                            break
                                                        elif end > mkl1 > start:
                                                            is_founded = True
                                                            print(mkl[0] + ', ' + mkl[1] + ', '
                                                                  + mkl[2] + ' 内包含匹配')
                                                        else:
                                                            continue

                                                if not is_founded:
                                                    record = 'T' + str(record_idx) + '\t' + kw[1] + ' ' + \
                                                             str(mkl[1]) + ' ' + str(mkl[2]) + '\t' + mkl[0] + '\n'
                                                    print(record)
                                                    new_entity_records_list.append(record)
                                                    record_idx += 1
                                except Exception as e:
                                    print(str(e))

                                # to write record into ann file
                                if len(new_entity_records_list) > 0:
                                    try:
                                        with open(file=ann_file_path, mode='a+', encoding='utf-8') as af2:
                                            for record in new_entity_records_list:
                                                pass
                                                #print(record)
                                                #af2.write(record)
                                    except Exception as e:
                                        print(str(e))

                    except Exception as e:
                        print(str(e))
                elif ann_pattern.match(file):
                    #pass
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
aa.print_all_current_news('D:\\dev\\src\\work\\brat\\cailianpress\\split')
#keywords = aa.load_all_keywords(r'D:\dev\src\work\brat\cailianpress\keywords')
#aa.auto_annotation_of_entity(keywords)
#count = aa.count_of_entities(r'D:\dev\src\work\brat\cailianpress\split\cailianpress_2018-05-31\2018-05-31_02_27_457.ann')
#print(count)
#keywords = aa.load_keywords_list_from(r'D:\dev\src\work\brat\cailianpress\keywords\地缘政治实体_人口中心.txt')
#aa.auto_annotation_of_entity('地缘政治实体_人口中心', keywords)
#aa.print_keywords(keywords)