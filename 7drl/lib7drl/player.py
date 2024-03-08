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

from .assets import *
from .glbls  import *

@dataclass()
class Body():
    HEAD:int = 0x01
    BODY:int = 0x02
    LEGS:int = 0x03
    FEET:int = 0x04

    head: str = ''
    body: str = ''
    legs: str = ''
    feet: str = ''

    def wear(self, what, where):
        if where == self.HEAD: self.head = what
        if where == self.BODY: self.body = what
        if where == self.LEGS: self.legs = what
        if where == self.FEET: self.feet = what

    def getArmorValue(self):
        return 100

class Player():
    def __init__(self) -> None:
        self.updated = ttk.pyTTkSignal()
        self._health:    int  = 100
        self.maxHealth:  int = 100
        self.weaponHeld: str  = 'wr1'
        self.weapons:    list = ['wr1','wr3','wr4']
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
            'wr1': (self.shells    , 'ws1', 10),
            'wr2': (self.shells    , 'ws2', 20),
            'wr3': (self.shells    , 'ws3', 40),
            'wr4': (self.shells    , 'ws4', 40),
            'wt1': (self.throwables, 'wt1', 25),
            'wt2': (self.throwables, 'wt2', 30),
            'wt3': (self.throwables, 'wt3', 40),
            'wt4': (self.throwables, 'wt4', 20)}

        self.body = Body()
        self.armor:int = self.body.getArmorValue()

    def shellGlyph(self):
        return Tiles[self._weaponParams[self.weaponHeld][1]]

    @property
    def atk(self):
        # Calc the value of the melee attack
        return 10

    @property
    def wpn(self):
        # Calc the value of the weapon attack
        sh = self._weaponParams.get(self.weaponHeld,None)
        if not sh: return
        shn, sht, wpn = sh
        # if not shn[sht]: return 0
        return wpn

    def shot(self):
        sh = self._weaponParams.get(self.weaponHeld,None)
        if sh:
            shn, sht, wpn = sh
            shn[sht] = max(0,shn[sht]-1)
        self.updated.emit()
        return sh

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



