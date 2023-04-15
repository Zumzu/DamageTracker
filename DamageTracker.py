from math import ceil,floor
from random import choice,randint
import os
from platform import system
 
class Unit:
    name="Unnamed"
    wildcard=False
    sp=[0]*7
    btm=0
    body=6
    damageTaken=0

    #shooting=9 unused
    
    stun=False
    uncon=False
    dead=False
    
    def __init__(self,sp=[-1],body=6,wildcard=False):
        self.btm=2
        if(sp[0]==-1):
            initBody(self)
            initSP(self)
        else:
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

def dealDamage(unit,damage,index,silent=False):
    global barrier,shotCount,autostun,bulletType

    sp=unit.sp
    btm=unit.btm
    damageTaken=unit.damageTaken
    wildcard=unit.wildcard

    targetBar=int(barrier)
    targetSP=int(sp[index])

    if(bulletType=="f"):
        targetBar=0
        targetSP=0

    elif(bulletType=="b" or bulletType=="k" or bulletType=="t"):
        targetBar*=0.5
        targetSP*=0.5

    elif(bulletType=="hm"):
        targetBar*=2/3
        targetSP*=2/3

    elif(bulletType=="sm"):
        targetBar*=1/3
        targetSP*=1/3
    
    elif(bulletType=="hp"):
        targetBar*=1.5
        targetSP*=1.5

    elif(bulletType=="roland"):#SPECIAL
        targetBar*=0.75
        targetSP*=0.75

    elif(bulletType=="leo"):
        targetBar=max(0,targetBar-15)

    if(index in exposed):
        targetBar=0

    targetBar=floor(targetBar)
    targetSP=floor(targetSP)

    ##Exposed
    damage-=targetBar
    if(damage+targetBar>=floor(targetBar/2) and barrier>0):
        barrier-=1

    #SP
    damage-=targetSP
    if(damage+targetSP>=floor(targetSP/2) and sp[index]>0):
        sp[index]-=1

    #end sp reduction and degredation
    
    if(bulletType=="hp" or bulletType=="roland"):
        damage=floor(damage*1.5)
        
    if(index==0):#head
        if(not wildcard):#not wildcard
            if(bulletType!="b"):
                damage*=2

            if (damage>=8):
                if(not silent):
                    print(f"### INSTA-KILL, {damage} to head before BTM ###")
                unit.dead=True

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
                unit.dead=True

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
autostun=True
hide=False

#status=set() < future plan for status flags (dynamic set)


############################ ^^^ Globals cause Im a TERRIBLE programmer

def askBulletType():
    return(input("""Ammo Types:
(N)/(Normal) - Standard Ammo
(HP)   - SP treated as 1.5x, 1.5x damage through  <--Fact check thats correct
(B:AP) - SP treated as half, half damage through
(T:AP) - SP treated as half, full damage through (also called K:AP)
(SM:AP)- SP treated as 1/3, full damage through
(HM:AP)- SP treated as 2/3, full damage through
(F:AP) - SP ignored (still degraded), full damage through

(ROLAND) - Aidanos Special Sauce: SP treated as 0.75x, 1.5x damage through
(LEO)    - Matts Special Sauce: BAR treated as 15 points less
    
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
        print(f"[{unit.sp[0]}] [{unit.sp[1]}] [{unit.sp[2]}|{unit.sp[3]}] [{unit.sp[4]}|{unit.sp[5]}]",end="")
    else:
        print(f"[/] [/] [/|/] [/|/]",end="")


def printBarrier(barrier,exposed):
    if(barrier>0):
        print(f"(BAR) Barrier [{barrier}] - ",end="")
        if(len(exposed)>0):
            print(f"(EXP) {exposedString(exposed,False)}")
        else:
            print("(EXP) Exposed")
    else:
        print("(BAR) Barrier")

def exposedString(exposed,big=True):
    output=""
    if(big):
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
    else:
        if(0 in exposed):
            output+="H "
        if(1 in exposed):
            output+="T "
        if(2 in exposed):
            output+="La "
        if(3 in exposed):
            output+="Ra "
        if(4 in exposed):
            output+="Ll "
        if(5 in exposed):
            output+="Rl "
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
        if(i is str):
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
    output=f"(DMG): {unit.damageTaken}\n["
    for _ in range(unit.damageTaken):
        i+=1
        output+="X"
        if(i%10==0):
            output+="]["
        elif(i%5==0):
            output+="|"
        if(i==50):
            unit.dead=True
            break
    for _ in range(50-unit.damageTaken):
        i+=1
        output+="."
        if(i%10==0):
            output+="]["
        elif(i%5==0):
            output+="|"
    print(output[:-1])

def clr():
    if WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def reset(unit):#temp
    global autostun,shotCount,bulletType,barrier,exposed
    exposed=set()
    bulletType="normal"
    autostun=False
    shotCount=0
    barrier=0
    unit.reset()

def saveState(unit):
    clr()
    if(unit.name=="Unnamed"):
        name=input("Save name: ")
    else:
        print(f"### ENTER to default to [{unit.name}] ###")
        name=input(f"Save name: ")
        if(name==""):
            name=unit.name

    data=f"{hide};{autostun};{unit.sp[0]},{unit.sp[1]},{unit.sp[2]},{unit.sp[3]},{unit.sp[4]},{unit.sp[5]};{unit.body};{unit.damageTaken};{unit.wildcard}"

    with open(f"./DT/{name}.txt","w") as f:
        f.write(data)

def loadState(name,unit):
    global autostun,hide
    try:
        with open(f"./DT/{name}.txt","r") as f:
            data=f.read().split(";")

            reset(unit)
            
            hide=data[0]=='True'
            autostun=data[1]=='True'


            input_sp=[int(i) for i in data[2].split(",")]
            sp=[0]*7
            for i in range(len(input_sp)):
                if(i==6):
                    break
                sp[i]=input_sp[i]
            unit.sp=sp

            unit.body=int(data[3])
            unit.btm=bodyToBTM(unit.body)

            unit.damageTaken=int(data[4])

            unit.wildcard=data[5]=='True'

            unit.name=name

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

    unit=Unit([0]*7,6,False)

    if(WINDOWS):
        os.system("title Unnamed DT")

    while(True):### INIT ###
        clr()
        temp=input("If loading from file, enter its name\nIf fresh instance, leave blank\n\n: ")
        if(temp!=""):
            if(loadState(temp,unit)):
                break
        else:
            clr()
            unit=Unit()
            break

    undoSP=unit.sp
    undoDMG=unit.damageTaken
    undoBar=barrier
    undoShot=shotCount
    undoStun=unit.stun
    undoUncon=unit.uncon
    undoDead=unit.dead

    while(True):### MAIN LOOP ###
        clr()
        if(unit.wildcard or autostun or hide):
            if(unit.wildcard):
                print("*WILDCARD*  ",end="")
            if(autostun):
                print("@-Autostun-@  ",end="")
            if(hide):
                print("// HIDDEN //  ",end="")
            print()

        print("‾"*53)

        print(f"{unit.name}",end="")
        if(unit.stun or unit.uncon or unit.dead):
            print("  -  ",end="")
            if(unit.stun):
                print("*STUN*  ",end="")
            if(unit.uncon):
                print("-=-UNCON-=-  ",end="")
            if(unit.dead):
                print("###DEAD###  ",end="")
        print()

        printSP(unit)
        print("   ",end="")

        if(not hide):
            print(f"Body: {unit.body}   BTM: {unit.btm}",end="")
        else:      
            print(f"/// spooky ///",end="")
        print()

        print()

        renderDamage(unit)

        if(unit.stunMod()>0):
            if(unit.unconMod()>0):
                print(f"@ ALL ROLLS -{unit.unconMod()} @   ",end="")
            if(unit.stunMod()>0):
                print(f"** Stun -{unit.stunMod()} **   ",end="")
            print()
        print()
        

        print(f"(AM) Ammo: {bulletType.upper()}")
        printBarrier(barrier,exposed)
        print(f"""{"_"*53}
   (AUTO) (WILD) (HIDE)    |  (CALL)   Called Shot   |
(SAVE) (LOAD) (NEW) (UNDO) |  (RAND) Random Location |
        """)
        temp=input("Input Option: ").lower()
        clr()

        if(temp=="undo"):
            unit.sp=list(undoSP)
            unit.damageTaken=undoDMG
            barrier=undoBar
            shotCount=undoShot
            unit.stun=undoStun
            unit.uncon=undoUncon
            unit.dead=undoDead
            continue
        else:
            undoSP=list(unit.sp)
            undoDMG=unit.damageTaken
            undoBar=barrier
            undoShot=shotCount
            undoStun=unit.stun
            undoUncon=unit.uncon
            undoDead=unit.dead

        if(temp=="stun"):
            unit.stun=not unit.stun
            continue

        if(temp=="uncon"):
            unit.uncon=not unit.uncon
            continue

        if(temp=="dead"):
            unit.dead=not unit.dead
            continue

        if(temp=="hide"):
            hide=not hide
            continue

        if(temp=="exp"):
            while(True):
                clr()
                print("-=- (X) to EXIT -=-\n")
                print("(ALL) - (Head)|(Torso)|(Larm)|(Rarm)|(Lleg)|(Rleg)\n")
                print(f"Currently Exposed: {exposedString(exposed)}")
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
            unit.name=input("Enter new name: ")
            if(WINDOWS):
                os.system("title "+unit.name)
            else: #linux
                os.system("set-title "+unit.name)
            continue

        if(temp=="save"):
            saveState(unit)
            continue

        if(temp=="load"):
            temp=input("Load file name (no '.txt'): ")
            loadState(temp,unit)
            continue

        if(temp=="sp"):
            initSP(unit)
            continue

        if(temp=="dmg"):
            unit.damageTaken=int(input(f"Set damage taken (old: {unit.damageTaken}): "))
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
            unit.wildcard=not unit.wildcard
            continue

        if(temp=="head"):
            unit.sp[0] = input("Set head SP: ")
            continue
        if(temp=="torso"):
            unit.sp[1] = input("Set torso SP: ")
            continue
        if(temp=="larm"):
            unit.sp[2] = input("Set left arm SP: ")
            continue
        if(temp=="rarm"):
            unit.sp[3] = input("Set right arm SP: ")
            continue
        if(temp=="lleg"):
            unit.sp[4] = input("Set left leg SP: ")
            continue
        if(temp=="rleg"):
            unit.sp[5] = input("Set right leg SP: ")
            continue

        if(temp=="c" or temp=="call"):
            count=0
            clr()
            print(f"Current ammo type: {bulletType.upper()}")
            print("-=- Press (x) to EXIT -=-")
            while(True):
                count+=1
                location=input("Location (Head,Torso,Larm,Rarm,Lleg,Rleg,Other): ").lower()
                if(location=="x"):
                    break

                if(location=="other"):
                    temp=input("Location SP: ")
                    unit.sp[6]=0
                    if(temp.isnumeric() and not temp==""):
                        unit.sp[6]=int(temp)

                damage=input("Damage: ")
                if(damage=="x"):
                    break
                if(damage==""):
                    print()
                    continue

                if(location=="other"):
                    locSP=unit.sp[6]
                    output=dealDamage(unit,processDamage(damage),6)
                    unit.damageTaken+=output
                    if(input(f"{count}: Dealt {output} damage to {locSP} SP, new SP is {unit.sp[6]}, ENTER to Continue\n").lower()=="x"):
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

                output=dealDamage(unit,processDamage(damage),i)
                unit.damageTaken+=output
                print(f"{count}: Dealt {output} damage to {LOCATIONS[i]}\n")

            continue

        if(temp=="r" or temp=="rand"):
            iterations=0
            count=0
            print(f"Current ammo type: {bulletType.upper()}")
            print("-=- Press (x) to EXIT -=-\n")
            while(True):
                count+=1
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

                output=dealDamage(unit,processDamage(damage),i)
                unit.damageTaken+=output
                print(f"{count}: Dealt {output} damage to {LOCATIONS[i]}\n")

if __name__=='__main__':
    main()