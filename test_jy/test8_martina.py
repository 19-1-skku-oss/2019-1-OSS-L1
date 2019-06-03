user=input("User Input: ")
letter=0
number=0
symbol=0

for i in range(len(user)):
    if(user[i].isspace()):
         continue
    elif(user[i].isdigit()):
        number+=1
    elif(user[i].isalpha()):
        letter+=1
    else: symbol+=1



   
print("Letters:  %d" %letter)
print("Numbers:  %d" %number)
print("Symbol: %d" %symbol)
