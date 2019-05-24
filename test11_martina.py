import random

states=open("StatesANC.txt","r")
i=0
j=0
wrong=0
state=[]
capital=[]
arrwrong=[]

    
while j<5:
    for line in states: #전체 리스트 받아와서 리스트로 저장해놓기
        list=line.split(',')
        state.insert(i,list)
        i+=1
    sample=random.choice(state) #랜덤으로 state하나 고르기
    idx=state.index(sample) #해당 state index저장
    print('What is the capital of',sample[0],'?')
    answer=input()
    if answer==sample[3]: #답이라면 그냥 continue
        arrwrong.insert(j,0)
    else:
        wrong+=1
        arrwrong.insert(j,1)
    state.remove(sample) #해당 데이터를 지워서 다음에 반복되지않게하기
    j+=1

print('You missed',wrong,'question(s).')



    

