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

__all__ = ['Foe','FOELIST']

import sys, os, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk


FOELIST = {
    'z'       : {'health':  5, 'atk':  5, 'wpn': 0, 'speed': 7, 'reloadSpeed':  0, 'distance':2, 'drop':['g1''g2','ws1','ws2']},
    'Vampire' : {'health': 10, 'atk': 10, 'wpn': 3, 'speed': 7, 'reloadSpeed':  5, 'distance':6, 'drop':['g1''g2','ws1','ws2']},
    'Ghost'   : {'health': 15, 'atk': 10, 'wpn': 4, 'speed': 4, 'reloadSpeed':  5, 'distance':2, 'drop':['g2''g3','ws1','ws2']},
    'Pumpkin' : {'health': 20, 'atk': 15, 'wpn': 5, 'speed': 6, 'reloadSpeed':  5, 'distance':2, 'drop':['g2''g3','ws1','ws2']},
    'Imp'     : {'health': 25, 'atk': 15, 'wpn': 5, 'speed': 7, 'reloadSpeed':  5, 'distance':2, 'drop':['g4''g5','ws2','ws3']},
    'Robot'   : {'health': 40, 'atk': 20, 'wpn': 5, 'speed': 2, 'reloadSpeed':  5, 'distance':2, 'drop':['g4''g5','ws2','ws3']},
    'Crap'    : {'health': 40, 'atk': 10, 'wpn': 5, 'speed': 4, 'reloadSpeed':  5, 'distance':6, 'drop':['g6''g7','ws2','ws3','wt2']},
    'SI'      : {'health': 60, 'atk': 15, 'wpn': 6, 'speed': 7, 'reloadSpeed':  5, 'distance':2, 'drop':['g6''g7','ws2','ws3','wt2']},
    'Alien'   : {'health': 70, 'atk': 15, 'wpn': 6, 'speed': 8, 'reloadSpeed':  5, 'distance':2, 'drop':['g7''g8','ws3','ws4','wt3']},
    'Dragon1' : {'health': 80, 'atk': 30, 'wpn':10, 'speed': 5, 'reloadSpeed':  5, 'distance':6, 'drop':['g7''g8','ws3','ws4','wt3']},
    'TRex'    : {'health': 90, 'atk': 30, 'wpn': 0, 'speed': 8, 'reloadSpeed':  5, 'distance':2, 'drop':['g7''g8','ws3','ws4','wt3']},
    'Nose'    : {'health':150, 'atk': 35, 'wpn':15, 'speed': 8, 'reloadSpeed':  5, 'distance':2, 'drop':['KY']},
}

class Foe():
    def __init__(self, *, pos=(0,0), name,
                 distance, atk, wpn, speed, reloadSpeed, health, drop) -> None:
        self.pos=pos
        self.atk=atk
        self.wpn=wpn
        self.drop = drop
        self.name = name
        self.speed = speed
        self.active = False
        self.health = health
        self.distance = distance
        self.reloadSpeed = reloadSpeed
        self.time = random.randint(0,10)

    def getActions(self) -> list[bool,bool]: # return move or shot
        self.time += 1
        return (self.time*self.speed)%10<=self.speed, (self.time*self.reloadSpeed)%10<self.reloadSpeed,
