# encoding=UTF-8
import json
import sys,os,re
import logging
import xlrd

_logger = logging.getLogger(__name__)
__author__ = 'Gaoyu'

logging.basicConfig(level=logging.INFO,
                    filename='./log/log.txt',
                    filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

path = os.path.abspath(os.path.dirname(sys.argv[0]))
xls_list = path.replace('\\', '/')+'/xls/'

def read_excel_info():
    if os.path.isdir(xls_list):
        files_list = os.listdir(xls_list)
        # 同一IP，同一name，同一password，不同commond
        papers_list = []
        for x in files_list:
            # 不是_开头，不是.pyc结尾的！
            rr1 = re.compile(r'^_')
            rr2 = re.compile(r'.*.xls.?')
            # 匹配出excle文件
            if not rr1.findall(x) and rr2.findall(x):
                Url = xls_list + x
                # 找到文件打断循环
                papers_list.append(Url)
            else:
                pass
                # _logger.info('未检测到脚本仓库的excle！！！请求添加excle！')
        dict_commonds = {}
        for url in papers_list:
            if url:
                #打开Excel文件读取数据
                excel = xlrd.open_workbook(url)
                # 读取第一个sheet
                sh = excel.sheets()[0]

                nrows = sh.nrows
                ncols = sh.ncols
                if nrows <= 1:
                    raise '请检查excel信息(少于2行)!'
                # 取出第一行表头
                excel_fields = sh.row_values(0)
                for k in range(nrows):
                    data = {}
                    child = {}
                    commonds = []
                    if k == 0:
                        pass
                    elif k >= 1:
                        if dict_commonds.get(sh.row_values(k)[0]):
                            dict_commonds[sh.row_values(k)[0]]["commond"].append(sh.row_values(k)[3])
                        else:
                            child["name"] = sh.row_values(k)[1]
                            child["password"] = sh.row_values(k)[2]
                            commonds.append(sh.row_values(k)[3])
                            child["commond"] = commonds
                            print child
                            dict_commonds[sh.row_values(k)[0]] = child
                print dict_commonds
                _logger.info('%s', dict_commonds)
            else:
                pass
                # _logger.info('未检测到脚本仓库的脚本路径！！！请求添加脚本！')
    return json.dumps(dict_commonds)




if __name__ == "__main__":
    read_excel_info()


