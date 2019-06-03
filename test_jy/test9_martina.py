league=open("ALE.txt","r")

print("Team\tWon\tLost\tPercentage")

for line in league:
    data=line.split(',')
    Won=int(data[1])
    Lost=int(data[2])
    Percentage=Lost/Won
   

Sort(data)
print(data)
print("%s\t%d\t%d\t%.3f" data[0],Won,Lost,Percentage)
