#引入文件
from scrapy.exceptions import DropItem
import json

class MyPipeline(object):
    def __init__(self):
        #打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    #该方法用于处理数据
    def process_item(self, item, spider):
        #读取item中的数据.    dumps是将dict转化成str格式，loads是将str转化成dict格式。dump和load也是类似的功能，只是与文件操作结合起来了。
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #写入文件
        self.file.write(line)
        #返回item
        return item

    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        print("spider被开启")
        pass

    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        print("spider被关闭")
        pass