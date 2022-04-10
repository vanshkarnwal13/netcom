ip=input()
a,b,c,d=int(ip.split('.'))
i=int(input("enter 1 for classless and 2 for classfull: "))
j=int(input("enter the mask: "))
if i==2:
    m1,m2,m3,m4=int(j.split('.'))
    if(m1==225 and m2==0 and m3==0 and m4==0):
    elif(m1==225 and m2==225 and m3==0 and m4==0):
    elif(m1==225 and m2==225 and m3==225 and m4==0):
    elif(m1==225 and m2==225 and m3==225 and m4==225):
    else:
        print("invalid mask")
elif(i==1):
    ab=bin[a]
    bb=bin[b]
    cb=bin[c]
    db=bin[d]
    ipb=str(ab)+str(bb)+str(cb)+str(db)
    network_id=ipb[:j]
    