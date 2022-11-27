import sys
import matplotlib.pyplot as plt
reg={'000':'R0','001':'R1','010':'R2','011':'R3','100':'R4','101':'R5','110':'R6','111':'FLAGS'}
regs={'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0,'FLAGS':'0000000000000000'}
############################## FUNCTION ###############################################
def Flags(f):
    if(f=='v'):
        regs['FLAGS']='0000000000001000'
    elif(f=='l'):
        regs['FLAGS']='0000000000000100'
    elif(f=='g'):
        regs['FLAGS']='0000000000000010'
    elif(f=='e'):
        regs['FLAGS']='0000000000000001'
    elif(f=='n'):
        regs['FLAGS']='0000000000000000'   
def dtb(n):                 
    n=int(n)
    val=bin(n).replace("0b", "")
    val=int(val)
    a=''
    while(val>0):         
        x=val%10     
        a+=str(x)
        val=val//10      
    c=16-len(a)
    while(c>0):
        a+='0'  
        c-=1     
    a=a[::-1]
    # print(a)
    return a
def btd(n):
    n=int(n)
    decimal = 0
    power = 1
    while n>0:
        rem = n%10
        n = n//10
        decimal += rem*power
        power = power*2
    return decimal   
def nott(n): #takes input as str
    a=''
    for i in n:
        if i=='0':
            a+='1'
        elif i=='1':
            a+='0'
    return a
def ieeetodeci(a): #accepts IEEE
    a = str(a)
    # print(a)
    b = a[0:3] #expo
    c = a[3:] #mantissa
    final = "1"+c
    b = int(b,2) 
    
    inn = final[0:b+1]
    deci = final[b+1:]
    sum1 = 0
    inn = int(inn,2)

    for i in range(0,len(deci)):
        sum1 += (int(deci[i]))*(2**((-1)*(i+1)))

    final1 = float(inn)+float(sum1)
    return(final1)
def dtbf(n):
    n=float(n)
    whole=int(n)
    dec=n-whole
    whole= bin((whole)).lstrip("0b") + "."
    if whole=='.':
        whole='0.'
    decimal=''
    # print(whole,dec)
    tmp=dec
    for i in range(5):
        tmp=tmp*2
        # print(tmp)
        if tmp<1:
            decimal+="0"
        elif tmp>1:
            decimal+="1"
            tmp-=1
        else:
            decimal+='1'
            break
    return (whole+decimal)

def exp_po(a):
    # print(a)
    # print("yah")
    
    a=str(a)
    c=0
    m=''
    if(a[1]=='.'):
       c=0 
    else:
       i=1
       while(a[i]!='.'):
        c+=1
        i+=1
    i=1
    for i in range(1,7,1):
        try:
            if(a[i]!='.'):
                m+=a[i]
        except :
            m+='0'  

    f=''      
               
    if c==0 or c==1 :
       f='00'+dtb((c))       
    elif c==2 or c==3:
        f='0'+dtb((c))  
    else:
        f=dtb((c))    
    return f+m
#######################################################################################
l=[]
for data in sys.stdin:
    if data!="\n":
        l.append(data)
for i in range(len(l)):
    l[i]=l[i].rstrip()
address=[]
for i in range(256): #address is stored in decimal
    address.append(0)
i=0
jumpflag=0
ou=[]
### Question 4 part
Pc=0
add=[]
noofcycle=[]
addre=0
def graph_plot(x, y):
    plt.scatter(x,y)
    plt.xlabel('Cycle number')
    plt.ylabel('Memory address acessed')
    plt.savefig("graph.jpg")
    plt.show()
while True:
    tmpRegs=[]
    if l[i][:5]=='10000':#add
        if((regs[reg.get(l[i][7:10])])+(regs[reg.get(l[i][10:13])])>65535):
            Flags('v')
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][7:10])]+(regs[reg.get(l[i][10:13])])-65536
        else:
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][7:10])]+regs[reg.get(l[i][10:13])]
            Flags('n')
    elif l[i][:5]=='10001':#sub
        if(regs[reg.get(l[i][7:10])]-regs[reg.get(l[i][10:13])]<0):
            Flags('v')
            regs[reg.get(l[i][13:])]=0
        else:
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][7:10])]-regs[reg.get(l[i][10:13])]
            Flags('n')
    if l[i][:5]=='00000':#addf
        tmpRegs.append(reg.get(l[i][7:10]))
        tmpRegs.append(reg.get(l[i][10:13]))
        tmpRegs.append(reg.get(l[i][13:]))
        # print(regs[reg.get(l[i][7:10])])
        # print(regs[reg.get(l[i][10:13])])
        if(((regs[reg.get(l[i][7:10])]))+((regs[reg.get(l[i][10:13])]))>31.5):
            Flags('v')
            regs[reg.get(l[i][13:])]=exp_po(31.5)
        else:
            regs[reg.get(l[i][13:])]=(regs[reg.get(l[i][7:10])])+(regs[reg.get(l[i][10:13])])
            Flags('n')
    elif l[i][:5]=='00001':#subf
        tmpRegs.append(reg.get(l[i][7:10]))
        tmpRegs.append(reg.get(l[i][10:13]))
        tmpRegs.append(reg.get(l[i][13:]))
        if(regs[reg.get(l[i][7:10])]-regs[reg.get(l[i][10:13])]<1):
            Flags('v')
            regs[reg.get(l[i][13:])]=0
        else:
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][7:10])]-regs[reg.get(l[i][10:13])]
            Flags('n')
    elif l[i][:5]=='10010':#movi
        regs[reg.get(l[i][5:8])]=(btd(l[i][-8::])) 
        Flags('n')
    elif l[i][:5]=='10011':#movr
        if reg.get(l[i][10:13])=='FLAGS':
            regs[reg.get(l[i][13:])]=btd(int(regs[reg.get(l[i][10:13])]))
        else:
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][10:13])]
        Flags('n')
    elif l[i][:5]=='00010':#movf
        tmpRegs.append(reg.get(l[i][5:8]))
        regs[reg.get(l[i][5:8])]=(ieeetodeci(l[i][-8::])) 
        # print(ieeetodeci(l[i][-8::]))
        Flags('n')
    elif l[i][:5]=='10100':#ld
        regs[reg.get(l[i][5:8])]=address[btd(l[i][8:])]
        Flags('n')
    elif l[i][:5]=='10101':#st
        address[btd(l[i][8:])]=regs.get(reg.get(l[i][5:8]))
        Flags('n')
    elif l[i][:5]=='10110':#mul 
        if(regs[reg.get(l[i][7:10])]*regs[reg.get(l[i][10:13])]>65535):
            Flags('v')
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][7:10])]*(regs[reg.get(l[i][10:13])])
            while regs[reg.get(l[i][13:])]>65535:
                regs[reg.get(l[i][13:])]-=65536
        else:
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][7:10])]*regs[reg.get(l[i][10:13])]
            Flags('n')
    elif l[i][:5]=='10111':#div
        regs['R0']=regs[reg.get(l[i][10:13])]//regs[reg.get(l[i][13:])]
        regs['R1']=regs[reg.get(l[i][10:13])]%regs[reg.get(l[i][13:])]
        Flags('n')
    elif l[i][:5]=='11000':#rsr
        regs[reg.get(l[i][5:8])]=int(regs[reg.get(l[i][5:8])])>>(btd(l[i][-8::])) 
        Flags('n')
    elif l[i][:5]=='11001':#lsr
        regs[reg.get(l[i][5:8])]=int(regs[reg.get(l[i][5:8])])<<(btd(l[i][-8::])) 
        Flags('n') 
    elif l[i][:5]=='11010':#xor
        regs[reg.get(l[i][13:])]=int(regs[reg.get(l[i][7:10])])^int(regs[reg.get(l[i][10:13])])
        Flags('n')
    elif l[i][:5]=='11011':#or
        regs[reg.get(l[i][13:])]=int(regs[reg.get(l[i][7:10])])|int(regs[reg.get(l[i][10:13])]) 
        Flags('n')
    elif l[i][:5]=='11100':#and
        regs[reg.get(l[i][13:])]=int(regs[reg.get(l[i][7:10])])&int(regs[reg.get(l[i][10:13])])
        Flags('n')
    elif l[i][:5]=='11101':#invert
        regs[reg.get(l[i][13:])]=btd(nott(dtb(regs[reg.get(l[i][10:13])])))
        Flags('n')
    elif l[i][:5]=='11110':#cmp
        if(regs[reg.get(l[i][10:13])]==regs[reg.get(l[i][13:])]):
            Flags('e')
        elif (regs[reg.get(l[i][10:13])]<regs[reg.get(l[i][13:])]):
            Flags('l')
        elif((regs[reg.get(l[i][10:13])]>regs[reg.get(l[i][13:])])):
            Flags('g')  
    elif l[i][:5]=='11111':#jump
            jumpflag=1
            Flags('n')
    elif l[i][:5]=='01100':#jlt
        if(regs['FLAGS']=='0000000000000100'):
             jumpflag=1
        Flags('n')
    elif l[i][:5]=='01101':#jgt
        if(regs['FLAGS']=='0000000000000010'):
             jumpflag=1
        Flags('n')
    elif l[i][:5]=='01111':#je
        if(regs['FLAGS']=='0000000000000001'):
             jumpflag=1
        Flags('n')
    elif l[i][:5]=='01010':
        Flags('n')
    if l[i][:5]=="00000" or l[i][:5]=="00001" or l[i][:5]=="00010":
        tmpList=['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']
        st=str(dtb(i))[-8:]+' '
        for j in tmpList:
            # print(regs.get(j))
            if j in tmpRegs:
                st+=exp_po(dtbf(regs.get(j)))+' '
            else:
                st+=dtb(regs.get(j))+' '
        st=st.rstrip()
        st+="\n"
        ou.append(st)
    else:
        ou.append(str(dtb(i))[-8:]+' '+str(dtb(regs.get('R0')))+' '+str(dtb(regs.get('R1')))+' '+str(dtb(regs.get('R2')))+' '+str(dtb(regs.get('R3')))+' '+str(dtb(regs.get('R4')))+' '+str(dtb(regs.get('R5')))+' '+str(dtb(regs.get('R6')))+' '+str(regs.get('FLAGS'))+'\n')
    if l[i][:5]=='01010':
        break
    if jumpflag==1:
        i=btd(l[i][-8::])-1
        jumpflag=0
    add.append(i)
    noofcycle.append(Pc)
    Pc+=1           #programcounter
    i=i+1           #address 
graph_plot(noofcycle, add)

for j in range(256):
    try:
        address[j]=l[j]+'\n'
    except IndexError:
        address[j]=str(dtb(address[j]))+'\n'
ou.extend(address)
for i in range(0,len(ou)):
        sys.stdout.write(ou[i])
