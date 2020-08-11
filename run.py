import requests
import os
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from multiprocessing import Process,Queue
base_url = "域名/.git/"
q = Queue(maxsize=99999)
# 爬取根域名
q.put("")

def file_tree():
    global q
    while not q.empty():
        path = q.get()
        url = "%s%s"%(base_url,path)
        print("file tree:%s" % url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for t in soup.find_all('a'):
            href = t.attrs["href"]
            if href == "../":
                print("../ continue")
                continue
            if href.endswith("/"):
                q.put("%s%s"%(path,href))
            else:
                file_url = "%s%s" % (url, href)
                dir_path = os.path.join('create/.git/',path)
                file_path = os.path.join(dir_path,href)
                if os.path.exists(file_path):
                    try:
                        with open(file_path,"r") as f:
                            data = f.read()
                            if "系统发生错误" in data:
                                continue
                    except UnicodeDecodeError:
                        pass

                r = requests.get(file_url)
                if r.status_code != 200:
                    print("error:%s"% file_url)
                if not os.path.exists(os.path.join('create',path)):
                    os.makedirs(os.path.join('create',path))
                print("download %s" % file_path)
                with open(file_path, 'wb') as f:
                    f.write(r.content)


q = file_tree()
pool = []
for i in range(16):
    pool.append(Thread(target=file_tree))
for i in pool:
    i.start()
for i in pool:
    i.join()
