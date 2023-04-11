from math import ceil,floor
from random import choice,randint
import os
from platform import system
 
class Unit:
    wildcard=False
    sp=[0]*7
    btm=0
    body=6
    damageTaken=0

    #shooting=9 unused
    
    stun=False
    uncon=False
    dead=False
    
    def __init__(self):
        initBody(self)
        initSP(self)

    def __init__(self,sp,body,wildcard):
        self.sp=sp
        self.body=body
        self.btm=bodyToBTM(self.body)
        self.wildcard=wildcard

    def stunMod(self):
        return floor((self.damageTaken-1)/5)

    def unconMod(self):#does not need to exist, just a macro for convinience
        return self.allNegative()

    def allNegative(self):
        return max(floor((self.damageTaken-1)/5)-3,0)
    
    def rollStun(self,silent=False):
        if(not self.stun):
            if(rollD10()>self.body-self.stunMod()):
                if(not silent):
                    print("*** STUN ***")
                self.stun=True
    
        if(self.stun and self.damageTaken>15 and not self.uncon):
            if(rollD10()>self.body-self.unconMod()):
                if(not silent):
                    print("-=- UNCON -=-")
                self.uncon=True

    def reset(self):
        self.sp=[0]*7
        self.body=6
        self.btm=2
        self.damageTaken=0
        self.stun=False
        self.uncon=False
        self.dead=False
        self.wildcard=False




############################ ^^^ CLASS ^^^  +imports lol

def dealDamage(unit,damage,index,bulletType,silent=False):
    global barrier,shotCount,dead,autostun

    sp=unit.sp
    btm=unit.btm
    damageTaken=unit.damageTaken
    dead=unit.dead
    wildcard=unit.wildcard

    if(not index in exposed):
        if(bulletType=="f"):
            if(damage>=barrier/2 and barrier>0):
                barrier-=1

        elif(bulletType=="b"):
            damage-=floor(barrier/2)
            if(damage+floor(barrier/2)>=floor(barrier/4) and barrier>0):
                barrier-=1

        else:#bullet type not full AP
            damage-=barrier
            if(damage+barrier>=barrier/2 and barrier>0):
                barrier-=1
    #end exposed
        
    if(bulletType=="f"):
        if(damage>=sp[index]/2 and sp[index]>0):
            if(not silent):
                print("-",end="")
            sp[index]-=1
        else:
            if(not silent):
                print(" ",end="")

    elif(bulletType=="k" or bulletType=="t" or bulletType=="b"):
        damage-=floor(sp[index]/2)
        if(damage+floor(sp[index]/2)>=floor(sp[index]/4) and sp[index]>0):
            if(not silent):
                print("-",end="")
            sp[index]-=1
        else:
            if(not silent):
                print(" ",end="")

    else:#normal
        damage-=sp[index]
        if(damage+sp[index]>=sp[index]/2 and sp[index]>0):
            if(not silent):
                print("-",end="")
            sp[index]-=1
        else:
            if(not silent):
                print(" ",end="")

    #end sp reduction and degredation
        
        
    if(index==0):#head
        if(not wildcard):#not wildcard
            if(bulletType!="b"):
                damage*=2

            if (damage>=8):
                if(not silent):
                    print(f"### INSTA-KILL, {damage} to head before BTM ###")
                dead=True

            if(bulletType=="b"):
                damage-=btm
            elif(damage>0):
                damage=max(1,damage-btm)

        else:#wildcard
            if(bulletType=="b"):
                damage=floor(damage/2)
                damage-=btm
            elif(damage>0):
                damage=max(1,damage-btm)

            if(damage>=8):
                if(not silent):
                    print(f"### INSTA-KILL, {damage} to head *before double* ###")
                dead=True

            damage*=2

    elif(damage>0):#not head AND damage exists
        if(bulletType=="b"):
            damage=floor(damage/2)
        
        if(not silent and not wildcard):
            if(damage>=8 and index>1):
                print(f"### CRITICAL INJURY TO {LOCATIONS[index].upper()} ###")
            if(damage>=15 and index==1):
                print(f"### CRITICAL INJURY TO TORSO ###")

        if(bulletType!="b"):
            damage=max(1,damage-btm)
        else:
            damage-=btm #stipulation for BTM does not apply to AP rounds
        
        if(not silent and wildcard):
            if(damage>=8 and index>1):
                print(f"### CRITICAL INJURY TO {LOCATIONS[index].upper()} ###")
            if(damage>=15 and index==1):
                print(f"### CRITICAL INJURY TO TORSO ###")
        
    shotCount+=1

    if(damage>0):
        if(autostun):
            unit.rollStun()
        damageTaken+=damage
        return damage

    return 0

############################ ^^^ BIG BUT LESS AWFUL DAMAGE FUNCTION ^^^  ##################################

#Macros
WINDOWS=system()=="Windows"
LOCATIONS=["Head","Torso","Larm","Rarm","Lleg","Rleg","Other"]
RANDLOCATION=[0,1,1,1,1,1,2,3,4,5]

#Program Logic (will be placed in main)
bulletType="normal"
shotCount=0
barrier=0
exposed=set()
autostun=False
hide=False

#status=set() < future plan for status flags (dynamic set)


############################ ^^^ Globals cause Im a TERRIBLE programmer

def askBulletType():
    return(input("""Ammo Types:
(N)/(Normal) - Standard Ammo
(B:AP) - SP treated as half, half damage through
(T:AP) - SP treated as half, full damage through (also called K:AP)
(F:AP) - SP ignored (still degraded), full damage through
    
Ammo Type: """).split(":")[0].lower())

def initBody(unit):
    temp=input("Set body: ")
    if(temp=="" or not temp.isnumeric()):
        temp=6
        print("defaulted to body: 6, btm: 2")
    unit.body=int(temp)
    unit.btm=bodyToBTM(unit.body)

def bodyToBTM(body):
    if(body>10):
        return 5
    elif(body<6):
        return ceil(body/2-1)
    else:
        return floor(body/2-1)

def printSP(unit):
    if(not hide):
        print(f"(SP) - [{unit.sp[0]}] [{unit.sp[1]}] [{unit.sp[2]}|{unit.sp[3]}] [{unit.sp[4]}|{unit.sp[5]}]  (BTM): {unit.btm}  (BODY): {unit.body}",end="")
    else:
        print(f"(SP) - [/] [/] [/|/] [/|/]  (BTM/BODY): ///",end="")

    if(unit.stunMod()>0):
        print(f"  Stun: -{unit.stunMod()}",end="")
    print()

def printBarrier(barrier,exposed):
    print(f"\n(BAR) Barrier SP: {barrier}")
    if(barrier>0):
        if(len(exposed)>0):
            print(f"(EXP) Exposed areas: {exposedString(exposed)}")
        else:
            print("(EXP) Exposed")

def exposedString(exposed):
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

def initSP(unit):
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

    for i in sp:
        if(not i.isnumeric()):
            print("@@SP INIT FAILURE@@")
            sp=[0]*7
            return

    sp=[int(i) for i in sp]

    unit.sp=sp

def processDamage(input):
    output=0
    input=str(input)

    try:
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
    
    except:
        print("@@FAILED DMG EVAL@@")
        return 0

    return output

def renderDamage(unit):
    i=0
    print(f"(DMG): {unit.damageTaken} - [",end="")
    for _ in range(unit.damageTaken):
        i+=1
        print("#",end="")
        if(i%10==0):
            print("][",end="")
        elif(i%5==0):
            print("|",end="")
        if(i==50):
            unit.dead=True
            break
    for _ in range(50-unit.damageTaken):
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

def saveState(unit):
    clr()
    name=input("Save name: ")
    data=f"{unit.wildcard};{autostun};{unit.sp[0]},{unit.sp[1]},{unit.sp[2]},{unit.sp[3]},{unit.sp[4]},{unit.sp[5]};{unit.body}"

    with open(f"{name}.txt", "w") as f:
        f.write(data)


def reset():#temp
    global autostun,shotCount,bulletType,barrier,exposed
    exposed=set()
    bulletType="normal"
    autostun=False
    shotCount=0
    barrier=0

def loadState(name,unit):
    global autostun
    try:
        with open(f"{name}.txt", "r") as f:
            data=f.read().split(";")

            reset()
            
            unit.wildcard=data[0]=='True'
            autostun=data[1]=='True'

            unit.body=int(data[3])
            unit.btm=bodyToBTM(unit.body)

            input_sp=[int(i) for i in data[2].split(",")]
            sp=[0]*7
            for i in range(len(input_sp)):
                if(i==6):
                    break
                sp[i]=input_sp[i]

            unit.sp=sp

    except:
        return False
    
    if(WINDOWS):
        os.system(f"title {name}")
    
    return True

def rollD10():
    d10=[1,2,3,4,5,6,7,8,9,10]
    total=0

    roll=choice(d10)
    total=roll

    if(roll==1):
        while(True):
            roll=choice(d10)
            total-=roll
            if(roll!=10):
                break

    elif(roll==10):
        while(True):
            roll=choice(d10)
            total+=roll
            if(roll!=10):
                break

    return total


def main():#### MAIN ####
    #To hide in main
    global bulletType,shotCount,barrier,exposed,autostun,hide

    unit=Unit()

    if(WINDOWS):
        os.system("title Unnamed DT")

    while(True):### INIT ###
        clr()
        temp=input("If loading from file, enter its name\nIf fresh instance, leave blank\n\n: ")
        if(temp!=""):
            if(loadState(temp)):
                break
        else:
            clr()
            initBody(unit)
            print()
            initSP()
            break

    undoSP=sp
    undoDMG=damageTaken
    undoBar=barrier
    undoShot=shotCount
    undoStun=stun
    undoUncon=uncon
    undoDead=dead

    while(True):### MAIN LOOP ###
        clr()
        if(wildcard or autostun or hide):
            if(wildcard):
                print("-=- *WILDCARD* -=-  ",end="")
            if(autostun):
                print("@--Autostun ON--@  ",end="")
            if(hide):
                print("// HIDDEN //  ",end="")
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
        printBarrier()
        print(f"""
(AM) Ammo: {bulletType.upper()}
(C) Called Shot
(R) Random Location

   (AUTO) (WILD) (HIDE)
(SAVE) (LOAD) (NEW) (UNDO)
        """)
        temp=input("Input Option: ").lower()
        clr()

        if(temp=="undo"):
            sp=list(undoSP)
            damageTaken=undoDMG
            barrier=undoBar
            shotCount=undoShot
            stun=undoStun
            uncon=undoUncon
            dead=undoDead
            continue
        else:
            undoSP=list(sp)
            undoDMG=damageTaken
            undoBar=barrier
            undoShot=shotCount
            undoStun=stun
            undoUncon=uncon
            undoDead=dead

        if(temp=="stun"):
            stun=not stun
            continue

        if(temp=="uncon"):
            uncon=not uncon
            continue

        if(temp=="dead"):
            dead=not dead
            continue

        if(temp=="hide"):
            hide=not hide
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
            initBody(unit)
            continue

        if(temp=="am"):
            bulletType=askBulletType()
            continue

        if(temp=="sht"):
            shotCount=int(input(f"Set shot count (old: {shotCount}): "))
            continue

        if(temp=="bar"):
            barrier=int(input(f"Set barrier (old: {barrier}): "))
            continue

        if(temp=="new"):
            unit=Unit()
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

if __name__=='__main__':
    main()