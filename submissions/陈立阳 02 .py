# ...
# 陈立阳
# 大数据2班
# 02
# 2024年9月19日12:52:10
# ...

# 1
def main():
    num = int(input("输入一个整数："))
    number = num * 2
    print(f"{num} 的两倍是 {number}")
# 2
def main():
    num = input("输入一个浮点数：")
    number = float(num)
    number = round(number, 2)
    print(f"{num} 四舍五入后保留两位小数是 {number}")
# 3
def main():
    a = input("输入一句话：")
    print(f"输入的句子长度为：{len(a)}")
# 4
def main():
    zhengshu = input("输入两个以空格分隔的整数：")
    a, b = map(int, zhengshu.split())
    sum = a + b
    print("两数和为", sum)
# 5
def main():
    h = input("请输入您的姓名和年龄（用空格分隔）：")
    name, age = h.split()
    print(f"姓名：{name}")
    print(f"年龄：{age}")

# 你定义了5个main函数，这里你只调用了一个，而且，所有的函数都是同一个名字，这里仅能调用最后一个。
main()




































































# 抄作业si码
# cly