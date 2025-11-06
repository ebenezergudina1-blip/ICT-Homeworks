# Created on iPad.

#print("Hello World!")

#sectionA= 20
#sectionB= 25
#sectionC= 25+5

#print(sectionA)
#print(sectionB)
#print(sectionC)

#sec_a = 20
#secb = secc = 25
#print(secc+5)
#sec_a,sec_b,sec_c= 20,25,2

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

