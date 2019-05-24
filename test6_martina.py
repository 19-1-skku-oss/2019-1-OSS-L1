SPY=float(input("Enter the amount invested in SPY: "))
QQQ=float(input("Enter the amount invested in QQQ: "))
EEM=float(input("Enter the amount invested in EEM: "))
VXX=float(input("Enter the amount invested in VXX: "))

total=SPY+QQQ+EEM+VXX


print("ETF PERCENTAGE: ")
print("{0:^6s} {1:^6s} {2:^6s} {3:^6s}".format("SPY", "QQQ", "EEM", "VXX"))
print("{0:6s} {1:6s} {2:6s} {3:6s}".format("------", "------", "------", "------"))
print("{0:6.2%} {1:6.2%} {2:6.2%} {3:6.2%}".format((SPY/total), (QQQ/total), (EEM/total), (VXX/total)))
print("TOTAL AMOUNT INVESTED: $%.2f" %total)


      
