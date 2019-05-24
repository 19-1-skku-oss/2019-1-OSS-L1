data=open("data.txt","r")

for line in data:
    name,score=line.split(',')
    score=int(score)
    print("The score of %s is %d" %(name,score))

data.close()
