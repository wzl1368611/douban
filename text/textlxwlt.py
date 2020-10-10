import xlwt
workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
sheet1 = workbook.add_sheet('sheet1')  # 创建工作表
# sheet1.write(0, 0, "hello world")
for i in range(1, 10):
    for j in range(1, 10):
        if j <= i:
            sheet1.write(i-1, j-1, str(j)+"X"+str(i)+"="+str(i*j))
workbook.save('student1.xls')

