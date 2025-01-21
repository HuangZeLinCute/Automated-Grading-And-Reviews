# ...
# 姓名：陈希婷
# 班级：大数据2班
# 学号：03
# ...

# 你这个只有部分的题目写成了函数化，请把每个题目都改成你第三题的写法

# 第一题
num = input("请输入一个整数：")
num = int(num)
double_num = num * 2
print (f"{num} 的两倍是 {double_num}")

# 第二题
num = input("请您输入一个浮点数：")
num = float (num) # 这地方也不应该有空格
rounded_num = round (num, 2)# 这个round和（）之间不应该有空格
print (f"{num} 四舍五入后保留两位小数是 {rounded_num}")

# 第三题
def main():
    name = input("请您输入一句话：")
    length = len(name)
    print(f"您输入的这句话的长度是：{length}")
    main() # 这里写错了，调用的时候应该没有缩进，。

# 第四题
input_str = input("请您输入两个整数：")
num0 = input_str.split()
num1 = int(num0[0])
num2 = int(num0[1])
sum_nums = num1 + num2
print(f"{num1} 和 {num2} 的和是 {sum_nums}")

# 第五题
input_str = input("请输入您的姓名和年龄：")
name, age = input_str.split()
print(f"姓名：{name}")
print(f"年龄：{age}")