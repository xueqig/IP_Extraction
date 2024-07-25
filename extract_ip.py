import numpy as np
import pandas as pd
import ipaddress
import csv


# 读取input.csv 文档，提取每条电路的业务IP（CE IP），返回所有的业务IP
def get_ce_ip():
    data = pd.read_csv("input.csv", encoding="gbk")
    prod_num = np.array(list(data["产品号码"]))
    ce_ip = np.array(list(data["业务IP"]))
    pe_ip = np.array(list(data["网关IP"]))

    out_prod_num = list()
    out_ce_ip = list()

    for idx in range(len(prod_num)):
        try:
            ip_range = ce_ip[idx]
            if "-" in ip_range:
                # 拆解此种形式的IP段：58.250.29.39-58.250.29.40
                start_ip, end_ip = ip_range.split("-")
                start_octets = start_ip.split(".")
                end_octets = end_ip.split(".")

                pe = pe_ip[idx].strip()
                for j in range(int(start_octets[-1]), int(end_octets[-1]) + 1):
                    ip = ".".join(start_octets[:-1] + [str(j)])
                    # 剔除PE IP
                    if str(ip) != pe:
                        out_prod_num.append(prod_num[idx])
                        out_ce_ip.append(ip)

            else:
                # 拆解此种形式的IP段：58.250.176.168/30
                # 去除空白字符
                if " " in ip_range:
                    ip_range = ip_range.replace(" ", "")
                if " " in ip_range:
                    ip_range = ip_range.replace(" ", "")
                if ip_range == "nan":
                    continue

                ip_network = ipaddress.ip_network(ip_range, strict=False)
                pe = pe_ip[idx].strip()
                for ip in ip_network.hosts():
                    # 剔除PE IP
                    if str(ip) != pe:
                        out_prod_num.append(prod_num[idx])
                        out_ce_ip.append(ip)
        except Exception as e:
            print(f"处理数据时出错: {e} - " + prod_num[idx])

    return out_prod_num, out_ce_ip


# 将业务IP写入ce_ip.csv
def write_data(out_prod_num, out_ce_ip):
    output_file = open("ce_ip.csv", "w", newline="")
    writer = csv.writer(output_file)
    writer.writerow(["产品号码", "IP"])
    for i in range(len(out_prod_num)):
        writer.writerow([out_prod_num[i], out_ce_ip[i]])
    output_file.close()


if __name__ == '__main__':
    out_prod_num, out_ce_ip = get_ce_ip()
    write_data(out_prod_num, out_ce_ip)
