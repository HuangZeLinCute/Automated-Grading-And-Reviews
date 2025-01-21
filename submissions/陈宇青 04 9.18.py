# 陈宇青
# 23大数据2班
# 2351020500204
# 2024.9.18

# 有技术，有能力，责任就越大，得做事。

# 1.让用户输入一个整数，输出这个整数的两倍
def demo1():
    num = int(input('请输入一个整数:'))
    print(f'{num}的两倍是：{num * 2}'  )
    




# 2.让用户输入一个浮点数，输出这个浮点数的四舍五入值（保留两位小数）。
def demo2():
    num2 = float(input('请输入一个三位及以上的小数：'))
    print(f'{num2}四舍五入值（保留两位小数）：{round(num2, 2)}')




# 3.	让用户输入一句话，输出这句话的长度。
def demo3():
    juzi = input('请输入一句话：')
    print(f'您输入的这句话的长度是：{len(juzi)}')



# 4.	让用户输入两个整数，用一个空格隔开，然后输出这两个整数的和。

def demo4():
    num4 = input('请输入两个整数，用一个空格隔开：')
    number = num4.split()
    if len(number) == 2:
        try: 
            num1, num2 = int(number[0]), int(number[1])
            print(f'两个整数的和是：{num1 + num2}')
        except ValueError: 
            print('输入包含非整数值，请确保输入的是两个用空格隔开的整数。')
    else:
        print('输入错误，请确保只输入了两个用空格隔开的整数。')




# 5.	让用户输入自己的姓名和年龄，用一个空格隔开，然后分别输出姓名和年龄。
def demo5():
    agename = input('请输入您的姓名和年龄，用一个空格隔开：')
    agename2 = agename.split()
    name, age = agename2[0], agename2[1]
    age2 = int(age)
    print(f'您的姓名是：{name}')
    print(f'您的年龄是：{age2}')

def main():
    demo1()
    print('=====================================')
    demo2()
    print('=====================================')
    demo3()
    print('=====================================')
    demo4()
    print('=====================================')
    demo5()



print('开始测试作业')
main()

