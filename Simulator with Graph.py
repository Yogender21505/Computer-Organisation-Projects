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
################
while True:
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
    elif l[i][:5]=='10010':#movi
        regs[reg.get(l[i][5:8])]=(btd(l[i][-8::])) 
        Flags('n')
    elif l[i][:5]=='10011':#movr
        if reg.get(l[i][10:13])=='FLAGS':
            regs[reg.get(l[i][13:])]=btd(int(regs[reg.get(l[i][10:13])]))
        else:
            regs[reg.get(l[i][13:])]=regs[reg.get(l[i][10:13])]
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
 
