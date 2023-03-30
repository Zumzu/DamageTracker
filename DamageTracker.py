from math import ceil,floor
from random import choice,randint
import os
from platform import system
 
def dealDamage(damage,index):
    global barrier,sp,shotCount,bulletType,dead,autostun
    if(bulletType=="normal" or bulletType=="n" or bulletType=="knife" or bulletType=="k" or bulletType=="f" or bulletType=="full"):
        
        if(not index in exposed):
            if(bulletType=="f" or bulletType=="full"):
                if(damage>=barrier/2 and barrier>0):
                    barrier-=1
            else:#bullet type not full AP
                damage-=barrier
                if(damage+barrier>=barrier/2 and barrier>0):
                    barrier-=1
        
        if(bulletType=="f" or bulletType=="full"):
            if(damage>=sp[index]/2 and sp[index]>0):
                sp[index]-=1
        elif(bulletType=="knife" or bulletType=="k"):
            damage-=floor(sp[index]/2)
            if(damage+floor(sp[index]/2)>=floor(sp[index]/4) and sp[index]>0):
                sp[index]-=1
        else:#normal
            damage-=sp[index]
            if(damage+sp[index]>=sp[index]/2 and sp[index]>0):
                sp[index]-=1
        
        if(index==0):#head
            if(not wildcard):#not wildcard
                damage*=2
                if (damage>=8):
                    print(f"### INSTA-KILL, {damage} to head before BTM ###")
                    dead=True
                if(damage>0):
                    damage=max(1,damage-btm)

            else:#wildcard
                if(damage>0):
                    damage=max(1,damage-btm)
                if(damage>=8):
                    print(f"### INSTA-KILL, {damage} to head *before double* ###")
                    dead=True
                damage*=2

        elif(damage>0):#not head AND damage exists
            if(not wildcard and damage>=8 and index>1):
                print(f"### CRITICAL INJURY TO {LOCATIONS[index].upper()} ###")
            if(not wildcard and damage>=15 and index==1):
                print(f"### CRITICAL INJURY TO TORSO ###")

            damage=max(1,damage-btm)

            if(wildcard and damage>=8 and index>1):
                print(f"### CRITICAL INJURY TO {LOCATIONS[index].upper()} ###")
            if(wildcard and damage>=15 and index==1):
                print(f"### CRITICAL INJURY TO TORSO ###")

    elif(bulletType=="bullet" or bulletType=="b"):

        if(not index in exposed):
            damage-=floor(barrier/2)
            if(damage+floor(barrier/2)>=floor(barrier/4) and barrier>0):
                barrier-=1

        damage-=floor(sp[index]/2)
        if(damage+floor(sp[index]/2)>=floor(sp[index]/4) and sp[index]>0):
            sp[index]-=1

        if(index==0):#head
            if(not wildcard):#not wildcard
                if (damage>=8):
                    print(f"### INSTA-KILL, {damage} to head before BTM ###")
                    dead=True
                damage-=btm

            else:#wildcard
                damage=floor(damage/2)
                damage-=btm
                if(damage>=8):
                    print(f"### INSTA-KILL, {damage} to head *before double* ###")
                    dead=True
                damage*=2

        else:#not head
            damage=floor(damage/2)
            
            if(not wildcard and damage>=8 and index>1):
                print(f"### CRITICAL INJURY TO {LOCATIONS[index].upper()} ###")
            if(not wildcard and damage>=15 and index==1):
                print(f"### CRITICAL INJURY TO TORSO ###")

            damage-=btm
            
            if(wildcard and damage>=8 and index>1):
                print(f"### CRITICAL INJURY TO {LOCATIONS[index].upper()} ###")
            if(wildcard and damage>=15 and index==1):
                print(f"### CRITICAL INJURY TO TORSO ###")

        #end bullet type == ap
    elif(bulletType=="knife" or bulletType=="k"):
        pass

    else:#Undefined bullet type
        bulletType="normal"
        return dealDamage(damage,index)
        
    shotCount+=1

    if(damage>0):
        if(autostun):
            rollStun()
        return damage

    return 0

############################ ^^^ BIG BOTCHED AND SCARY DAMAGE FUNCTION ^^^  +imports lol

WINDOWS=system()=="Windows"
LOCATIONS=["Head","Torso","Larm","Rarm","Lleg","Rleg"]
RANDLOCATION=[0,1,1,1,1,1,2,3,4,5]

shotCount=0
damageTaken=0
wildcard=False
btm=0
body=6
sp=[0]*7
bulletType="normal" #normal,bullet,knife,
barrier=0
exposed=set()

if(WINDOWS):
    os.system("title Unnamed DT")

temp=""

autostun=False
stun=False
uncon=False
dead=False

############################ ^^^ Globals cause Im a TERRIBLE programmer

def setBulletType():
    global bulletType
    bulletType=input("""Ammo Types:
(N)/(Normal) - Standard Ammo
(B)/(Bullet) - SP treated as half, half damage through
(K)/(Knife) - SP treated as half, full damage through
(F)/(Full) - SP ignored (still degraded), full damage through
    
Ammo Type: """).lower()

def setBody():
    global btm,body
    temp=input("Set body: ")
    if(temp==""):
        temp=6
        print("defaulted to body: 6, btm: 2")
    temp=int(temp)
    body=temp
    if(temp>10):
        btm=5
    elif(temp<6):
        btm=ceil(temp/2-1)
    else:
        btm=floor(temp/2-1)

def printSP():
    print(f"(SP) - [{sp[0]}] [{sp[1]}] [{sp[2]}|{sp[3]}] [{sp[4]}|{sp[5]}]  (BTM): {btm}  (BODY): {body}",end="")
    if(floor((damageTaken-1)/5)>0):
        print(f"  Stun: -{floor((damageTaken-1)/5)}",end="")
    print()

def initSP():
    global sp
    sp=[0]*7
    userin=input("SP format \"H,T,L,R,L,R\", \"H,T,A,L\", \"H,T/A,L\", \"H,T/A\" or \"ALL\"\nSP: ").split(",")
    if(len(userin)==1 and userin[0]!=""):
        sp=[userin[0]]*7
    elif(len(userin)==2):
        sp[0]=userin[0]
        sp[1],sp[2],sp[3]=userin[1],userin[1],userin[1]
    elif(len(userin)==3):
        sp[0]=userin[0]
        sp[1],sp[2],sp[3]=userin[1],userin[1],userin[1]
        sp[4],sp[5]=userin[2],userin[2]
    elif(len(userin)==4):
        sp[0]=userin[0]
        sp[1]=userin[1]
        sp[2],sp[3]=userin[2],userin[2]
        sp[4],sp[5]=userin[3],userin[3]
    else:
        for i in range(len(userin)):
            if(i==6):
                break
            if(userin[i]==""):
                sp[i]=0
            else:
                sp[i]=userin[i]
    sp=[int(i) for i in sp]

def exposedString():
    global exposed
    output=""
    if(0 in exposed):
        output+="(Head) "
    if(1 in exposed):
        output+="(Torso) "
    if(2 in exposed):
        output+="(Larm) "
    if(3 in exposed):
        output+="(Rarm) "
    if(4 in exposed):
        output+="(Lleg) "
    if(5 in exposed):
        output+="(Rleg) "
    return output

def processDamage(input):
    output=0
    input=str(input)

    input=input.lower().strip().split("+")

    for item in input:
        if(item.__contains__("d")):
            multiple,dieType=item.split("d")
            if(multiple==""):
                multiple=1
            for _ in range(int(multiple)):
                output+=randint(1,int(dieType))
            
        else:#its just a number
            output+=int(item)

    return output

def renderDamage():
    global dead,btm
    i=0
    print(f"(DMG): {damageTaken} - [",end="")
    for _ in range(damageTaken):
        i+=1
        print("#",end="")
        if(i%10==0):
            print("][",end="")
        elif(i%5==0):
            print("|",end="")
        if(i==50):
            dead=True
            break
    for _ in range(50-damageTaken):
        i+=1
        print(".",end="")
        if(i%10==0):
            print("][",end="")
        elif(i%5==0):
            print("|",end="")
    print(f"\b (SHT): {shotCount}")

def clr():
    if WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def saveState():
    clr()
    name=input("Save name (no input for default load set): ")
    data=f"{wildcard};{autostun};{sp[0]},{sp[1]},{sp[2]},{sp[3]},{sp[4]},{sp[5]};{body}"

    with open(f"{name}.txt", "w") as f:
        f.write(data)

def reset():
    global wildcard,autostun,btm,body,sp,stun,uncon,dead,damageTaken,shotCount,bulletType,barrier,exposed
    exposed=set()
    bulletType="normal"
    stun=False
    uncon=False
    dead=False
    wildcard=False
    autostun=False
    sp=[0]*7
    body=6
    btm=2
    damageTaken=0
    shotCount=0
    barrier=0


def loadState(name):
    global wildcard,autostun,btm,body,sp
    try:
        with open(f"{name}.txt", "r") as f:
            data=f.read().split(";")

            reset()
            
            wildcard=data[0]
            autostun=data[1]

            body=int(data[3])
            if(body>10):
                btm=5
            elif(body<6):
                btm=ceil(body/2-1)
            else:
                btm=floor(body/2-1)

            input_sp=[int(i) for i in data[2].split(",")]
            sp=[0]*7
            for i in range(len(input_sp)):
                if(i==6):
                    break
                sp[i]=input_sp[i]

    except:
        return False
    
    return True

def rollStun():
    global stun,uncon
    d10=[1,2,3,4,5,6,7,8,9,10]
    if(not stun):
        if(choice(d10)>body-floor((damageTaken-1)/5)):
            print("*** STUN ***")
            stun=True
    if(stun and damageTaken>15 and not uncon):
        if(choice(d10)>body-floor((damageTaken-1)/5)-3):
            print("-=- UNCON -=-")
            uncon=True
        

##################### INIT ########################################################################

while(True):
    clr()
    temp=input("If loading from file, enter its name\nIf fresh instance, leave blank\n\n: ")
    if(temp!=""):
        if(loadState(temp)):
            break
    else:
        clr()
        setBody()
        print()
        initSP()
        break

####################### MAIN LOOP ############################################################################

while(True):
    clr()
    if(wildcard or autostun):
        if(wildcard):
            print("-=- *WILDCARD* -=-  ",end="")
        if(autostun):
            print("@--Autostun ON--@",end="")
        print("\n")
    
    renderDamage()
    if(floor((damageTaken-1)/5)-3>0):
            print(f"@ ALL ROLLS -{floor((damageTaken-1)/5)-3} @")
    if(stun or uncon or dead):
        print("\nStatus: ",end="")
        if(stun):
            print("*STUN* ",end="")
        if(uncon):
            print("-=-UNCON-=- ",end="")
        if(dead):
            print("###DEAD### ",end="")
        print()
        
    print()
    printSP()
    print(f"\n(BAR) Barrier SP: {barrier}")
    if(barrier>0):
        if(len(exposed)>0):
            print(f"(EXP) Exposed areas: {exposedString()}")
        else:
            print("(EXP) Exposed")
    print(f"""
(AM) Ammo: {bulletType.upper()}
(C) Called Shot
(R) Random Location

(SAVE) (LOAD) (NEW) (AUTO) (WILD)
    """)
    temp=input("Input Option: ").lower()
    clr()

    if(temp=="stun"):
        stun=not stun
        continue

    if(temp=="uncon"):
        uncon=not uncon
        continue

    if(temp=="dead"):
        dead=not dead
        continue

    if(temp=="status"):
        input("Try typing the name of the status!\n(STUN) (UNCON) (DEAD)\nEnter to continue...")
        continue

    if(temp=="exp"):
        while(True):
            clr()
            print("-=- (X) to EXIT -=-")
            print("(ALL) - (Head)|(Torso)|(Larm)|(Rarm)|(Lleg)|(Rleg)")
            print(f"Currently Exposed: {exposedString()}")
            userIn=input("\nEnter location to toggle: ").lower()
            if(userIn=="x" or userIn==""):
                break
            if(userIn=="all"):
                if(len(exposed)==0):
                    exposed={0,1,2,3,4,5}
                else:
                    exposed=set()
            elif(userIn=="head"):
                if(0 in exposed):
                    exposed.remove(0)
                else:
                    exposed.add(0)
            elif(userIn=="torso"):
                if(1 in exposed):
                    exposed.remove(1)
                else:
                    exposed.add(1)
            elif(userIn=="larm"):
                if(2 in exposed):
                    exposed.remove(2)
                else:
                    exposed.add(2)
            elif(userIn=="rarm"):
                if(3 in exposed):
                    exposed.remove(3)
                else:
                    exposed.add(3)
            elif(userIn=="lleg"):
                if(4 in exposed):
                    exposed.remove(4)
                else:
                    exposed.add(4)
            elif(userIn=="rleg"):
                if(5 in exposed):
                    exposed.remove(5)
                else:
                    exposed.add(5)

        continue

    if(temp=="name"):
        if(WINDOWS):
            os.system("title "+input("Enter new window name: ").upper())
        else: #linux
            os.system("set-title "+input("Enter new window name: ").upper())
        continue

    if(temp=="save"):
        saveState()
        continue

    if(temp=="load"):
        temp=input("Load file name (no '.txt'): ")
        loadState(temp)
        continue

    if(temp=="sp"):
        initSP()
        continue

    if(temp=="dmg"):
        damageTaken=int(input(f"Set damage taken (old: {damageTaken}): "))
        continue

    if(temp=="btm" or temp=="body"):
        setBody()
        continue

    if(temp=="am"):
        setBulletType()
        continue

    if(temp=="sht"):
        shotCount=int(input(f"Set shot count (old: {shotCount}): "))
        continue

    if(temp=="bar"):
        barrier=int(input(f"Set barrier (old: {barrier}): "))
        continue

    if(temp=="new"):
        reset()
        setBody()
        print()
        initSP()
        continue

    if(temp=="auto" or temp=="autostun"):
        autostun=not autostun
        continue

    if(temp=="wild" or temp=="wildcard"):
        wildcard=not wildcard
        continue

    if(temp=="head"):
        sp[0] = input("Set head SP: ")
        continue
    if(temp=="torso"):
        sp[1] = input("Set torso SP: ")
        continue
    if(temp=="larm"):
        sp[2] = input("Set left arm SP: ")
        continue
    if(temp=="rarm"):
        sp[3] = input("Set right arm SP: ")
        continue
    if(temp=="lleg"):
        sp[4] = input("Set left leg SP: ")
        continue
    if(temp=="rleg"):
        sp[5] = input("Set right leg SP: ")
        continue

    if(temp=="c"):
        if(bulletType=="normal"):
            setBulletType()
        while(True):
            clr()
            print(f"Current ammo type: {bulletType.upper()}")
            print("-=- Press (x) to EXIT -=-")
            location=input("Location (Head,Torso,Larm,Rarm,Lleg,Rleg,Other): ").lower()
            if(location=="x"):
                break
            if(location=="other"):
                temp=input("Location SP: ")
                sp[6]=0
                if(temp.isnumeric() and not temp==""):
                    sp[6]=int(temp)
            damage=input("Damage: ")
            if(damage=="x"):
                break
            if(damage==""):
                print()
                continue

            if(location=="other"):
                locSP=sp[6]
                output=dealDamage(processDamage(damage),6)
                damageTaken+=output
                if(input(f"Dealt {output} damage to {locSP} SP, new SP is {sp[6]}, ENTER to Continue\n").lower()=="x"):
                    break
                continue

            i=0
            if(location=="head"):
                i=0
            elif(location=="torso"):
                i=1
            elif(location=="larm"):
                i=2
            elif(location=="rarm"):
                i=3
            elif(location=="lleg"):
                i=4
            elif(location=="rleg"):
                i=5

            output=dealDamage(processDamage(damage),i)
            damageTaken+=output
            if(input(f"Dealt {output} damage to {LOCATIONS[i]}, ENTER to Continue\n").lower()=="x"):
                break
        continue

    if(temp=="r"):
        iterations=0
        if(bulletType=="normal"):
            setBulletType()
        print(f"Current ammo type: {bulletType.upper()}")
        print("-=- Press (x) to EXIT -=-\n")
        while(True):
            i=choice(RANDLOCATION)
            if(iterations<=0):
                print(f"Damage to {LOCATIONS[i]}")
                damage=input("Damage: ")

                if(damage.lower()=="x"):
                    break
                if(damage==""):
                    print()
                    continue
                if(damage.__contains__("*")):
                    damage,iterations=damage.split("*")
                    iterations=int(iterations)-1

            else:#iterating
                iterations-=1
            
            output=dealDamage(processDamage(damage),i)
            damageTaken+=output
            print(f"Dealt {output} damage to {LOCATIONS[i]}\n")