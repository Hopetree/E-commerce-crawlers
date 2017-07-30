import requests
import json
import re
import time
'''
date:2017-3-14
程序用来提取天猫商品的评论标签，将商品ID放在文本中，启动程序，得到商品的评论标签
'''

print("-"*30,"*"*4,"-"*30)
print('程序说明'.center(61))
print(r'''【1】程序获取天猫商品的评论标签
【2】创建一个txt文本，把文本放在跟程序同一文件夹中
【3】在文本里面存放商品ID,每行放一个
【4】按照要求输入文件的名称
【5】在程序所在文件夹中生成一个信息表格''')
print('作者：Alex Zhu'.rjust(50))
print("-"*30,"*"*4,"-"*30)

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

# 获取单个商品的DSR信息
def get_dsr(item_id):
    URL = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId={id}&callback=jsonp'
    url = URL.format(id = item_id)
    data = requests.get(url,headers=headers).text
    info_dic = json.loads(re.findall('jsonp\((.*)\)', data)[0])
    dsr = {}
    dsr['grade'] = info_dic['dsr']['gradeAvg']
    dsr['ratetotal'] = info_dic['dsr']['rateTotal']
    # print(dsr)
    return dsr

# 获取单个商品的评论标签信息
def get_tag_info(item_id):
    URL = 'https://rate.tmall.com/listTagClouds.htm?itemId={id}&isAll=true&isInner=true&callback=jsonp'
    url = URL.format(id = item_id)
    data = requests.get(url,headers=headers).text
    info_dic = json.loads(re.findall('jsonp\((.*)\)',data)[0])
    infos = info_dic['tags']['tagClouds']
    dsr = get_dsr(item_id)
    dsr_grade = dsr['grade']
    dsr_ratetotal = dsr['ratetotal']
    if len(infos)>0:
        for info in infos:
            tag = info['tag']
            # tag_id = info['id']
            countnum = info['count']
            posi = info['posi']
            try:
                prop = '{:.2f}%'.format((countnum/dsr_ratetotal)*100)
            except:
                prop = '{:.2f}%'.format(0)
            print(item_id,'\t',tag,'\t',countnum)
            the_list = [str(item_id),str(posi),tag,str(countnum),str(prop),str(dsr_grade),str(dsr_ratetotal)]
            with open('tags.csv','a') as f:
                f.write(','.join(the_list)+'\n')
    else:
        print(item_id,'没有评论标签！')

# 读取文件中ID
def get_idlist(filename):
    with open(filename,'r') as f:
        lines = f.readlines()
    idlist = []
    for each in lines:
        idlist.append(each.strip())
    return idlist

# 主函数，逻辑判断
def main(filename):
    # 创建一个表格并写明标题
    titles = ['商品ID','标签性质','标签内容','相关评论数','相关评论占比','商品评分','商品总评论数']
    with open('tags.csv','w') as f:
        f.write(','.join(titles)+'\n')
    idlist = get_idlist(filename)
    totalid = len(idlist)
    i = 1
    for id in idlist:
        print('总计{0}个商品，正在爬取第{1}个商品的评论标签-----------------'.format(totalid,i))
        get_tag_info(id)
        i = i+1

if __name__ == '__main__':
    filename = input('请输入放置ID的文件名（含后缀）：').strip()

    start = time.time()
    main(filename)
    end = time.time()
    print('程序运行完毕，耗时：{:.2f}秒'.format(end-start))
    input('输入任意内容退出程序！')