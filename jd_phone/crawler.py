# -*- coding: utf-8 -*-
#
# Created by: https://github.com/Hopetree
#
# Created data: 2017/7/29

from selenium import webdriver
import time
import datetime
from lxml import etree
import xlwt
import requests
import json
import re


class JDPhone(object):
    def __init__(self, max_p):
        '''判重的集合'''
        self.set = set()
        # 手动设置最大页数
        self.max_p = max_p
        self.T = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M")
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
        self.title_list = ['id', 'shopname', 'is_jd', 'price', 'brand', 'year', 'month', 'weight', 'thick', 'long',
                           'cpu_brand', 'cpu_num',
                           'sim_num', 'sim', 'rom', 'ram', 'size', 'front_c', 'back_c', 'battery',
                           'total_com', 'good_com', 'mid_com', 'bad_com', 'good_lv', 'mid_lv', 'bad_lv']
        self.base_url = 'https://www.jd.com/'
        self.key = "手机"
        self.row = 2
        self.wk = xlwt.Workbook(encoding="utf-8")
        self.sheet = self.wk.add_sheet(self.key)
        self.set_title()
        self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        time.sleep(0.2)
        self.driver.find_element_by_id("key").clear()
        self.driver.find_element_by_id("key").send_keys(self.key)
        self.driver.find_element_by_xpath("//button/i[@class='iconfont']").click()

    def set_title(self):
        '''给表格添加标题'''
        titles = ["商品ID", "店铺名称", "是否自营", "价格", "品牌", "上市年份", "上市月份", "机身重量", "机身厚度", "机身长度", "CPU品牌", "CUP核数",
                  "单双卡类型", "SIM卡类型", "ROM", "RAM", "屏幕尺寸", "前置像素", "后置像素", "电池容量",
                  "总评论数", "好评数", "中评数", "差评数", "好评率", "中评率", "差评率"]
        i = 0
        for each, top in zip(titles, self.title_list):
            self.sheet.write(0, i, each, xlwt.easyxf("font:bold on"))
            '''第一行用中文标题，第二行用英文标题，英文标题方便后续做统计分析'''
            self.sheet.write(1, i, top, xlwt.easyxf("font:bold on"))
            self.sheet.col(i).width = 256 * 10
            i += 1
        return

    def save_info(self, *args):
        '''解析每个单品页面，提取并保存信息到表格，接受2个参数，分别是商品ID和价格组成的元祖和表格中行数'''
        url = "https://item.jd.com/{}.html".format(args[0])
        html = requests.get(url, headers=self.headers).text
        tree = etree.HTML(html)
        # 先给每个标题一个空值，后面找到数据再替换
        # 信息要分普通的和全球购，所以查找的时候要用|
        item = {t: "" for t in self.title_list}
        item['id'] = args[0]
        item['price'] = args[1]
        is_jd = tree.xpath("//em[@class='u-jd']/text()")
        if is_jd:
            item['is_jd'] = is_jd[-1].strip()
        shopname = tree.xpath("//div[@class='name']/a/@title|//div[@class='shopName']/strong/span/a/text()")
        if shopname:
            item['shopname'] = shopname[0]
        brand = tree.xpath(
            "//dt[text()='品牌']/following-sibling::*[1]/text()|//dt[text()='品牌']/following-sibling::*[1]/text()")
        if brand:
            item['brand'] = brand[0]
        year = tree.xpath(
            "//dt[text()='上市年份']/following-sibling::*[1]/text()|//td[text()='上市年份']/following-sibling::*[1]/text()")
        if year:
            item['year'] = year[0]
        month = tree.xpath(
            "//dt[text()='上市月份']/following-sibling::*[1]/text()|//td[text()='上市月份']/following-sibling::*[1]/text()")
        if month:
            item['month'] = month[0]
        weight = tree.xpath(
            "//dt[text()='机身重量（g）']/following-sibling::*[1]/text()|//dt[text()='机身重量（g）']/following-sibling::*[1]/text()")
        if weight:
            item['weight'] = weight[0]
        thick = tree.xpath(
            "//dt[text()='机身厚度（mm）']/following-sibling::*[1]/text()|//dt[text()='机身厚度（mm）']/following-sibling::*[1]/text()")
        if thick:
            item['thick'] = thick[0]
        long = tree.xpath(
            "//dt[text()='机身长度（mm）']/following-sibling::*[1]/text()|//dt[text()='机身长度（mm）']/following-sibling::*[1]/text()")
        if long:
            item['long'] = long[0]
        cpu_brand = tree.xpath(
            "//dt[text()='CPU品牌']/following-sibling::*[1]/text()|//dt[text()='CPU品牌']/following-sibling::*[1]/text()")
        if cpu_brand:
            item['cpu_brand'] = cpu_brand[0]
        cpu_num = tree.xpath(
            "//dt[text()='CPU核数']/following-sibling::*[1]/text()|//dt[text()='CPU核数']/following-sibling::*[1]/text()")
        if cpu_num:
            item['cpu_num'] = cpu_num[0]
        sim_num = tree.xpath(
            "//dt[text()='双卡机类型']/following-sibling::*[1]/text()|//dt[text()='双卡机类型']/following-sibling::*[1]/text()")
        if sim_num:
            item['sim_num'] = sim_num[0]
        sim = tree.xpath(
            "//dt[text()='SIM卡类型']/following-sibling::*[1]/text()|//dt[text()='SIM卡类型']/following-sibling::*[1]/text()")
        if sim:
            item['sim'] = sim[0]
        rom = tree.xpath(
            "//dt[text()='ROM']/following-sibling::*[1]/text()|//dt[text()='ROM']/following-sibling::*[1]/text()")
        if rom:
            item['rom'] = rom[0]
        ram = tree.xpath(
            "//dt[text()='RAM']/following-sibling::*[1]/text()|//dt[text()='RAM']/following-sibling::*[1]/text()")
        if ram:
            item['ram'] = ram[0]
        size = tree.xpath(
            "//dt[text()='主屏幕尺寸（英寸）']/following-sibling::*[1]/text()|//dt[text()='主屏幕尺寸（英寸）']/following-sibling::*[1]/text()")
        if size:
            item['size'] = size[0]
        front_c = tree.xpath(
            "//dt[text()='前置摄像头']/following-sibling::*[1]/text()|//dt[text()='前置摄像头']/following-sibling::*[1]/text()")
        if front_c:
            item['front_c'] = front_c[0]
        back_c = tree.xpath(
            "//dt[text()='后置摄像头']/following-sibling::*[1]/text()|//dt[text()='后置摄像头']/following-sibling::*[1]/text()")
        if back_c:
            item['back_c'] = back_c[0]
        battery = tree.xpath(
            "//dt[text()='电池容量（mAh）']/following-sibling::*[1]/text()|//dt[text()='电池容量（mAh）']/following-sibling::*[1]/text()")
        if battery:
            item['battery'] = battery[0]
        dsr = self.get_dsr(args[0])['CommentsCount'][0]
        item['total_com'] = dsr['CommentCount']
        item['good_com'] = dsr['GoodCount']
        item['mid_com'] = dsr['GeneralCount']
        item['bad_com'] = dsr['PoorCount']
        item['good_lv'] = dsr['GoodRate']
        item['mid_lv'] = dsr['GeneralRate']
        item['bad_lv'] = dsr['PoorRate']
        print(item)
        c = 0
        for tt in self.title_list:
            self.sheet.write(self.row, c, item[tt])
            c += 1
        self.row += 1

    def get_dsr(self, id):
        '''提取dsr'''
        url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.format(id)
        html = requests.get(url, headers=self.headers).text
        data = json.loads(html)
        return data

    def getall(self):
        '''提取页面的ID，并按照每个ID去解析单个商品的页面提取信息,递归翻页'''
        time.sleep(0.1)
        '''将网页滑到最下面，加载出所有的商品，这个滑动的次数可以根据试探来选择最少次数和最短等待时间'''
        for i in range(18):
            js = "window.scrollTo(0,{})".format(i * 500)
            self.driver.execute_script(js)
            time.sleep(0.3)
        # self.driver.save_screenshot("screenshot.png")
        # 将加载后的网页解析出来
        tree = etree.HTML(self.driver.page_source)
        result = tree.xpath("//div[@id='J_goodsList']/ul/li")
        if result:
            for each in result:
                id = each.xpath('@data-sku')[0]
                price = each.cssselect('div.p-price > strong > i')[0].text
                if id not in self.set:
                    try:
                        self.save_info(id, price)
                        self.set.add(id)
                    except Exception as e:
                        print(id, e)

        next_page = tree.xpath("//a[@class='pn-next']")
        if next_page and self.max_p - 1:
            self.max_p -= 1
            self.driver.find_element_by_xpath("//a[@class='pn-next']").click()
            time.sleep(0.1)
            next_url = self.driver.current_url
            pagenum = re.findall("&page=(\d*?)&", next_url)[0]
            pagenum = (int(pagenum) + 1) // 2
            print('找到下一页，即将提取第{}页的信息'.format(pagenum))
            self.getall()
        else:
            print("所有页面已经全部提取完毕！")


if __name__ == '__main__':
    '''唯一的参数是需要爬的最大页码数，如果要爬全部的可以输入一个很大的值'''
    jd = JDPhone(1000)
    jd.getall()
    jd.wk.save("{}_{}.xls".format(jd.key, jd.T))
