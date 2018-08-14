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
        self.cur_year = str(datetime.datetime.now().year)
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

    def valid_element_exist_by_xpath(self, ele, xpath):
        es = ele.find_elements_by_xpath(xpath)
        size = len(es)
        if size == 0:
            return False
        elif size == 1:
            return True
        else:
            print(xpath + ", found " + str(size))
            return True

    def valid_element_exist_by_css(self, ele, css):
        es = ele.find_elements_by_css_selector(css)
        size = len(es)
        if size == 0:
            return False
        elif size == 1:
            return True
        else:
            print(css + ", found " + str(size))
            return True

    def valid_is_commmon_news_element(self, ele):
        return self.valid_element_exist_by_xpath(ele, ".[@class='jsx-1890198016']")

    def extract_news_from_common_news_element(self, ele):
        try:
            common_news_element = ele.find_element_by_xpath("./div/div/div/span[@class='jsx-1890198016']")
            common_news = str(common_news_element.text).replace("\u200B", "")
            return common_news
        except NoSuchElementException as ex:
            return None

    def extract_time_from_common_news_element(self, ele):
        try:
            common_news_time_element = ele.find_element_by_css_selector(".jsx-1890198016.time-text")
            common_news_time = str(common_news_time_element.text)
            return common_news_time
        except NoSuchElementException as ex:
            return None

    def valid_is_common_day_title_element(self, ele):
        return self.valid_element_exist_by_css(ele, ".jsx-3362659131.telegraph-time-box")

    def extract_news_from_common_day_title_element(self, ele):
        try:
            common_day_title_news_element = ele.find_element_by_xpath("./div[@class='jsx-1890198016']/div/div/div/span[@class='jsx-1890198016']")
            common_day_title_news = str(common_day_title_news_element.text).replace("\u200B", "")
            return common_day_title_news
        except Exception as ex:
            return None

    def extract_time_from_common_day_title_element(self, ele):
        try:
            common_day_title_news_time_element = ele.find_element_by_css_selector(".jsx-1890198016.time-text")
            common_day_title_news_time = str(common_day_title_news_time_element.text)
            return common_day_title_news_time
        except Exception as ex:
            return None

    def extract_date_from_common_day_title_element(self, ele):
        try:
            common_day_title_news_date_element = ele.find_element_by_css_selector(".jsx-3362659131.telegraph-time")
            common_day_title_news_date = str(common_day_title_news_date_element.text).split(" ")[0]
            print("common day title date: " + str(common_day_title_news_date))
            return str(common_day_title_news_date)
        except Exception as ex:
            return None

    def valid_is_first_day_title_element(self, ele):
        return self.valid_element_exist_by_css(ele, ".jsx-897524169.first-tele-time")

    def extract_news_from_first_day_title_element(self, ele):
        try:
            first_day_title_news_element = ele.find_element_by_xpath("./div[@class='jsx-1890198016']/div/div/div/span")
            first_day_title_news = str(first_day_title_news_element.text).replace("\u200B", "")
            return first_day_title_news
        except NoSuchElementException:
            return None

    def extract_time_from_first_day_title_element(self, ele):
        try:
            first_day_title_time_element = ele.find_element_by_css_selector(".jsx-1890198016.time-text")
            first_day_title_time = str(first_day_title_time_element.text)
            return first_day_title_time
        except NoSuchElementException:
            return None

    def extract_date_from_first_day_title_element(self, ele):
        try:
            first_day_title_date_element = ele.find_element_by_css_selector(".jsx-897524169.first-tele-time")
            first_day_title_date = str(first_day_title_date_element.text).split(" ")[0]
            print("first day title date: " + first_day_title_date)
            return str(first_day_title_date)
        except NoSuchElementException:
            return None

    @staticmethod
    def valid_text_to_be_present_in_attribute(ele, attr, text):
        attr_value = ele.get_attribute(attr)
        if attr_value:
            return text in attr_value
        else:
            return False

    def valid_end_of_element_list(self, ele):
        if self.valid_element_exist_by_css(ele, ".jsx-927607683.wrap"):
            end_ele = ele.find_element_by_css_selector(".jsx-927607683.wrap")
            if end_ele.text == "已经加载到最后了":
                return True
            else:
                return False
        else:
            return False

    def valid_is_last_of_element_list(self, ele):
        if self.valid_element_exist_by_css(ele, ".jsx-927607683.wrap"):
            end_ele = ele.find_element_by_css_selector(".jsx-927607683.wrap")
            if end_ele.text == "点击加载更多":
                return True
            else:
                return False
        else:
            return False

    def valid_to_the_last_time(self, cur_date, cur_time, last_date, last_time):
        if cur_date == last_date and cur_time <= last_time:
            return True
        else:
            return False

    def valid_is_date_item(self, ele):
        if self.valid_is_common_day_title_element(ele):
            return self.extract_date_from_common_day_title_element(ele)
        if self.valid_is_first_day_title_element(ele):
            return self.extract_date_from_first_day_title_element(ele)
        return None

    def print_text(self):
        for news in self.text_list:
            print("----------------------------------------------------")
            print(news.datetime)
            print(news.text)

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
        count = 0
        while not_end_of_today:
            getmore_element = driver.find_element_by_css_selector(".jsx-927607683.wrap")
            if getmore_element:
                print("click once!")
                getmore_element.click()
            else:
                not_end_of_today = False
            count += 1
            print("click " + str(count))
            driver.implicitly_wait(10)
            centerwrpa_element = driver.find_element_by_css_selector(".jsx-992155393.contentLeft")
            item_elements = centerwrpa_element.find_elements_by_xpath("./div/div")
            valid_item_elements = item_elements[1:]
            n = len(valid_item_elements)
            print("list count: " + str(n))
            cur_date = ""
            is_start_valid = False

            common_day_title_elements = driver.find_elements_by_css_selector(".jsx-3362659131.telegraph-time")
            size_of_common_day_title_element = len(common_day_title_elements)
            print("common day title element: " + str(size_of_common_day_title_element))
            if size_of_common_day_title_element == 0:
                cur_date = self.cur_date
                if cur_date == last_date:
                    # check the last news ctime
                    last_news_element = valid_item_elements[-2]
                    # extract ctime
                    ctime_ele = last_news_element.find_element_by_xpath("./div/div/span")
                    ctime = ctime_ele.text
                    if ctime <= last_ctime:
                        print("end founded!")
                        not_end_of_today == False
                    else:
                        continue
            else:
                # check the last common day title
                last_common_day_title_element = common_day_title_elements[-1]
                last_common_day_title_date = last_common_day_title_element.text.split(" ")[0]
                last_common_day_title_date = self.cur_year + "-" + last_common_day_title_date
                if last_date == self.cur_date:
                    print("end founded")
                    not_end_of_today = False
                elif last_common_day_title_date != last_date:
                    continue
                else:
                    # check the last news
                    last_news_element = valid_item_elements[-2]
                    # extract ctime
                    ctime_ele = last_news_element.find_element_by_xpath("./div/div/span")
                    ctime = ctime_ele.text
                    if ctime <= last_ctime:
                        print("end founded")
                        not_end_of_today = False
                    else:
                        continue

            if not not_end_of_today:
                is_valid_interval = False
                is_valid_internal_ctime = True
                print("start!")
                cur_date = ""  # contains both cur_year and cur_date, eg. 2018-06-06
                n = 0
                for item in valid_item_elements:
                    n += 1
                    print("current: " + str(n))
                    if self.valid_is_commmon_news_element(item):
                        news_text = self.extract_news_from_common_news_element(item)
                        ctime = self.extract_time_from_common_news_element(item)
                        cdate = cur_date + " " + str(ctime)
                        if self.valid_to_the_last_time(cur_date, ctime, last_date, last_ctime):
                            break
                        news = CailianPressNews(cdate, news_text)
                        self.text_list.append(news)
                        print("add common news element")
                    elif self.valid_is_common_day_title_element(item):
                        news_text = self.extract_news_from_common_day_title_element(item)
                        cur_date = self.cur_year + "-" + self.extract_date_from_common_day_title_element(item)
                        ctime = self.extract_time_from_common_day_title_element(item)
                        if self.valid_to_the_last_time(cur_date, ctime, last_date, last_ctime):
                            break
                        cdate = cur_date + " " + ctime
                        news = CailianPressNews(cdate, news_text)
                        self.text_list.append(news)
                        print("add common day title element")
                    elif self.valid_is_last_of_element_list(item):
                        print("last element")
                        continue
                    elif self.valid_is_first_day_title_element(item):
                        news_text = self.extract_news_from_first_day_title_element(item)
                        cur_date = self.cur_year + "-" + self.extract_date_from_first_day_title_element(item)
                        ctime = self.extract_time_from_first_day_title_element(item)
                        cdate = cur_date + " " + ctime
                        news = CailianPressNews(cdate, news_text)
                        self.text_list.append(news)
                        print("add first day title element")
                    else:
                        print("extract news failed!")
        self.print_text()

    def extract_news_data_from(self, start_date, start_time):
        last_date = start_date
        last_ctime = start_time
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(self.url)
        not_end_of_today = True
        count = 0
        is_before_the_first_day = False
        while not_end_of_today:
            getmore_element = driver.find_element_by_css_selector(".jsx-927607683.wrap")
            if getmore_element:
                print("click once!")
                getmore_element.click()
            else:
                not_end_of_today = False
            count += 1
            print("click " + str(count))
            driver.implicitly_wait(10)
            centerwrpa_element = driver.find_element_by_css_selector(".jsx-992155393.contentLeft")
            item_elements = centerwrpa_element.find_elements_by_xpath("./div/div")
            valid_item_elements = item_elements[1:]
            n = len(valid_item_elements)
            print("list count: " + str(n))
            cur_date = ""
            is_start_valid = False

            common_day_title_elements = driver.find_elements_by_css_selector(".jsx-3362659131.telegraph-time")
            size_of_common_day_title_element = len(common_day_title_elements)
            print("common day title element: " + str(size_of_common_day_title_element))
            if size_of_common_day_title_element == 0:
                cur_date = self.cur_date
                if cur_date == last_date:
                    # check the last news ctime
                    last_news_element = valid_item_elements[-2]
                    # extract ctime
                    ctime_ele = last_news_element.find_element_by_xpath("./div/div/span")
                    ctime = ctime_ele.text
                    if ctime <= last_ctime:
                        print("end founded!")
                        not_end_of_today == False
                    else:
                        continue
            else:
                # check the last common day title
                is_before_the_first_day = True
                last_common_day_title_element = common_day_title_elements[-1]
                last_common_day_title_date = last_common_day_title_element.text.split(" ")[0]
                last_common_day_title_date = self.cur_year + "-" + last_common_day_title_date
                if last_date == self.cur_date:
                    print("end founded")
                    not_end_of_today = False
                elif last_common_day_title_date != last_date:
                    continue
                else:
                    # check the last news
                    last_news_element = valid_item_elements[-2]
                    # extract ctime
                    ctime_ele = last_news_element.find_element_by_xpath("./div/div/span")
                    ctime = ctime_ele.text
                    if ctime <= last_ctime:
                        print("end founded")
                        not_end_of_today = False
                    else:
                        continue

            if not not_end_of_today:
                is_valid_interval = False
                is_valid_internal_ctime = True
                print("start!")
                cur_date = ""  # contains both cur_year and cur_date, eg. 2018-06-06
                n = 0
                for item in valid_item_elements:
                    n += 1
                    print("current: " + str(n))
                    if self.valid_is_commmon_news_element(item):
                        news_text = self.extract_news_from_common_news_element(item)
                        ctime = self.extract_time_from_common_news_element(item)
                        cdate = cur_date + " " + str(ctime)
                        if self.valid_to_the_last_time(cur_date, ctime, last_date, last_ctime):
                            break
                        news = CailianPressNews(cdate, news_text)
                        self.text_list.append(news)
                        print("add common news element")
                    elif self.valid_is_common_day_title_element(item):
                        news_text = self.extract_news_from_common_day_title_element(item)
                        cur_date = self.cur_year + "-" + self.extract_date_from_common_day_title_element(item)
                        ctime = self.extract_time_from_common_day_title_element(item)
                        if self.valid_to_the_last_time(cur_date, ctime, last_date, last_ctime):
                            break
                        cdate = cur_date + " " + ctime
                        news = CailianPressNews(cdate, news_text)
                        self.text_list.append(news)
                        print("add common day title element")
                    elif self.valid_is_last_of_element_list(item):
                        print("last element")
                        continue
                    elif self.valid_is_first_day_title_element(item):
                        news_text = self.extract_news_from_first_day_title_element(item)
                        cur_date = self.cur_year + "-" + self.extract_date_from_first_day_title_element(item)
                        ctime = self.extract_time_from_first_day_title_element(item)
                        cdate = cur_date + " " + ctime
                        news = CailianPressNews(cdate, news_text)
                        self.text_list.append(news)
                        print("add first day title element")
                    else:
                        print("extract news failed!")
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
        #self.extract_news_data_from_to_by_timetag("2018-07-13", "17:47", "2018-07-16", "10:41")
        #self.extract_news_data_from("2018-08-12", "22:19")
        self.extract_news_data_from_last_time()
        self.write_text_into_file()


cls = CailianPress()
cls.run()
