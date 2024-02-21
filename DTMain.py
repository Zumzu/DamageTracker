from math import ceil,floor
from random import choice,randint
import os
from platform import system

def dealDamage(damage,index,silent=False):
    global shotCount,barrier,sp,damageTaken,stun,uncon,dead,bulletType,exposed,autostun

    targetBar=int(barrier)
    targetSP=int(sp[index])

    if(bulletType=="full" or bulletType=="f"):
        targetBar=0
        targetSP=0

    elif(bulletType=="pref" or bulletType=="p" or bulletType=="t" or bulletType=="hm"):
        targetSP*=0.5

    elif(bulletType=="quarter" or bulletType=="qu" or bulletType=="sm"):
        targetSP*=0.25
        
    elif(bulletType=="ap" or bulletType=="b"):
        targetBar*=0.5
        targetSP*=0.5

    elif(bulletType=="holo" or bulletType=="hp" or bulletType=="h"):
        targetBar*=1.5
        targetSP*=1.5

    elif(bulletType=="cyber" or bulletType=="cc"):
        if(not sdp[index]==-1):
            damage*=2
    
    elif(bulletType=="fmj"):
        targetBar=max(targetBar-15,0)

    targetBar=floor(targetBar)
    targetSP=floor(targetSP)

    ##Exposed
    if(index in exposed or targetBar<0):
        targetBar=0

    damage-=targetBar
    if(damage+targetBar>=barrier/2 and targetBar>0):
        barrier-=1

    #SP
    damage-=targetSP
    if(damage+targetSP>=sp[index]/2 and sp[index]>0):
        sp[index]-=1

    if(bulletType=="explo" or bulletType=="e"):
        exploDamage=randint(1,3)
        if(not silent):
            print(f"+{exploDamage} sp damage from explosive ammo")  
        sp[index]-=exploDamage

    #end sp reduction and degredation
        
    if(bulletType=="ap" or bulletType=="b"):
        damage*=0.5
    elif(bulletType=="holo" or bulletType=="hp" or bulletType=="h"):
        damage*=1.5
    damage=floor(damage)

    if(damage<=0): # return early if no damage
        return 0
    
    if(index==0): # double if head
        damage*=2

    if(sdp[index]==-1):
        damage=max(1,floor(damage)-btm) # apply btm

        if(damage>=8 and index==0): # check if headshot to death
            dead=True
            if(not silent):
                print(f"### INSTA-KILL, {damage} to head before BTM ###")
        elif(damage>=15 and index==1):  # check crit injury for torso
            if(not silent):
                print(f"# CRITICAL INJURY TO TORSO #")  
        elif(damage>=8 and index>1):   # check crit injury for other limbs
            if(not silent):
                print(f"# CRITICAL INJURY TO {LOCATIONS[index].upper()} #")      

    shotCount+=1

    if(sdp[index]==-1):
        damageTaken+=damage
        if(autostun):
            rollStun()
    else:
        if(bulletType=="cyber" or bulletType=="cc"):
            sdp[index]-=damage*2
            if(autostun):
                rollStun()
        else:
            sdp[index]-=damage

        if(sdp[index]<=0):
            sdp[index]=0
            if(not silent):
                if(index==1):
                    print(f"### ROBOT DEAD ###")  
                    dead=True
                else:
                    print(f"# CYBERLIMB BROKEN #")

    if(bulletType=="i" or bulletType=="incin"):
        incinDamage=randint(1,6)
        if(not silent):
            print(f"+{incinDamage} damage from incindiary ammo")  
        
        if(sdp[index]==-1):
            incinDamage=max(1,floor(incinDamage)-btm)

        damage+=incinDamage

        if(sdp[index]==-1):
            damageTaken+=incinDamage
            if(autostun):
                rollStun()
        else:
            sdp[index]-=incinDamage
            if(sdp[index]<0):
                sdp[index]=0
                if(not silent):
                    if(index==1):
                        print(f"### ROBOT DEAD ###")  
                        dead=True
                    else:
                        print(f"# CYBERLIMB BROKEN #")  
        
    return damage


############################ ^^^ BIG BUT LESS AWFUL DAMAGE FUNCTION ^^^  ##################################

#Macros
WINDOWS=system()=="Windows"
LOCATIONS=["Head","Torso","Larm","Rarm","Lleg","Rleg","Other"]
RANDLOCATION=[0,1,1,1,1,1,2,3,4,5]

#Program Logic (will be placed in main)
bulletType="Norm"
shotCount=0
barrier=0
exposed=set()
autostun=True
hide=False

# Unit Stats
name="Unnamed"
wildcard=False
sp=[0]*7
sdp=[-1]*6
btm=0
body=6
damageTaken=0

# Unit Flags
stun=False
uncon=False
dead=False

############################ ^^^ Globals cause Im a TERRIBLE programmer

def stunMod(damageTaken):
    return floor((damageTaken-1)/5)

def unconMod(damageTaken):#does not need to exist, just a macro for convinience
    return allNegative(damageTaken)

def allNegative(damageTaken):
    return max(floor((damageTaken-1)/5)-3,0)

def rollStun(silent=False):
    global stun,uncon,damageTaken,body

    if(not stun):
        if(rollD10()>body-stunMod(damageTaken)):
            if(not silent):
                print("*** STUN ***")
            stun=True

    if(stun and damageTaken>15 and not uncon):
        if(rollD10()>body-unconMod(damageTaken)):
            if(not silent):
                print("-=- UNCON -=-")
            uncon=True

def bodyToBTM(body):
    if(body>14):
        return 7
    elif(body>10):
        return 5
    elif(body<6):
        return ceil(body/2-1)
    else:
        return floor(body/2-1)

def askBulletType():
    return(input("""Ammo Types:
(NORM) - Standard damage
(PREF) - SP halved, full damage
(QU)   - SP quartered, full damage

(AP)   - SP treated as half, half damage through         
(HOLO) - SP treated as 1.5x, 1.5x damage through
(INCIN)- Additional 1D6 damage if damage does through
(EXPLO)- Additional 1D3 sp damage
(CYBER)- On SDP: 2x damage and force a stun check
(FMJ)  - Pierces the first 15 SP of barriers

(FULL) - SP ignored (still degraded), full damage through

Ammo Type: """).lower())

def initBody():
    global body,btm
    clr()
    temp=input("Set body: ")
    if(temp=="" or not temp.isnumeric()):
        temp=6
        print("defaulted to body: 6, btm: 2")
    body=int(temp)
    btm=bodyToBTM(body)

def printSP():
    global sp,sdp,hide
    if(not hide):
        print(f"[{sp[0]}] [{sp[1]}] [{sp[2]}|{sp[3]}] [{sp[4]}|{sp[5]}]",end="")
    else:
        print(f"[/] [/] [/|/] [/|/]",end="")
    print("   ",end="")
    if(sdp[1]==-1):
        if(not hide):
            print(f"Body: {body}",end="")
        else:      
            print(f"/// spooky ///",end="")
    print()

    for i in range(6):
        if(sdp[i]!=-1):
            print(f"{LOCATIONS[i]}: {sdp[i]}sdp  ",end="")


def printBarrier(barrier,exposed):
    if(barrier>0):
        print(f"Barrier [{barrier}] - ",end="")
        if(len(exposed)>0):
            print(f"(EXP) {exposedString(exposed,False)}")
        else:
            print("(EXP) Exposed")

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

    for i in sp:
        if(i is str):
            if(not i.isnumeric()):
                print("@@SP INIT FAILURE@@")
                sp=[0]*7
                return

    sp=[int(i) for i in sp]

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

def renderDamage():
    global dead,damageTaken
    i=0
    output=f"(DMG): {damageTaken}\n["
    for _ in range(damageTaken):
        i+=1
        output+="#"
        if(i%10==0):
            output+="]["
        elif(i%5==0):
            output+="|"
        if(i==50):
            dead=True
            break
    for _ in range(50-damageTaken):
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

def reset():#temp
    global name,hide,autostun,shotCount,bulletType,barrier,exposed,sp,sdp,body,btm,damageTaken,stun,uncon,dead,wildcard
    exposed=set()
    bulletType="Norm"
    autostun=True
    shotCount=0
    barrier=0
    sp=[0]*7
    sdp=[-1]*6
    body=6
    btm=2
    damageTaken=0
    stun=False
    uncon=False
    dead=False
    wildcard=False
    name="Unnamed"
    if(WINDOWS):
        os.system("title "+name)
    else: #linux
        os.system("set-title "+name)

def saveState():
    global name,hide,autostun,sp,body,damageTaken,wildcard
    clr()
    if(name=="Unnamed"):
        name=input("Save name: ")
    else:
        print(f"### ENTER to default to [{name}] ###")
        temp=input(f"Save name: ")
        if(temp==""):
            name=temp

    data=f"{hide};{autostun};{sp[0]},{sp[1]},{sp[2]},{sp[3]},{sp[4]},{sp[5]};{body};{damageTaken};{wildcard}"

    with open(f"./DT/{name}.txt","w") as f:
        f.write(data)

def loadState(fileName):
    global name,autostun,hide,sp,body,btm,damageTaken,wildcard
    try:
        with open(f"./DT/{fileName}.txt","r") as f:
            data=f.read().split(";")

            reset()
            
            hide=data[0]=='True'
            autostun=data[1]=='True'


            input_sp=[int(i) for i in data[2].split(",")]
            sp=[0]*7
            for i in range(len(input_sp)):
                if(i==6):
                    break
                sp[i]=input_sp[i]

            body=int(data[3])
            btm=bodyToBTM(body)

            damageTaken=int(data[4])

            wildcard=data[5]=='True'

            name=fileName


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
    global name,hide,autostun,shotCount,bulletType,barrier,exposed,sp,sdp,body,btm,damageTaken,stun,uncon,dead,wildcard

    if(WINDOWS):
        os.system("title Unnamed DT")

    while(True):### INIT ###
        clr()
        temp=input("If loading from file, enter its name\nIf fresh instance, leave blank\n\n: ")
        if(temp!=""):
            if(loadState(temp)):
                break
        else:
            initBody()
            initSP()
            break

    undoSP=sp
    undoSDP=sdp
    undoDMG=damageTaken
    undoBar=barrier
    undoShot=shotCount
    undoStun=stun
    undoUncon=uncon
    undoDead=dead

    while(True):### MAIN LOOP ###
        clr()

        if(damageTaken>=50):
            dead=True

        if(wildcard or autostun or hide):
            if(wildcard):
                print("*WILDCARD*  ",end="")
            else:
                print("-Standard-  ",end="")

            if(autostun):
                print("@-Autostun-@  ",end="")
            if(hide):
                print("// HIDDEN //  ",end="")
            print()
            print("‾"*53)

        print(f"{name}",end="")
        if(stun or uncon or dead):
            print("  -  ",end="")
            if(stun):
                print("*STUN*  ",end="")
            if(uncon):
                print("-=-UNCON-=-  ",end="")
            if(dead):
                print("###DEAD###  ",end="")
        print()

        printSP()
        print()
        if(sdp[1]!=-1):
            print()
            
        printBarrier(barrier,exposed)

        if(sdp[1]==-1):
            print()
            renderDamage()

        if(stunMod(damageTaken)>0):
            if(unconMod(damageTaken)>0):
                print(f"@ ALL ROLLS -{unconMod(damageTaken)} @   ",end="")
            if(stunMod(damageTaken)>0):
                print(f"** Stun -{stunMod(damageTaken)} **   ",end="")
        print()

        print(f"""{"_"*53}
(NAME) (BODY) (CYBER) (SP) | (CALL) Called Shot
(SAVE) (LOAD) (NEW) (UNDO) | (RAND) Random Location
                           | (AMMO) Ammo: {bulletType.upper()}    
""",end="")
        temp=input("C$> ").lower()
        clr()

        if(temp=="undo"):
            sp=list(undoSP)
            sdp=list(undoSDP)
            damageTaken=undoDMG
            barrier=undoBar
            shotCount=undoShot
            stun=undoStun
            uncon=undoUncon
            dead=undoDead
            continue
        else:
            undoSP=list(sp)
            undoSDP=list(sdp)
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
        
        if(temp=="sdp" or temp=="cyber"):
            userin=input("SDP format \"H,T,L,R,L,R\", \"Larm,Rarm,Lleg,Rleg\" or empty to clear\nSDP: ").split(",")
            if(userin[0]==""):
                sdp=[-1]*6
            elif(len(userin)==4):
                sdp[2]=(-1 if userin[0]=='0' else int(userin[0]))
                sdp[3]=(-1 if userin[1]=='0' else int(userin[1]))
                sdp[4]=(-1 if userin[2]=='0' else int(userin[2]))
                sdp[5]=(-1 if userin[3]=='0' else int(userin[3]))
            elif(len(userin)==1):
                sdp=[int(userin[0])]*6
            else:
                for i in range(len(userin)):
                    if(i==6):
                        break
                    if(userin[i]==""):
                        sdp[i]=-1
                    else:
                        sdp[i]=(-1 if userin[i]=='0' else int(userin[i]))

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
            name=input("Enter new name: ")
            if(WINDOWS):
                os.system("title "+name)
            else: #linux
                os.system("set-title "+name)
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
            initBody()
            continue

        if(temp=="am" or temp=="ammo"):
            bulletType=askBulletType()
            continue

        if(temp=="sht"):
            shotCount=int(input(f"Set shot count (old: {shotCount}): "))
            continue

        if(temp=="bar" or temp=="barrier"):
            barrier=int(input(f"Set barrier (old: {barrier}): "))
            continue

        if(temp=="new"):
            reset()
            initBody()
            initSP()
            continue

        if(temp=="auto" or temp=="autostun"):
            autostun=not autostun
            continue

        if(temp=="wild" or temp=="wildcard"):
            wildcard=not wildcard
            continue

        if(temp=="head"):
            sp[0] = int(input("Set head SP: "))
            continue
        if(temp=="torso"):
            sp[1] = int(input("Set torso SP: "))
            continue
        if(temp=="larm"):
            sp[2] = int(input("Set left arm SP: "))
            continue
        if(temp=="rarm"):
            sp[3] = int(input("Set right arm SP: "))
            continue
        if(temp=="lleg"):
            sp[4] = int(input("Set left leg SP: "))
            continue
        if(temp=="rleg"):
            sp[5] = int(input("Set right leg SP: "))
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
                    if(input(f"{count}: Dealt {output} damage to {locSP} SP, new SP is {sp[6]}, ENTER to Continue\n").lower()=="x"):
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

                output=dealDamage(processDamage(damage),i)
                print(f"{count}: Dealt {output} damage to {LOCATIONS[i]}\n")

if __name__=='__main__':
    main()