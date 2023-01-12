from math import ceil,floor
from random import choice,randint
import os

shotCount=0
damageTaken=0
wildcard=False
btm=0
sp=[0]*6
bulletType="normal" #normal,bullet,knife,
barrier=0

locations=["Head","Torso","Larm","Rarm","Lleg","Rleg"]
randLocation=[0,1,1,1,1,1,2,3,4,5]
temp=""

def setBulletType():
    global bulletType
    bulletType=input("""Ammo Types
Default: (Normal)/(N)
AP: (Bullet)/(B) (Knife)/(K) (Full)/(F)
    
Ammo Type:""").lower()

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
    print(f"(SP) - [{sp[0]}|{sp[1]}|{sp[2]}|{sp[3]}|{sp[4]}|{sp[5]}]")

def initSP():
    global sp
    print("SP in order (Head)|(Torso)|(Larm)|(Rarm)|(Lleg)|(Rleg)")
    sp=input("format \"H,T,L,R,L,R\" or \"ALL\": ").split(",")
    if(sp==[""]):
        sp=[0]*6
        return
    if(len(sp)==1):
        sp=[int(sp[0])]*6
    else:
        for i in range(len(sp)):
            sp[i]=int(sp[i])

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

def dealDamage(damage,index):
    global barrier,sp,shotCount,bulletType
    if(bulletType=="normal" or bulletType=="n"):

        damage-=barrier
        if(damage+barrier>=barrier/2 and barrier>0):
            barrier-=1
        damage-=sp[index]
        if(damage+sp[index]>=sp[index]/2 and sp[index]>0):
            sp[index]-=1
        
        if(index==0):#head
            if(not wildcard):#not wildcard
                damage*=2
                if (damage>=8):
                    print(f"INSTA-KILL!!, with {damage} damage after double before BTM")
                if(damage>0):
                    damage=max(1,damage-btm)

            else:#wildcard
                if(damage>0):
                    damage=max(1,damage-btm)
                if(damage>=8):
                    print(f"INSTA-KILL!!, with {damage} damage after BTM before double")
                damage*=2

        elif(damage>0):#not head AND damage exists
            damage=max(1,damage-btm)

    elif(bulletType=="bullet" or bulletType=="b"):

        damage-=floor(barrier/2)
        if(damage+floor(barrier/2)>=floor(barrier/4) and barrier>0):
            barrier-=1
        damage-=floor(sp[index]/2)
        if(damage+floor(sp[index]/2)>=floor(sp[index]/4) and sp[index]>0):
            sp[index]-=1

        if(index==0):#head
            if(not wildcard):#not wildcard
                if (damage>=8):
                    print(f"INSTA-KILL!!, with {damage} damage after double before BTM")
                damage-=btm

            else:#wildcard
                damage=floor(damage/2)
                damage-=btm
                if(damage>=8):
                    print(f"INSTA-KILL!!, with {damage} damage after BTM before double")
                damage*=2

        else:#not head
            damage=floor(damage/2)
            damage-=btm

        #end bullet type == ap

    else:#Undefined bullet type
        bulletType="normal"
        return dealDamage(damage,index)
        
    shotCount+=1

    if(damage>0):
        return damage

    print("No damage")
    return 0

os.system('cls')
if(input("Wildcard(y/n): ").__contains__("y")):
    print("Wildcard")
    wildcard=True
else:
    print("Non wildcard")
print()
setBody()
print()
initSP()

####################### MAIN LOOP

while(True):
    os.system('cls')
    if(wildcard):
        print("*WILDCARD*")
    print(f"(SHT) Shot counter: {shotCount} (DMG) Damage Taken: {damageTaken}\n")
    printSP()
    print(f"""(BTM) Body Type Modifier: {btm}

(AM)  Ammo Type: {bulletType.upper()}
(BAR) Barrier SP: {barrier}

(C) Called Shot
(D) Damage to random location
(N) New Enemy
    """)
    temp=input("Input Option: ").lower()
    os.system('cls')

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
        if(input("Wildcard(y/n): ").__contains__("y")):
            wildcard=True
        setBody()
        initSP()

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
            os.system('cls')
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

            damage=processDamage(damage)
            output=dealDamage(damage,i)
            damageTaken+=output
            if(input(f"Dealt {output} damage to {locations[i]}, ENTER to Continue\n").lower()=="x"):
                break

    if(temp=="d"):
        iterations=0
        if(bulletType=="normal"):
            setBulletType()
        print("-=- Press (x) to EXIT -=-\n")
        while(True):
            i=choice(randLocation)
            if(iterations<=0):
                print(f"Damage to {locations[i]}")
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
            
            damage=processDamage(damage)
            output=dealDamage(damage,i)
            damageTaken+=output
            print(f"Dealt {output} damage to {locations[i]}\n")