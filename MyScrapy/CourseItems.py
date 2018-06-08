#引入文件
import scrapy

class CourseItem(scrapy.Item):
    #1.课程标题
    title = scrapy.Field()
    #2.课程url
    url = scrapy.Field()
    #3.课程标题图片
    image_url = scrapy.Field()
    #4.课程描述
    introduction = scrapy.Field()
    #5.学习人数
    student = scrapy.Field()
    #6.图片地址
    image_path = scrapy.Field()

'''
#定义一个item
course = CourseItem()
#赋值
course['title'] = "语文"
#取值
course['title']
course.get('title')
#获取全部键
course.keys()
#获取全部值
course.items()
'''