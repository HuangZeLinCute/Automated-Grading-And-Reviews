

'''
陈毓华
23大数据2班
2351020500205
'''

# 1.让用户输入一个整数，输出这个整数的两倍。
def damn1():
   num = int(input("请输入一个整数: ")) 
   print(f"{num}的两倍是：{num* 2}")
   

# 2.让用户输入一个浮点数，输出这个浮点数的四舍五入值（保留两位小数）。
def damn2():
   num2 = float(input("请输入一个浮点数: ")) 
print(f"{f}的四舍五入值是: {round(f, 2)}") # 这个f怎么写到里面了呢，咱这个写法就是f"{变量名}"除非你有个变量叫f，显然你没有。

# 3.让用户输入一句话，输出这句话的长度。
def damn3():  
    changdu = input("请输入一句话: ")  
    print(f"这句话的长度是: {len(changdu)}") 


# 4.让用户输入两个整数，用一个空格隔开，然后输出这两个整数的和。
def damn4():  
    nums = input("请输入两个整数，用一个空格隔开: ").split()  
    num1 = int(nums[0])  
    num2 = int(nums[1])  
    print(f"{num1}和{num2}的和是: {num1 + num2}") 


# 5.让用户输入自己的姓名和年龄，用一个空格隔开，然后分别输出姓名和年龄。
def damn5():  
    info = input("请输入你的姓名和年龄，用一个空格隔开: ").split()  
    name = info[0]  
    age = info[1]  
    print(f"姓名: {name}, 年龄: {age}") 


damn1()  
damn2()  
damn3()  
damn4()  
damn5()