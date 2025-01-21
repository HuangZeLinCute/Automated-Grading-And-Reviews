'''
名字:陈哲聪
班级:23大数据技术2班
学号:2351020500206
2024.09.18
'''

def mul():
    num = int(input('请输入一个整数'))
    return num*2

def sishewuru():
    num = float(input('请输入一个小数'))
    return round(num,2)

def changdu():
    hua = input('随便说句话')
    return len(hua)

def sum():
    num1,num2 = input('请输入两个整数，之间用空格隔开').split()
    num1 = int(num1)
    num2 = int(num2)
    return num1+num2


def NameAge():
    name,age = input('请输入自己的姓名和年龄，之间用空格隔开').split()
    print("姓名：",name)
    print("年龄：",age)

def main():
    # 你这里要注意的是，你前四个函数都是采用了return将结果返回，你这里直接打印是可以的，如果不是进行打印输出的话，需要一个变量保存，
    print(mul())
    print(sishewuru())
    print(changdu())
    print(sum())
    NameAge()

main()


