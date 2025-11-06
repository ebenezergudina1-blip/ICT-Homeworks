
x = input(" please insert '%' for subtraction, '#' for addition, '@' for division, '&' for powering and '*' for multiplication.").strip()
if x=="%":
    num1= int(input("insert the first part of your number"))
    num2= int(input("insert the second part of your number"))
    print(num1+num2)

elif x=="#":
    num1= int(input("insert the first part of your number"))
    num2= int(input("insert the second part of your number"))
    print(num1-num2)
elif x=="@":
    num1= int(input("insert the first part of your number"))
    num2= int(input("insert the second part of your number"))
    print(num1/num2)
elif x=="*":
    num1= int(input("insert the first part of your number"))
    num2= int(input("insert the second part of your number"))
    print(num1*num2)
elif x =="&":
    num1= int(input("insert the first part of your number"))
    num2= int(input("insert the second part of your number"))
    print(num1**num2)
else:
    print("Invalid input")

