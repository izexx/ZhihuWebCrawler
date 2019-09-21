#基于Scrapy的知乎爬虫  
##轮子哥的带逛图鉴分析:)  
首先这是我们轮子哥的主页：  
>https://www.zhihu.com/people/excited-vczh/activities  

直接request这个页面，只能得到页面的前面一小部分，这是因为知乎的页面是动态加载的，使用浏览器的开发者功能很容易猜到，我们的浏览器首先通过这个url来进行动态的加载：
>next: https://www.zhihu.com/api/v4/members/excited-vczh/activities?limit=7&session_id=1067720421109129216&after_id=1568941699&desktop=True

![](https://github.com/izexx/ZhihuWebCrawler/blob/master/zhihu_browser.png)
