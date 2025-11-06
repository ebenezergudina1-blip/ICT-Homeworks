# Created on iPad.

user = input("please insert the type of unit to convert to meters, choices include: mm, cm, hm and km:").lower().strip()
number= float(input("Insert a number"))
li = ['km','mm','hm','cm']
def unit (number):
    if user not in li:
        print("Invalid input!")
    elif user == "km":
        print(f"Answer:{1000*number} meters")
    elif user == "mm":
        print(f"Answer:{1/1000* number} meters")
    elif user == "cm":
        print(f"Answer:{1/100*number} meters")
    elif user == "hm":
        print(f"Answer:{100*number} meters")
        
unit(number)
    
    