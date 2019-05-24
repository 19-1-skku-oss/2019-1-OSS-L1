etermA=int(input("Enter English Term A : "))
etermB=int(input("Enter English Term B : "))
mtermA=int(input("Enter Mathematics Term A : "))
mtermB=int(input("Enter Mathematics Term B : "))

esum=etermA+etermB
msum=mtermA+mtermB
eavg=esum/2
mavg=msum/2

print("{0:16} {1:<6} {2:<6} {3:8} {3:8}". format("","a","b","sum","average"))
print("{0:16s} {1:<6d} {2:<6d} {3:<8d} {3:<8.2f}". format("English",etermA,etermB, esum,eavg))
print("{0:16s} {1:<6d} {2:<6d} {3:<8d} {3:<8.2f}". format("Mathematics",mtermA,mtermB, msum,mavg))
