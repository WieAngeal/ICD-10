import csv
import re
import xlwt
import xlrd
from xlutils.copy import copy


SERVER_URL = 'http://www.a-hospital.com'


def reader_csv_list(file):
    data = []
    with open(file, encoding='UTF-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        csv_header = next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return data


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()   # 初始化样式
    font = xlwt.Font()       # 为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    return style


def write_excel(path, data):
    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8', )
    # 创建sheet
    data_sheet = workbook.add_sheet('demo')
    # 生成第一行和第二行
    for i in range(len(data)):
        data_sheet.write(0, i, data[i], set_style('黑体', 220, False))

    workbook.save(path)


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


if __name__ == '__main__':
    file = 'hospital_info_test.csv'
    path = 'excel_hospital.xls'
    hos_data = reader_csv_list(file)
    p1 = re.compile(r"['](.*?)[']", re.S)
    data = []
    for hos in hos_data:
        s = re.findall(p1, hos[3][1:-1])
        s1 = [hos[0], hos[1], hos[2], s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]]
        data.append(s1)
    print(data)
    print(len(data))
    write_excel_xls_append(path, data)