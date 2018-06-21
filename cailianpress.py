from selenium import webdriver
import requests, sys, os, os.path, time, re, datetime, logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from cailianpressnews import CailianPressNews

class CailianPress:

    def __init__(self):
        self.url = "https://www.cailianpress.com/"
        self.web_name = "cailianpress"
        # current date
        self.cur_date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.cur_path = str(sys.path[0])
        # write logs to this file with specific file name
        self.log_file = self.cur_path + "\\logs\\" + self.web_name + "_" + self.cur_date + ".log"
        # write text data to this file with specific file name
        self.data_file = self.cur_path + "\\data\\" + self.web_name + "_" + self.cur_date + ".data"
        self.driver = webdriver.Firefox()
        # text info
        self.text_list = []

    @staticmethod
    def datetime_timestamp(date):
        time.strptime(date, '%Y-%m-%d')
        s = time.mktime(time.strptime(date, '%Y-%m-%d'))
        return int(s)

    def read_last_time_from_the_latest_datafile(self):
        rootdir = self.cur_path + "\\data"
        print(rootdir)
        list_filenames = []
        for parent, dirnames, filenames in os.walk(rootdir):
            for filename in filenames:
                date_part = filename.split("_")[1].replace(".data", "")
                list_filenames.append(date_part)
        list_filenames.sort(key=self.datetime_timestamp, reverse=True)
        latest_date = list_filenames[0]
        latest_file_name_path = rootdir + "\\cailianpress_" + latest_date + ".data"
        file = open(latest_file_name_path, mode='r', encoding='utf-8')
        line = file.readline()
        file.close()
        return line

    @staticmethod
    def valid_text_to_be_present_in_attribute(ele, attr, text):
        attr_value = ele.get_attribute(attr)
        if attr_value:
            return text in attr_value
        else:
            return False

    def extract_one_news_from_one_element(self, ele, date):
        if self.valid_text_to_be_present_in_attribute(ele, "style", "overflow"):
            # extract date info
            return None
        else:
            ctime_element = ele.find_element_by_xpath("./div[@class='newsLeft']/div[@class='cTime']")
            if ctime_element:
                cdate = str(date + " " + ctime_element.text)
                text_element = ele.find_element_by_xpath("./div[@class='newsRight']/p")
                if text_element:
                    text = str(text_element.text)
                    return CailianPressNews(cdate, text)
                else:
                    return None
            else:
                return None

    """
    in news item    <div class="cTime" data-jsx="2516998736">10:46</div>
    """
    def extract_ctime_from_one_element(self, ele):
        if self.valid_text_to_be_present_in_attribute(ele, "style", "overflow"):
            # extract date info
            return None
        else:
            ctime_element = ele.find_element_by_xpath("./div[@class='newsLeft']/div[@class='cTime']")
            if ctime_element:
                ctime = str(ctime_element.text)
                return ctime
            else:
                return None

    """
    <div style="width:100%;height:43px;overflow:hidden;border-top:1px solid #eee;border-bottom:1px solid #eee;" data-reactid="64"><div class="logo" data-reactid="65">
        <div class="time" data-reactid="67">2018-06-04</div>
    """
    @staticmethod
    def extract_news_date_from_one_element(ele):
        date_element = ele.find_element_by_xpath("./div[@class='time']")
        if date_element:
            date = str(date_element.text)
            return date
        else:
            return None

    def valid_end_of_element_list(self, ele):
        if self.valid_text_to_be_present_in_attribute(ele, "class", "getMoreWrap"):
            return True
        else:
            return False

    def print_text(self):
        for news in self.text_list:
            print("----------------------------------------------------")
            print(news.datetime)
            print(news.text)

    def extract_news_data_today(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(self.url)
        not_end_of_today = True
        while not_end_of_today:
            getmore_element = driver.find_element_by_class_name("getMore")
            getmore_element.click()
            driver.implicitly_wait(10)
            centerwrpa_element = driver.find_element_by_xpath(
                "//div[@class='centerWrpa']/div[@class='contentLeft']/div[2]")
            item_elements = centerwrpa_element.find_elements_by_xpath("./div")
            cur_date = ""
            for item in item_elements:
                if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                    cur_date = self.extract_news_date_from_one_element(item)
                    if self.cur_date == cur_date:
                        continue
                    else:
                        not_end_of_today = False
                        break
            if not not_end_of_today:
                for item in item_elements:
                    if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                        cur_date = self.extract_news_date_from_one_element(item)
                        if cur_date:
                            if self.cur_date == cur_date:
                                pass
                            else:
                                break
                        else:
                            print("无法抽取当前日期")
                            break
                    else:
                        news = self.extract_one_news_from_one_element(item, cur_date)
                        if news:
                            self.text_list.append(news)
                        else:
                            print("无法抽取当前新闻内容！")
        #driver.close()
        #self.print_text()

    def extract_news_data_from_last_time(self):
        last_time = self.read_last_time_from_the_latest_datafile()
        item = last_time.split(" ")
        print(item)
        last_date = item[0]
        last_ctime = item[1].replace("\n", "")
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(self.url)
        not_end_of_today = True
        while not_end_of_today:
            getmore_element = driver.find_element_by_class_name("getMore")
            getmore_element.click()
            driver.implicitly_wait(10)
            centerwrpa_element = driver.find_element_by_xpath(
                "//div[@class='centerWrpa']/div[@class='contentLeft']/div[2]")
            item_elements = centerwrpa_element.find_elements_by_xpath("./div")
            cur_date = ""
            is_start_valid = False
            for item in item_elements:
                if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                    cur_date = self.extract_news_date_from_one_element(item)
                    if str((datetime.datetime.strptime(last_date, '%Y-%m-%d')
                            - datetime.timedelta(days=1)).strftime('%Y-%m-%d')) != cur_date:
                        continue
                    else:
                        not_end_of_today = False
                        break
                elif self.valid_end_of_element_list(item):
                    break
                else:
                    ctime = self.extract_ctime_from_one_element(item)
                    if cur_date == last_date and ctime == last_ctime:
                        print("stop!!!")
                        not_end_of_today = False
                        break

            if not not_end_of_today:
                is_valid_interval = False
                is_valid_internal_ctime = True
                for item in item_elements:
                    if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                        cur_date = self.extract_news_date_from_one_element(item)
                        if cur_date:
                            is_valid_interval = True
                        else:
                            print("无法抽取当前日期")
                            break
                    elif is_valid_interval:
                        cur_ctime = self.extract_ctime_from_one_element(item)
                        if cur_date == last_date:
                            if cur_ctime == last_ctime:
                                is_valid_internal_ctime = False
                                break
                        if is_valid_internal_ctime:
                            news = self.extract_one_news_from_one_element(item, cur_date)
                            if news:
                                self.text_list.append(news)
                            else:
                                print("无法抽取当前新闻内容！")
                    else:
                        pass
        self.print_text()

    """
    this method does not work, since the website limit the click times of the button 'getMore',
    usually it will disappear after click 15 times. 
    """
    def extract_news_data_from_to(self, start_date, end_date):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(self.url)
        not_end_of_today = True
        while not_end_of_today:
            getmore_element = driver.find_element_by_class_name("getMore")
            getmore_element.click()
            driver.implicitly_wait(10)
            centerwrpa_element = driver.find_element_by_xpath(
                "//div[@class='centerWrpa']/div[@class='contentLeft']/div[2]")
            item_elements = centerwrpa_element.find_elements_by_xpath("./div")
            cur_date = ""
            for item in item_elements:
                if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                    cur_date = self.extract_news_date_from_one_element(item)
                    if str((datetime.datetime.strptime(start_date, '%Y-%m-%d')
                            - datetime.timedelta(days=1)).strftime('%Y-%m-%d')) != cur_date:
                        continue
                    else:
                        not_end_of_today = False
                        break
            if not not_end_of_today:
                is_valid_interval = False
                for item in item_elements:
                    if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                        cur_date = self.extract_news_date_from_one_element(item)
                        if cur_date:
                            if end_date == cur_date:
                                is_valid_interval = True
                                pass
                            elif str((datetime.datetime.strptime(start_date, '%Y-%m-%d')
                                      - datetime.timedelta(days=1)).strftime('%Y-%m-%d')) \
                                    == cur_date:
                                break
                            else:
                                pass
                        else:
                            print("无法抽取当前日期")
                            break
                    elif is_valid_interval:
                        news = self.extract_one_news_from_one_element(item, cur_date)
                        if news:
                            self.text_list.append(news)
                        else:
                            print("无法抽取当前新闻内容！")
                    else:
                        pass
        self.print_text()

    def extract_news_data_from_to_by_timetag(self, start_date, stime_tag, end_date, etime_tag):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(self.url)
        not_end_of_today = True
        count_of_news = 0
        while not_end_of_today:
            getmore_element = driver.find_element_by_class_name("getMore")
            getmore_element.click()
            driver.implicitly_wait(10)
            centerwrpa_element = driver.find_element_by_xpath(
                "//div[@class='centerWrpa']/div[@class='contentLeft']/div[2]")
            item_elements = centerwrpa_element.find_elements_by_xpath("./div")
            cur_date = ""
            is_end_valid = False
            is_start_valid = False
            for item in item_elements:
                if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                    cur_date = self.extract_news_date_from_one_element(item)
                    if str((datetime.datetime.strptime(start_date, '%Y-%m-%d')
                            - datetime.timedelta(days=1)).strftime('%Y-%m-%d')) != cur_date:
                        continue
                    else:
                        not_end_of_today = False
                        break
                elif self.valid_end_of_element_list(item):
                    break
                else:
                    ctime = self.extract_ctime_from_one_element(item)
                    if cur_date == start_date and ctime == stime_tag:
                        print("stop!!!")
                        not_end_of_today = False
                        break

            if not not_end_of_today:
                is_valid_interval = False
                is_valid_internal_ctime = False
                for item in item_elements:
                    if self.valid_text_to_be_present_in_attribute(item, "style", "overflow"):
                        cur_date = self.extract_news_date_from_one_element(item)
                        if cur_date:
                            if end_date == cur_date:
                                is_valid_interval = True
                                continue
                            else:
                                pass
                        else:
                            print("无法抽取当前日期")
                            break

                    if is_valid_interval:
                        count_of_news += 1
                        print("cur_id: " + str(count_of_news))
                        if len(self.text_list) > 1:
                            print(self.text_list[-1].datetime)
                        cur_ctime = self.extract_ctime_from_one_element(item)
                        if cur_date == end_date:
                            if cur_ctime == etime_tag:
                                print("start found!")
                                is_valid_internal_ctime = True
                        if cur_date == start_date:
                            if cur_ctime == stime_tag:
                                print("end founded !")
                                is_valid_internal_ctime = False
                                break
                        if is_valid_internal_ctime:
                            news = self.extract_one_news_from_one_element(item, cur_date)
                            if news:
                                self.text_list.append(news)
                            else:
                                print("无法抽取当前新闻内容！")
                    else:
                        pass
        self.print_text()

    def write_text_into_file(self):
        try:
            with open(file=self.data_file, mode='w+', encoding='utf-8') as file:
                for news in self.text_list:
                    file.write(news.datetime + "\n")
                    file.write(news.text + "\n")
        except Exception as e:
            print(str(e))
        print("ok")

    def run(self):
        #self.extract_news_data_from_to("2018-06-3", "2018-06-03")
        #self.extract_news_data_today()
        #self.extract_news_data_from_to_by_timetag("2018-06-20", "00:13", "2018-06-20", "23:53")
        self.extract_news_data_from_last_time()
        self.write_text_into_file()


cls = CailianPress()
cls.run()
