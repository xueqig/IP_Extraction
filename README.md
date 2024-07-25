1、将DIA台账中：产品号码、业务IP、网关IP保存为一个CSV文档，并命名为input.csv。文档内容模板如下:
|  产品号码   | 业务IP  | 网关IP  |
|  ----  | ----  | ----  |
| 540DIA000705  | 112.XX.XX.XX/29 | 112.XX.XX.XX |
| 540DIA13542725  | 210.XX.XXX.XXX-210.XX.XXX.XXX | 210.XX.XXX.XXX |

2、自动提取IP:
python extract_ip.py
运行extract_ip.py，提取业务IP，运行结果会写入“ce_ip.csv”文档。

3、批量Ping测:
python fast_ping.py
运行fast_ping.py，对所有业务IP进行Ping测，运行结果会写入“Ping测结果.csv”文档。