from DamageTracker import clr,saveState,Unit
from random import randint

class Mook:
    name=""
    sp=[0]*7

    #stat
    ref=6   #stats defined by 3-6, 4-7, 5-8, 6-9, 7-10
    body=6  
    move=6  

    #skill
    gun=9   #skill defined by 8-9, 10-11, 12-13, 14-15, 16-17
    melee=9 #skill defined by 6-10, 8-12, 10-14, 12-16, 14-18
    dodge=8 #skill below defined by 6-9, 7-11, 8-13, 9-15, 10-17
    ath=8   
    will=8
    awr=8
    end=8

    def __init__(self,skillTier):
        self.ref=min(3+skillTier+randint(0,3),10)
        self.body=min(3+skillTier+randint(0,3),10)
        self.move=min(3+skillTier+randint(0,3),10)

        self.gun=8+skillTier*2+randint(0,1)
        self.melee=6+skillTier*2+randint(0,4)

        self.dodge=6+skillTier+randint(0,3+skillTier)
        self.ath=6+skillTier+randint(0,3+skillTier)
        self.will=6+skillTier+randint(0,3+skillTier)
        self.awr=6+skillTier+randint(0,3+skillTier)
        self.end=6+skillTier+randint(0,3+skillTier)

    def render(self):
        output=f'''
        Relfex [{self.ref}] | Body [{self.body}] | Move [{self.move}]
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        ath: {self.ath}  end: {self.end}  dodge: {self.dodge}
        awr: {self.awr}  will: {self.will}
        '''
        print(output)

def mookToUnit(mook)->Unit:
    return Unit(mook.sp,mook.body,False)

def generateWeapon(tier,legal,illegal,melee)->str:
    with open(f"./MM/MMweapons.txt","r") as f:
        data=f.read().split(":)")

def main():
    userIn="f"
    statTier=-1
    weaponTier=-1
    armourTier=-1

    clr()
    print("Welcome to MookMaker!")
    print("-=-=-=-=-=-=-=-=-=-=-")
    print("For frame of reference: ")
    print("0: Weak | 1: Standard | 2: Strong | 3: Deadly | 4: Player level (Dont Use!)")
    print()
    while(not userIn.isnumeric()):
        userIn=input("Select a mook tier (0-4): ")
    statTier=int(userIn)

    userIn="f"
    while(not userIn.isnumeric()):
        userIn=input("Select a equipment grade (0-4): ")
    weaponTier=int(userIn)

    armourTier=input("Select an equipment style (Police,Gang,etc): ")

    currentMook=Mook(statTier)

    while(True):
        clr()
        print("CURRENT MOOK:")
        currentMook.render()
        print()
        print(f" (STAT)  - Current stat tier: {statTier}")
        print(f"(WEAPON) - Current weapon tier: {weaponTier}")
        print(f"(ARMOUR) - Current armour tier: {armourTier}")
        userIn=input("Input: ")

        if(userIn=="save"):
            saveState(mookToUnit(currentMook))


if __name__=="__main__" :
    main()