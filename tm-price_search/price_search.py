# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
import random

class TM_itemdetail(object):
    def __init__(self,readname='ids.txt',savename='info.csv'):
        '''传入2个参数，分别是读取ID的文本名称和保存信息的表格名称，给予默认值'''
        self.readname = readname
        self.savename = savename
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()
        # 设置一个只能等待
        self.waiter = WebDriverWait(self.driver,5)
        self.get_csv()

    def get_csv(self):
        '''创建一个表格，并且给表格添加标题行'''
        with open(self.savename,'w',newline='') as f:
            fieldnames = ['id','price']
            writer = csv.DictWriter(f,fieldnames=fieldnames)
            writer.writeheader()

    def write_info(self,info_dic):
        '''写入单个信息，传入的参数是一个字典，字典的key跟表格的标题对应'''
        with open(self.savename,'a',newline='') as f:
            fieldnames = ['id', 'price']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(info_dic)

    def get_ids(self):
        '''读取文本的ID，形成一个列表'''
        with open(self.readname,'r') as f:
            lines = f.readlines()
        ids = [k.replace('\n','').strip() for k in lines]
        return ids

    def get_info(self,id):
        '''爬虫的主要操作，模拟打开浏览器，找到信息的标签，提取后写入表格'''
        dic = {}
        url = 'https://detail.tmall.hk/hk/item.htm?spm=a220o.1000855.1998025129.2.102f616emYvWTL&abtest=_AB-LR32-PR32&pvid=a2be15e3-8200-46b3-bd09-de041b8b8dc3&pos=2&abbucket=_AB-M32_B9&acm=03054.1003.1.2431317&id={}&scm=1007.12144.81309.23864_0&sku_properties=-1:-1'.format(id)
        self.driver.get(url)
        # html = self.driver.page_source
        # print(html)
        try:
            location = self.waiter.until(
                EC.presence_of_element_located((By.XPATH,'//dl[@class="tm-happy11-panel"]/dd/span[@class="tm-price"]'))
            )
            info = location.text.strip()
            dic['id'] = id
            dic['price'] = info if info else '信息为空白'
            self.write_info(dic)
        except TimeoutException as e:
            print(e)
            dic['id'] = id
            dic['price'] = '{}超时，未找到信息'.format(e).strip()
            self.write_info(dic)

    def main(self):
        '''主函数，循环爬取，并打印相应的操作过程'''
        time.sleep(30)
        print('准备登陆信息')
        ids = self.get_ids()
        counter = len(ids)
        i = 1
        for id in ids:
            self.get_info(id)
            time.sleep(random.choice([3,4,5,6]))
            print('总计{}个，已经爬取{}个'.format(counter,i))
            i += 1


if __name__ == '__main__':
    start = time.time()
    tm = TM_itemdetail()
    tm.main()
    tm.driver.close()
    end = time.time()
    print('运行结束，总耗时：{:.2f}秒'.format(end-start))



