John=["John", 20101111,"Software",[["Mathmatics",3.5],["Physics",3.6],["Chemistry",4.1]]]
Mary=["Mary", 20092222, "Software",[["Mathmatics",3.7],["Physics",2.5],["Chemistry",3.4]]]
Joe=["Joe", 20083333, "Business",[["Mathmatics",4],["Physics",4],["Chemistry",4.1]]]
Peter=["Peter", 20005555, "Economics",[["Mathmatics",4.2],["Physics",3.2],["Chemistry",2.6]]]
May=["May", 19984444, "Art",[["Mathmatics",3.6],["Physics",3.8],["Chemistry",2.9]]]

allstudent=[John,Mary,Joe,Peter,May]



tmsum=[John[3][0][1],Mary[3][0][1],Joe[3][0][1],Peter[3][0][1],May[3][0][1]]
mavg=sum(tmsum)/len(tmsum)

tpsum=[John[3][1][1],Mary[3][1][1],Joe[3][1][1],Peter[3][1][1],May[3][1][1]]
pavg=sum(tpsum)/len(tpsum)

tcsum=[John[3][2][1],Mary[3][2][1],Joe[3][2][1],Peter[3][2][1],May[3][2][1]]
cavg=sum(tcsum)/len(tcsum)

print("{0:<10s}{1:<16s}{2:<16s}{3:^16s}{4:5}".format("Name","Student ID","Department","Score",""))

i=0
while i<5: 
    print("{0:<10s}{1:<16d}{2:<16s}".format(allstudent[i][0], allstudent[i][1], allstudent[i][2]))
    for j in range(3,3,1):
        print("{3:<16s}{4:5.2f}".format(allstudent[i][j][0],allstudent[i][j][1]))
    i=i+1
                                           
                                                      

