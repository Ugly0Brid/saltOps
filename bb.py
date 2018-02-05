16:13:39
Ugly bird 2018/1/6 16:13:39


对方已成功接收了您发送的离线文件“aa.py”(938.00B)。
16:22:17
python小白 2018/1/6 16:22:17
那这个哪里有线程？

Ugly bird 2018/1/6 16:22:52
安我最后发给你的那个写

python小白 2018/1/6 16:23:00
啊啊

python小白 2018/1/6 16:23:47
那个是线程？

python小白 2018/1/6 16:23:55
这个5？

python小白 2018/1/6 16:23:52


Ugly bird 2018/1/6 16:24:04
是的
16:27:27
python小白 2018/1/6 16:27:27


python小白 2018/1/6 16:27:35
这里就没有0了呜呜

Ugly bird 2018/1/6 16:27:38


Ugly bird 2018/1/6 16:28:06
这个地方先这样写
16:30:01
python小白 2018/1/6 16:30:01


python小白 2018/1/6 16:30:06
这不就重复了？

Ugly bird 2018/1/6 16:30:28


Ugly bird 2018/1/6 16:30:31
这样写

python小白 2018/1/6 16:31:11
我就是想让循环的哪里多一个查询大于0的

Ugly bird 2018/1/6 16:31:53
你先实现功能在说吧

python小白 2018/1/6 16:32:01
。。。
16:32:17
python小白 2018/1/6 16:32:17


python小白 2018/1/6 16:32:20
可以了

Ugly bird 2018/1/6 16:33:51


python小白 2018/1/6 16:34:04
。。。
16:40:06
python小白 2018/1/6 16:40:06


python小白 2018/1/6 16:40:13
这获取到了全部的imageurl

python小白 2018/1/6 16:40:22
是不是直接取消费者里面直接下载

Ugly bird 2018/1/6 16:41:25


python小白 2018/1/6 16:41:37
？

python小白 2018/1/6 16:41:39
看不懂

python小白 2018/1/6 16:41:51


python小白 2018/1/6 16:42:01
我查询出所有的url饿了
16:42:49
Ugly bird 2018/1/6 16:42:49


python小白 2018/1/6 16:43:37
然后？

python小白 2018/1/6 16:43:48
报错了

python小白 2018/1/6 16:43:44

16:45:05
Ugly bird 2018/1/6 16:45:05
import random,threading,time,queue,pymysql,urllib.request
# 生产者
class Producer(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self,name=name)
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd="ok", db="designs", charset="utf8")
    def run(self):
        # 操作数据库
        # select * from table_name
        for i in range(0,72000,2000):
            cccccc = self.db.cursor()
            sq1 = "select * from lianxi where id>{id}".format(id=str(i))
            cccccc.execute(sq1)
            chazhao=cccccc.fetchall()
            q.put(chazhao)
            # for x in chazhao:
                # image=x[1]
                # image1=str(image).replace("[","").replace("]","").split(",")
                # for r in image1:
                    # q.put(r)
# 消费之
class Consumer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self,name=name)

    def run(self):
        # 获取url
        while True:
            chazhao = q.get()
             for x in chazhao:
                image=x[1]
                image1=str(image).replace("[","").replace("]","").split(",")
                for r in image1:
                    print(r)


q = queue.Queue()
    
procucer = Producer("Producer")
procucer.start()
for i in range(35):
    consumer = Consumer("Consumer")
    consumer.start()
