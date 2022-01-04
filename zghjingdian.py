import scrapy
import re
import time
def data_write(list1):
    output = open('zghjingdian.xls','a+',encoding='gbk')
    #output.write('name\tgender\tstatus\tage\n')
    for i in range(len(list1)):
    	for j in range(len(list1[i])):
    		output.write(str(list1[i][j]))    #write函数不能写int类型的参数，所以使用str()转化
    		output.write('\t')   #相当于Tab一下，换一个单元格
    	output.write('\n')       #写完一行立马换行
    output.close()




class zghjingdian(scrapy.Spider): #需要继承scrapy.Spider类
    
    
    name = "zghjingdian" # 定义蜘蛛名
    
    start_urls = ['http://menpiao.tuniu.com/cat_0_0_0_0_0_0_1_1_1.html']
    
    
    def parse(self, response):
        
        list2 = []
        temp =response.xpath("//ul[@class='list_view']//li[@class='list_item']")
        time.sleep(5)#防止每一页爬取太快
        for v in temp:
            name = v.xpath("./h3/a/text()").extract()
            if(name):
                name = name[0].strip()
            else:
                name = "缺失"
            
            location1=v.xpath("./h3/span/a/text()").extract()
            #location="".join(location1)
            location=location1[0]
            if(location):
                location = location
            else:
                location = "缺失"
                
            manyidu=v.xpath("./p[@class='ticket']/strong/text()").extract()
            if(manyidu):
                manyidu = manyidu[0].strip()
            else:
                manyidu = "缺失"
            
            dianpingshuliang=v.xpath("./p[@class='ticket']/span/strong/text()").extract()
            if(dianpingshuliang):
                dianpingshuliang = dianpingshuliang[0].strip()
            else:
                dianpingshuliang = "缺失"
            
            jutididian=v.xpath("./p[@class='mp_addr']/text()").extract()
            if(jutididian):
                jutididian = jutididian[0].strip()
            else:
                jutididian = "缺失" 
           
            price=v.xpath("./div[@class='attri_price']/span[@class='price f_yh']/em/text()").extract()
            if(price):
                price = price[0].strip()
            else:
                price = "缺失"   
            list1 = []
            list1.append(name)
            list1.append(location)
            list1.append(manyidu)
            list1.append(dianpingshuliang)
            list1.append(jutididian)
            list1.append(price)
                      
            list2.append(list1)
                
      
        #write_excel_xls_append(zghjingdian.file_name_excel,list2)
        data_write(list2)
        response.css('a.page_next ').extract()[0].split('"')[5]
        
        next_page ="http://menpiao.tuniu.com"+response.css('a.page_next').extract()[0].split('"')[5]  
        if next_page is not None: 
            next_page = response.urljoin(next_page)
            zghjingdian.start_urls[0] = next_page
            yield scrapy.Request(next_page, callback=self.parse)
            
