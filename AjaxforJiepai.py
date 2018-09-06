#使用Ajax爬去今日头条街拍图片

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):
    params = {
        'offset' : offset,
        'format' : 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count'  : '20',
        'cur_tab' : '3',
    }

    url = 'https://www.toutiao.com/search_content/?'+urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None



def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            
            #注意到部分相应内容不存在title属性，防止异常抛出
            try:
                for image in images:
                    yield {
                        'image' : image.get('url'),
                        'title' : title
                    }
            except TypeError:
                print('This unit has no title!')
                

def save_image(item):
    #print('ok')
    if not os.path.exists('/home/mico/Desktop/python3Spider_code/Jiepai/'+item.get('title')):
        os.mkdir('/home/mico/Desktop/python3Spider_code/Jiepai/'+item.get('title'))
    try:
        response = requests.get('http:'+item.get('image'))
        if response.status_code ==200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists('/home/mico/Desktop/python3Spider_code/Jiepai/'+file_path):
                with open('/home/mico/Desktop/python3Spider_code/Jiepai/'+file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
       # print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    groups = ([x*20 for x in range(GROUP_START,GROUP_END+1)])
    for offset in groups:
        #print(offset)
        main(offset)