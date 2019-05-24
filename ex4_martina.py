'''
2014314433
lee young suk
'''
userinputa=input("Enter the first integer : ")
userinputb=input("Enter the second integer : ")

if int(userinputa)%2==0 and int(userinputb)%2==0:
    print("Both a and b are even numbers")

elif int(userinputa)%2==0 or int(userinputb)%2==0:
    print("Either a or b is an even number")

else:
    print("Both a and b are odd numbers")
