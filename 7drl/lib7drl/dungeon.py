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

__all__ = ['Dungeon']

import sys, os, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .dungeonprime import *
from .layer  import *

# Glyphs:
# 🍝🍜🔑🗝️🪪💳📓🎁📔📒📕📗📘📙
# 📀💿💾💽🥇🥈🥉🏅🎖️🗃️
# 🔫🛡️🪃🎣🏹🧨💣🪓🚬🪦🚀
# 💵💴💶💷🪙💰👛
Tiles = {
    '#' : ttk.TTkString('🧱'), # wall
    ' ' : ttk.TTkString('  '),
    '@' : ttk.TTkString('😎'),
    'X' : None,
    'D' : ttk.TTkString('🚪'),
    'DR' : ttk.TTkString('🚪',ttk.TTkColor.bg('#FF0000')),
    'DG' : ttk.TTkString('🚪',ttk.TTkColor.bg('#00FF00')),
    'DB' : ttk.TTkString('🚪',ttk.TTkColor.bg('#0000FF')),
    'KR' : ttk.TTkString('📕'),
    'KG' : ttk.TTkString('📗'),
    'KB' : ttk.TTkString('📘'),
    'd' : ttk.TTkString('| ',ttk.TTkColor.fg('#803000')),
    'z' : ttk.TTkString('🧟'),
    '>' : ttk.TTkString('🪜'),
    'b' : ttk.TTkString('🗃️'), # Black Box
}

class Dungeon(DungeonPrime):
    UP    = 0x01
    DOWN  = 0x02
    LEFT  = 0x03
    RIGHT = 0x04

    def __init__(self) -> None:
        super().__init__()
        self._heroPos = (5,3)
        self._floor = [
                [ttk.TTkColor.bg('#eeddee'),ttk.TTkColor.bg('#ccccee')], # Base
                [ttk.TTkColor.bg('#ddffdd'),ttk.TTkColor.bg('#aaddaa')], # Green
                [ttk.TTkColor.bg('#ddddff'),ttk.TTkColor.bg('#aaaadd')], # Blue
                [ttk.TTkColor.bg('#ffdddd'),ttk.TTkColor.bg('#ddaaaa')]] # Red

    def genDungeon(self):
        self._heroPos=super().genDungeon()

    def heroPos(self):
        return self._heroPos


    def moveHero(self, direction):
        d = self._data
        hx,hy = nx,ny = self._heroPos
        if   direction == self.UP:    ny -= 1
        elif direction == self.DOWN:  ny += 1
        elif direction == self.LEFT:  nx -= 1
        elif direction == self.RIGHT: nx += 1

        # Check if the floor is empty
        if tile:=d[ny][nx] in (' ','d'):
            self._heroPos = (nx,ny)
            return

        # Check if the floor is empty
        if tile:=d[ny][nx] == 'D':
            d[ny][nx] = 'd'
            self._heroPos = (nx,ny)
            return

        # check if I am hitting a wall
        if tile:=d[ny][nx] == '#':
            # Ouch!!!
            return


    def setFading(self, fading):
        self._fading = fading

    # draw the Layers:
    def _drawLayer(self, l, pos, canvas):
        la   = l['layers']
        lpos = l['pos']
        x,y = pos
        for ll,(px,py) in zip(la,lpos):
            w,h = ll.size()
            ll.drawInCanvas(pos=(x+px,y+py),canvas=canvas)

    def drawDungeon(self, pos, canvas:ttk.TTkCanvas):
        x,y = pos
        w,h = canvas.size()
        data     = self._data
        dataType = self._dataType
        # Draw the plane:
        self._drawLayer(self._layerPlane, pos, canvas)
        # Draw the Dungeon:
        fd = self._fading
        dw = int(math.ceil(fd*len(data[0])))
        dh = int(math.ceil(fd*len(data)))
        for cy,row in enumerate(data[0:dh],y):
            for cx,tile in enumerate(row[:dw]):
                ch = Tiles.get(tile)
                color = self._floor[dataType[cy-y][cx]][(cx+cy)%2]
                if ch:
                    canvas.drawTTkString(pos=(x+cx*2,cy),text=ch,color=color)
                # else:
                #     canvas.drawText(pos=(x+cx*2,cy),text="XX",color=color)
        # Place Hero:
        he = Tiles.get('@')
        hx,hy = self._heroPos
        color = self._floor[dataType[hy][hx]][(hx+hy)%2]
        canvas.drawTTkString(pos=(x+hx*2,y+hy),text=he,color=color)


