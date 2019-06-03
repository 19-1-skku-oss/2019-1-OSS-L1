'''
2014314433
lee young suk
'''

x = input("Input a value for x : ") #Ask user input x value
y = input("Input a value for y : ") #Ask user input y value

if x.isdigit() ==True:#변수가 정수면 true 반환하는 함수임
    if y.isdigit() ==True:
        z=int(x)+int(y) #calculate z value by converting two strings above into int and adding them.
        w=int(x)*int(y) #calculate w value by converting two strings above into int and adding them.
        print(z) #print z
        print(w) #print w
    else:
          print("ERROR; either of them is non-numerical ")
    
else:
   print("ERROR: either of them is non-numerical ")
    
