import scrapy
#引入容器
from scrapytest.CourseItems import CourseItem

class MySpider(scrapy.Spider):
    #设置name（必须）
    name = "MySpider"
    #设定域名
    allowed_domains = ["imooc.com"]
    #填写入口爬取地址（必须）
    start_urls = ["http://www.imooc.com/course/list"]       #可以包括多个url
    #编写爬取方法,该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
    def parse(self, response):  #默认回调给parse函数
        #实例一个容器保存爬取的信息
        item = CourseItem()
        #这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        #先获取每个课程的div

        #       for box in response.xpath('//div[@class="moco-course-wrap"]/a[@target="_self"]'):
        for box in response.xpath('//div[@class="course-card-container"]/a[@target="_blank"]'):
            #获取每个div中的课程路径
            item['url'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]           #selector 用extract（）提取里面的内容,前面的 . 表示在box标签下找
            #获取div中的课程标题
            item['title'] = box.xpath('.//div[@class="course-card-content"]/h3/text()').extract()[0].strip()    #提取h3标签里面的内容
            #获取div中的标题图片地址
            item['image_url'] = "http:" + box.xpath('.//img[@class="course-banner lazy"]/@src').extract()[0]  #寻找所有含有属性class="course-banner lazy"的img标签，提取里面的src属性
            print(item['image_url'])
            #获取div中的学生人数
            item['student'] = box.xpath('.//span/text()').extract()[1]
            #获取div中的课程简介
            item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
            #返回信息
            yield item          #如果是request则加入爬取队列，如果是item类型则使用pipeline处理，其他类型则返回错误信息

        #url跟进开始
        #获取下一页的url信息
        url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()             # contains用法
        if url :
            #将信息组合成下一页的url
            page = 'http://www.imooc.com' + url[0]
            #返回url
            yield scrapy.Request(page, callback=self.parse)         #每抓取到一个网页，调用callback指向的方法
        #url跟进结束
