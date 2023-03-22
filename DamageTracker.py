from math import ceil,floor
from random import choice,randint
import os
from platform import system
 
def dealDamage(damage,index):
    global barrier,sp,shotCount,bulletType,dead
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
                    print(f"-=- INSTA-KILL, {damage} to head before BTM -=-")
                    dead=True
                if(damage>0):
                    damage=max(1,damage-btm)

            else:#wildcard
                if(damage>0):
                    damage=max(1,damage-btm)
                if(damage>=8):
                    print(f"-=- INSTA-KILL, {damage} to head *before double* -=-")
                    dead=True
                damage*=2

        elif(damage>0):#not head AND damage exists
            if(not wildcard and damage>=8 and index>1):
                print(f"-=- CRITICAL INJURY TO {LOCATIONS[index].upper()} -=-")
            if(not wildcard and damage>=15 and index==1):
                print(f"-=- CRITICAL INJURY TO TORSO -=-")

            damage=max(1,damage-btm)

            if(wildcard and damage>=8 and index>1):
                print(f"-=- CRITICAL INJURY TO {LOCATIONS[index].upper()} -=-")
            if(wildcard and damage>=15 and index==1):
                print(f"-=- CRITICAL INJURY TO TORSO -=-")

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
                    print(f"-=- INSTA-KILL, {damage} to head before BTM -=-")
                    dead=True
                damage-=btm

            else:#wildcard
                damage=floor(damage/2)
                damage-=btm
                if(damage>=8):
                    print(f"-=- INSTA-KILL, {damage} to head *before double* -=-")
                    dead=True
                damage*=2

        else:#not head
            damage=floor(damage/2)
            
            if(not wildcard and damage>=8 and index>1):
                print(f"-=- CRITICAL INJURY TO {LOCATIONS[index].upper()} -=-")
            if(not wildcard and damage>=15 and index==1):
                print(f"-=- CRITICAL INJURY TO TORSO -=-")

            damage-=btm
            
            if(wildcard and damage>=8 and index>1):
                print(f"-=- CRITICAL INJURY TO {LOCATIONS[index].upper()} -=-")
            if(wildcard and damage>=15 and index==1):
                print(f"-=- CRITICAL INJURY TO TORSO -=-")

        #end bullet type == ap
    elif(bulletType=="knife" or bulletType=="k"):
        pass

    else:#Undefined bullet type
        bulletType="normal"
        return dealDamage(damage,index)
        
    shotCount+=1

    if(damage>0):
        return damage

    return 0

############################ ^^^ BIG BOTCHED AND SCARY DAMAGE FUNCTION ^^^  +imports lol

os.system("title Unnamed DT")
shotCount=0
damageTaken=0
wildcard=False
btm=0
sp=[0]*6
bulletType="normal" #normal,bullet,knife,
barrier=0
exposed=set()

WINDOWS=system()=="Windows"
LOCATIONS=["Head","Torso","Larm","Rarm","Lleg","Rleg"]
RANDLOCATION=[0,1,1,1,1,1,2,3,4,5]
temp=""

stun=False
uncon=False
dead=False

############################ ^^^ Globals cause Im a TERRIBLE programmer

def setBulletType():
    global bulletType
    bulletType=input("""Ammo Types
(N) - (Normal) Ammunition
(B) - (Bullet) Style AP
(K) - (Knife) Style AP
(F) - (Full) AP
    
Ammo Type: """).lower()

def setBody():
    global btm
    temp=input("Set body: ")
    if(temp==""):
        temp=6
        print("defaulted to body: 6, btm: 2")
    temp=int(temp)
    if(temp>10):
        btm=5
    elif(temp<6):
        btm=ceil(temp/2-1)
    else:
        btm=floor(temp/2-1)

def printSP():
    #print("(SP) - (Head) (Torso) (Larm) (Rarm) (Lleg) (Rleg)")
    print(f"(SP) - [{sp[0]}] [{sp[1]}] [{sp[2]}|{sp[3]}] [{sp[4]}|{sp[5]}]")

def initSP():
    global sp
    print("SP in order (Head)|(Torso)|(Larm)|(Rarm)|(Lleg)|(Rleg)")
    sp=[0]*6
    userin=input("format \"H,T,L,R,L,R\" or \"ALL\": ").split(",")
    if(len(userin)==1 and userin[0]!=""):
        sp=[int(userin[0])]*6
    else:
        for i in range(len(userin)):
            if(userin[i]==""):
                sp[i]=0
            else:
                sp[i]=int(userin[i])

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
        if(i==60):
            dead=True
            break
    for _ in range(60-damageTaken):
        i+=1
        print(".",end="")
        if(i%10==0):
            print("][",end="")
        elif(i%5==0):
            print("|",end="")
    print(f"\b (BTM): {btm}")

def clr():
    if WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def saveState():
    clr()
    name=input("Save name (no input for default load set): ")
    data=f"{wildcard};{sp[0]},{sp[1]},{sp[2]},{sp[3]},{sp[4]},{sp[5]};{btm}"

    with open(f"{name}.txt", "w") as f:
        f.write(data)

def loadState(name):
    global wildcard,btm,sp
    with open(f"{name}.txt", "r") as f:
        data=f.read().split(";")
        wildcard=data[0]
        btm=data[2]
        sp=data[1].split(",")


##################### INIT ########################################################################

clr()
temp=input("If loading from file, enter its name\nIf fresh instance, leave blank\n\nChoice: ")
if(temp!=""):
    loadState(temp)
else:
    clr()
    if(input("Wildcard(y/N): ").__contains__("y")):
        print("Wildcard")
        wildcard=True
    else:
        print("Non wildcard")
    print()
    setBody()
    print()
    initSP()

####################### MAIN LOOP ############################################################################

while(True):
    clr()
    if(wildcard):
        print("-=- *WILDCARD* -=-\n")
    renderDamage()
    if(stun or uncon or dead):
        print("Status: ",end="")
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
    if(len(exposed)>0):
        print(f"(EXP) Exposed areas: {exposedString()}")
    else:
        print("(EXP) Exposed")
    print(f"""
(AM) Ammo Type: {bulletType.upper()}
(SHT) Shot counter: {shotCount}

(C) Called Shot
(D) Damage to random location
(N) New Enemy

(SAVE) (LOAD)
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
            continue

    if(temp=="save"):
        saveState()
        continue

    if(temp=="load"):
        temp=input("Load file name (no.txt): ")
        loadState(f"{temp}.txt")
        continue

    if(temp=="sp"):
        initSP()
        continue

    if(temp=="dmg"):
        damageTaken=int(input(f"Set damage taken (old: {damageTaken}): "))
        continue

    if(temp=="btm"):
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

    if(temp=="n"):
        wildcard=False
        if(input("Wildcard(y/N): ").__contains__("y")):
            wildcard=True
        print()
        setBody()
        print()
        initSP()
        barrier=0
        bulletType="normal"
        damageTaken=0
        shotCount=0
        stun=False
        uncon=False
        dead=False


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
            print("-=- Press (x) to EXIT -=-")
            location=input("Location (Head,Torso,Larm,Rarm,Lleg,Rleg): ").lower()
            if(location.lower()=="x"):
                break
            damage=input("Damage: ")
            if(damage.lower()=="x"):
                break
            if(damage==""):
                print()
                continue

            i=1
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

    if(temp=="d"):
        iterations=0
        if(bulletType=="normal"):
            setBulletType()
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