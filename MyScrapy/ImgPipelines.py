import scrapy
#from scrapy.contrib.pipeline.images import ImagesPipeline  过时
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
'''scrapy.contrib.pipeline.images.ImagesPipeline类的get_media_requests(item, info)会下载图片，
并把结果喂给item_completed()方法，结果是一个tuple，(success, image_info_or_failure)，
其中success是下载是否成功的bool，image_info_or_failure包括url、path和checksum三项。
其中，path就是相对于settings中的IMAGES_STORE的路径（含文件名）。
'''
class ImgPipeline(ImagesPipeline):
    #通过抓取的图片url获取一个Request用于下载
    def get_media_requests(self, item, info):   
        #返回Request根据图片url下载
        yield scrapy.Request(item['image_url'])

    #下载的图片，名字是其SHA1 hash值，这里重写自定义图片名字函数
    def file_path(self, request, response=None, info=None):
        #print("repuest:",request)               #<GET http://img2.sycdn.imooc.com/5991489e00019f5c06000338-240-135.jpg>
        newpath = request.url.split('/')[-1]
        return 'full/%s' % (newpath)

    #当下载请求（成功/失败）完成后执行该方法
    def item_completed(self, results, item, info): 
        #获取下载地址
        image_path = [x['path'] for ok, x in results if ok]    #results中有2个参数，如果第一个参数（bool）为true，则返回第二个参数（dict）的['path']的值
        #判断是否成功
        if not image_path:
            raise DropItem("---------Item contains no images!!!---------")
        #将地址存入item
        item['image_path'] = image_path
        return item





'''参考
重命名图片：https://segmentfault.com/q/1010000000413334
'''