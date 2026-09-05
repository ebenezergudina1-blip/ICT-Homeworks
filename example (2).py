# Created on iPad.

income = int(input("Please insert your income"))

def min(income):
    if income > 0 and income <=2000:
        print(f"No tax to be paid(0%).Net income = {income}")
    elif income > 2001 and income <=4000:
        print(f"tax exempt is 15%. Net income = {15/100*income}")
    elif income > 4001 and income <=7000:   
        print(f"tax exempt is 20%. Net income ={20/100 * income}")
    elif income > 7001 and income <=10000:   
        print(f"tax exempt is 25%. Net income ={25/100*income}")
    elif income > 10001 and income <=14000:   
        print(f"tax exempt is 30%. Net income ={30/100*income}")
    else:
        print(f"tax exempt is 35%. Net income ={35/100*income}")
        
min(income)



