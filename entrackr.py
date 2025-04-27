import time
from dateparser import parse
import requests
import json
import os
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers.data_push import push_news

from helpers.data_helper import clean_text, get_first_element, get_text, get_all_cin


class EntrackrCraweler(object):

    def __init__(self, company_name, company_cin, max_page_count=5):
        self.company_name = company_name
        self.company_cin = company_cin
        self.page_count = 1
        self.max_page_count = max_page_count
        self.base_url = 'https://entrackr.com'

    def start_driver(self):
        """
        This function start  driver with relevent settings
        :return:
        """
        SELENIUM_DRIVER_PATH = os.getcwd() + "/chrome_driver/chromedriver_linux"
        chrome_options = Options()
        #chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36")
        # chrome_options.add_argument('--no-sandbox')
        #prefs = {"profile.default_content_setting_values.notifications": 2}
        #chrome_options.add_experimental_option("prefs", prefs)
        #chrome_options.add_argument('--disable-dev-shm-usage')
        # driver = webdriver.Chrome(SELENIUM_DRIVER_PATH, chrome_options=chrome_options)
        driver = webdriver.Chrome(SELENIUM_DRIVER_PATH, options=chrome_options)
        return driver
    def get_news_data(self):
        while self.max_page_count >= self.page_count:
            try:
                self.company_name = self.company_name.replace(" ", "%20")
                #url = 'https://entrackr.com/page/'+str(self.page_count)+'/?s=' + clean_text(self.company_name).lower()
                url="https://entrackr.com/search?page="+str(self.page_count)+"&title="+clean_text(self.company_name).lower()
                print("URL:",url)
                driver = self.start_driver()
                driver.get(url)
                time.sleep(10)
                with open("output_entrack.html","w") as f:
                   f.write(driver.page_source)
                #print(driver.page_source)
                doc = html.fromstring(driver.page_source)
                news = doc.xpath("//div[@class='abc search_post_div']")
                #news = doc.xpath("//article[contains(@id,'post')]")
                page_not_found = get_first_element(doc.xpath("//h3[@class='elementor-heading-title elementor-size-default']/text()"))
                print("NEWS COUNT:", len(news))
                if page_not_found :
                    if page_not_found.lower()=="Oops! That page can't be found".lower():
                        print("No More News !")
                        break
                if len(news) > 0 :
                    for new in news:
                        title = get_first_element(new.xpath(".//h3[@class='elementor-heading-title elementor-size-default']/a/text()"))
                        link = get_first_element(new.xpath(".//h3[@class='elementor-heading-title elementor-size-default']/a/@href"))
                        if self.company_name.lower().replace("%20","") not in title.lower().replace(" ",""):
                            #print("IN:",self.company_name.lower().replace(" ",""))
                            #print(title.lower().replace(" ",""))
                            continue
                        if self.base_url not in link:
                            link = self.base_url + link
                        print("LINK:",link)
                        news_data = {"title": title.replace('"','').replace("'",""), "url": link, "source": 'entrackr',
                                     "company_name": self.company_name.replace("&"," and"), "cin": self.company_cin,
                                     'category': 'financial'}
                        news_data.update(self.get_news_details(link))
                        print("TIME:",news_data.get("date"))
                        print("<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>.")
                        response = push_news(news_data, self.company_cin)
                        if response.status_code == 200:
                            print("News Data Pushed ....")
                        else:
                            print(response.text)
                            print(news_data)
                            print("News Data Not Pushed ....")
                    self.page_count = self.page_count + 1
                    print("NEXT PAGE:")
                else:
                    break
            except Exception as EX:
                print(self.page_count, "EXCEPTION:", EX)
                self.page_count = self.page_count + 1
                pass

    def get_news_details(self, url):
        #TODO work on description
        r = requests.get(url)
        if r.status_code == 200:
            doc = html.fromstring(r.text)
            # description = get_text(doc.xpath("//div[@class='elementor-row']"))
            # if description is None:
            #     description = 'No Description Found'
            authors = get_text(get_first_element(doc.xpath("//span[contains(@class,'elementor-post-info__item--type-author')]")))
            time = ''
            time_element = get_text(get_first_element(doc.xpath("//span[contains(@class,'item--type-date')]")))
            print("TIME LE:",time_element)
            if time_element:
                time = parse(time_element)
                time = time.strftime("%m/%d/%Y")
            # return {'author': authors, "description": description.replace('"','').replace("'",""), "date": time}
            return {'author': authors.replace(" ", "" ), "date": time}
        return {}





def get_news_data():
    input_company_data = get_all_cin()
    cin_list = [
        'U93090MH2010PTC209218',
        #'U80904KL2021PTC067288'
    ]
    # input_company_data = input_company_data[10:]
    for company in input_company_data:
        cin = company.get("cin")
        if cin not in cin_list:
            continue
        company_name = company.get("name")
        print("Searching ", company_name, "...")
        try:
            news = EntrackrCraweler(company_name, cin, 5)
            news.get_news_data()
        except:
            print("No News ..")


get_news_data()
