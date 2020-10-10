import sqlite3

conn = sqlite3.connect("test.db")
print("成功打开数据库")
cursor = conn.cursor()  # 获取目标
sql = '''
    create table company
        ( id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real);

'''

sql2 = '''
    insert into company(name,age,address,salary) values ("林祥林",20,"广西",5000)

'''

# ('黄林林','20','广西',5000)
sql3 = '''                           
    insert into company (name,age,address,salary) values ("周蝶",20,"广西",5000)

'''
sql4 = '''
    select * from company
'''
cursor.execute(sql4)  # 执行sql语句
for row in cursor:
    print("id=", row[0])
    print("name=", row[1])
    print("age=", row[2])
    print("address=", row[3])
    print("salary=", row[4], "\n")
conn.commit()
conn.close()
print("查询表数据成功")
