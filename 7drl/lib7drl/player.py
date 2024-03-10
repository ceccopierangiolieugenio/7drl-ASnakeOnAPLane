# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = ['Player','Body']

from dataclasses import dataclass
import sys, os, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .assets   import *
from .glbls    import *
from .objinfo  import *
from .messages import *

ArmorValues = {
    'af1':25,'ah1':25,'ab1':25,'al1':20,
    'af2':30,'ah2':30,'ab2':30,'al2':30,
    'af3':35,'ah3':35,'ab3':35,'al3':50,
    'af4':40,'ah5':40,'ab5':40,
    'af4':45,'ah4':45,'ab4':45}

@dataclass()
class Body():
    HEAD:int = 0x01
    BODY:int = 0x02
    LEGS:int = 0x03
    FEET:int = 0x04

    head: str = 'ah1'
    body: str = 'ab1'
    legs: str = 'al1'
    feet: str = 'af1'

    maxArmor = 45+45+45+50

    armorPoint = {'h': 15,'b': 15,'l': 10,'f': 15}

    def wear(self, obj):
        if obj in ['af1','af2','af3','af4','af4']:
            if self.armorPoint['f'] > ArmorValues[obj]:
                return False
            self.feet=obj
            self.armorPoint['f']=ArmorValues[obj]
        if obj in ['ah1','ah2','ah3','ah4','ah4']:
            if self.armorPoint['f'] > ArmorValues[obj]:
                return False
            self.head=obj
            self.armorPoint['h']=ArmorValues[obj]
        if obj in ['ab1','ab2','ab3','ab4','ab4']:
            if self.armorPoint['b'] > ArmorValues[obj]:
                return False
            self.body=obj
            self.armorPoint['b']=ArmorValues[obj]
        if obj in ['al1','al2','al3']:
            if self.armorPoint['l'] > ArmorValues[obj]:
                return False
            self.legs=obj
            self.armorPoint['l']=ArmorValues[obj]
        return True

    def getArmorValue(self):
        armor = 0
        for i in self.armorPoint:
            armor += self.armorPoint[i]
        return armor

    def hit(self, value):
        for ak in (ap:=self.armorPoint):
            if value >= ap[ak]:
                value -= ap[ak]
                ap[ak] = 0
                if ak == 'h': self.head = ''
                if ak == 'b': self.body = ''
                if ak == 'l': self.legs = ''
                if ak == 'f': self.feet = ''
            else:
                ap[ak] -= value
                value = 0
        return value

# ['wm1','wm2','wm3','wm4']
# ['wr1','wr2','wr3','wr4']
# ['ws1','ws2','ws3','ws4']
# ['wt1','wt2','wt3','wt4']

MeleeParams = {'wm0':10,'wm1':15,'wm2':20,'wm3':25,'wm4':30}
ShellsParam = {'wr1':5 ,'wr2':5 ,'wr3': 3,'wr4': 3,
               'ws1':15,'ws2':15,'ws3': 5,'ws4': 5,
               'wt1':3 ,'wt2':2 ,'wt3': 1,'wt4': 1}
AttackParam = {'wr1':5 ,'wr2':10,'wr3':20,'wr4':25,
               'wt1':20,'wt2':30,'wt3':40,'wt4':30}
MaxShells =   {'ws1':100,'ws2':100,'ws3':30,'ws4': 20,
               'wt1': 20,'wt2': 20,'wt3':20,'wt4': 10}
Gold = {'g1': 10,'g2': 13,'g3': 27,'g4':  44,
        'g5':142,'g6':364,'g7':735,'g8':1297}
class Player():
    def __init__(self) -> None:
        self.updated = ttk.pyTTkSignal()
        self.moneyUpdated = ttk.pyTTkSignal(int)

        self.shells = {
            'ws1' : 20,
            'ws2' : 0,
            'ws3' : 0,
            'ws4' : 0,}
        self.throwables = {
            'wt1' : 1,
            'wt2' : 0,
            'wt3' : 1,
            'wt4' : 2,}

        self._weaponParams = {
            'wr1': (self.shells    , 'ws1'),
            'wr2': (self.shells    , 'ws2'),
            'wr3': (self.shells    , 'ws3'),
            'wr4': (self.shells    , 'ws4'),
            'wt1': (self.throwables, 'wt1'),
            'wt2': (self.throwables, 'wt2'),
            'wt3': (self.throwables, 'wt3'),
            'wt4': (self.throwables, 'wt4')}
        self.resetStats()

    def resetKeys(self):
        self.keys = []
        self.updated.emit()

    def resetStats(self):
        self.deathSentence = ['']
        self.money= 1
        self.keys = []
        self.body = Body()
        self._health:    int  = 200
        self.maxHealth:  int = 200
        self.meleeHeld:  str  = 'wm0'
        self.weaponHeld: str  = 'wr1'
        self.weapons:    list = ['wr1','wr3','wr4']
        self.maxArmor = self.body.maxArmor

    def shellGlyph(self):
        return Tiles[self._weaponParams[self.weaponHeld][1]]

    @property
    def atk(self):
        # Calc the value of the melee attack
        return MeleeParams[self.meleeHeld]


    @property
    def wpn(self):
        return AttackParam[self.weaponHeld]

    def shot(self):
        ret = False
        sh = self._weaponParams.get(self.weaponHeld,None)
        if sh:
            shn, sht = sh
            if shn[sht]:
                shn[sht] = max(0,shn[sht]-1)
                ret = True
                self.updated.emit()
        return ret

    @property
    def health(self):
        # Calc the value of the melee attack
        return self._health

    @health.setter
    def health(self, value):
        # Calc the value of the weapon attack
        if glbls.godMode:
            self._health = self.maxHealth
        else:
            self._health = max(0,min(value,self.maxHealth))
        self.updated.emit()

    @property
    def armor(self):
        # Calc the value of the melee attack
        return self.body.getArmorValue()

    def hit(self,value, deathSentence):
        value = self.body.hit(value)
        self.health -= value
        self.deathSentence = deathSentence
        self.updated.emit()


    def nextWeapon(self,dir=1):
        aw = sorted(self.weapons)
        wh = self.weaponHeld
        aw += [t for t in self.throwables if self.throwables[t]]
        if wh in aw:
            i  = aw.index(wh)
            ai = (i+dir)%len(aw)
            self.weaponHeld = aw[ai]
        else:
           self.weaponHeld  = aw[0]
        self.updated.emit()

    def prevWeapon(self):
        self.nextWeapon(-1)

    def grab(self, obj):
        grabbed = True
        if obj in ['af1','ah1','ab1','al1',
                   'af2','ah2','ab2','al2',
                   'af3','ah3','ab3','al3',
                   'af4','ah4','ab4',
                   'af5','ah5','ab5']:
            grabbed = self.body.wear(obj)
            if grabbed:
                Message.add(ttk.TTkString(
                    random.choice([
                        "You are proudly suiting up",
                        "You are outfitting",
                        "You feel amazing dressing",
                        "You are as beautiful as ever with a new",
                        "It's time grab a damn new",
                        "Everyone is enchanted by your new",
                    ])))
            else:
                Message.add(ttk.TTkString("You are wearing something better than"))
        elif obj in ['wm1','wm2','wm3','wm4']:
            self.meleeHeld = obj
            Message.add(ttk.TTkString("Welding a shiny new"))
        elif obj in ['ws1','ws2','ws3','ws4']:
                shells = ShellsParam[obj]
                maxSh = MaxShells[obj]
                if self.shells[obj] == maxSh:
                    grabbed = False
                    Message.add(ttk.TTkString("You are already full of"))
                else:
                    self.shells[obj] = min(maxSh,self.shells[obj]+shells)
                    Message.add(ttk.TTkString("Grabbing"))
        elif obj in ['wt1','wt2','wt3','wt4']:
                shells = ShellsParam[obj]
                maxSh = MaxShells[obj]
                self.throwables[obj] = min(maxSh,self.throwables[obj]+shells)
                Message.add(ttk.TTkString("Picking up"))
        elif obj in ['wr1','wr2','wr3','wr4']:
            if obj not in self.weapons:
                self.weapons.append(obj)
                shells = ShellsParam[obj]
                _, nameSh = self._weaponParams[obj]
                maxSh = MaxShells[nameSh]
                self.shells[nameSh] = min(maxSh,self.shells[nameSh]+shells)
                Message.add(ttk.TTkString("Feel the dark power of"))
        elif obj in ['g1','g2','g3','g4','g5','g6','g7','g8']:
            self.money += Gold[obj]
            self.moneyUpdated.emit(self.money)
        elif obj in ['KR','KG','KB','KY']:
            self.keys.append(obj)
            Message.add(ttk.TTkString("Grabbed"))
        Message.add(ObjInfo[obj][0])
        self.updated.emit()
        return grabbed



