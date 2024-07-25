import csv
import numpy as np
import pandas as pd
from ping3 import ping
import time
from concurrent.futures import ThreadPoolExecutor


# 读取业务IP
def read_data():
    data = pd.read_csv("ce_ip.csv", dtype={"产品号码": str, "IP": str}, encoding="gbk")
    cir_nums = np.array(list(data["产品号码"]))
    ips = np.array(list(data["IP"]))
    return cir_nums, ips

# 对业务IP进行Ping测
def ping_task(ips):
    with ThreadPoolExecutor(max_workers=500) as pool:
        results = pool.map(ping, ips)
    ip_status = list()
    for res in results:
        if type(res) == float:
            ip_status.append("yes")
        else:
            ip_status.append("no")
    return ip_status


# 将Ping测结果写入文档
def write_ans(cir_nums, ips, ip_status):
    output_file = open("Ping测结果.csv", "w", newline="")
    writer = csv.writer(output_file)
    writer.writerow(["产品号码", "IP", time.strftime('%y-%m-%d %H:%M:%S', time.localtime(time.time()))])
    for i in range(len(cir_nums)):
        writer.writerow([cir_nums[i], ips[i], ip_status[i]])
    output_file.close()


if __name__ == '__main__':
    print("start read files  " + time.strftime('%y-%m-%d %H:%M:%S', time.localtime(time.time())))
    cir_nums, ips = read_data()
    print(time.strftime("start ping .....  " + '%y-%m-%d %H:%M:%S', time.localtime(time.time())))
    results = ping_task(ips)
    print(time.strftime("start write files " + '%y-%m-%d %H:%M:%S', time.localtime(time.time())))
    write_ans(cir_nums, ips, results)
    print(time.strftime("ping end          " + '%y-%m-%d %H:%M:%S', time.localtime(time.time())))