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
from .assets import *

class Dungeon(DungeonPrime):
    UP    = 0x01
    DOWN  = 0x02
    LEFT  = 0x03
    RIGHT = 0x04

    def __init__(self) -> None:
        super().__init__()
        self._mousePos = (5,3)
        self._heroPos  = (5,3)
        self._mouseColor = ttk.TTkColor.fg('#00FF00')+ttk.TTkColor.bg('#FFFF00')
        # self._mouseIcon = ttk.TTkString("🔆",self._mouseColor)
        self._mouseIcon = ttk.TTkString("🔆")
        self._floor = [
                [[ttk.TTkColor.bg('#eeddee'),ttk.TTkColor.bg('#ccccee')],
                 [ttk.TTkColor.bg('#eeeeee'),ttk.TTkColor.bg('#cccccc')]], # Base
                [[ttk.TTkColor.bg('#ddffdd'),ttk.TTkColor.bg('#aaddaa')],
                 [ttk.TTkColor.bg('#eeeeee'),ttk.TTkColor.bg('#dddddd')]], # Green
                [[ttk.TTkColor.bg('#ddddff'),ttk.TTkColor.bg('#aaaadd')],
                 [ttk.TTkColor.bg('#cccccc'),ttk.TTkColor.bg('#bbbbbb')]], # Blue
                [[ttk.TTkColor.bg('#ffdddd'),ttk.TTkColor.bg('#ddaaaa')],
                 [ttk.TTkColor.bg('#dddddd'),ttk.TTkColor.bg('#cccccc')]], # Red
                [[ttk.TTkColor.bg('#ffffdd'),ttk.TTkColor.bg('#ddddaa')],
                 [ttk.TTkColor.bg('#ffffdd'),ttk.TTkColor.bg('#ddddaa')]]] # Yellow
        self._makeRayMap()
        dw,dh = self.size()
        self._rayNum = 1
        self._visibilityMap = [[0]*(dw) for _ in range(dh)]
        self.updateVisibility()

    def _makeRayMap(self):
        maps = {}
        # . . . . . x . . . . . = 11
        # generate a raymap (101x51) excluding the 45Degrees rays
        for x in range(0,61):
            for y in range(0,60):
                dy1 = y+1
                dy2 = y
                dx1 = math.floor(x*dy1/60)
                dx2 = math.floor(x*dy2/60)
                if (dx2,dy2) not in maps:
                    maps[( dx2, dy2)] = []
                    maps[( dx2,-dy2)] = []
                    maps[(-dx2, dy2)] = []
                    maps[(-dx2,-dy2)] = []
                    maps[( dy2, dx2)] = []
                    maps[( dy2,-dx2)] = []
                    maps[(-dy2, dx2)] = []
                    maps[(-dy2,-dx2)] = []
                if (dx2**2)+(dy2**2)>15**2:continue
                if (d:=( dx1, dy1)) not in (m:=maps[( dx2, dy2)]):m.append(d)
                if (d:=( dx1,-dy1)) not in (m:=maps[( dx2,-dy2)]):m.append(d)
                if (d:=(-dx1, dy1)) not in (m:=maps[(-dx2, dy2)]):m.append(d)
                if (d:=(-dx1,-dy1)) not in (m:=maps[(-dx2,-dy2)]):m.append(d)
                if (d:=( dy1, dx1)) not in (m:=maps[( dy2, dx2)]):m.append(d)
                if (d:=( dy1,-dx1)) not in (m:=maps[( dy2,-dx2)]):m.append(d)
                if (d:=(-dy1, dx1)) not in (m:=maps[(-dy2, dx2)]):m.append(d)
                if (d:=(-dy1,-dx1)) not in (m:=maps[(-dy2,-dx2)]):m.append(d)
        self._rayMap = maps

    def genDungeon(self):
        self._heroPos=super().genDungeon()
        dw,dh = self.size()
        self._rayNum = 1
        self._visibilityMap = [[0]*(dw) for _ in range(dh)]
        self.updateVisibility()

    def updateVisibility(self):
        dw,dh=self.size()
        hx,hy = self._heroPos
        dataMap = self._dataFloor
        vm = self._visibilityMap
        rm = self._rayMap
        rn = self._rayNum = self._rayNum+1
        def _process(_points):
            for _rayPos in _points:
                _rx,_ry=_rayPos
                _px,_py = hx+_rx,hy+_ry
                if not (-25<_rx<25 and -13<_ry<13): continue
                if not (0<=_px<dw-1 and 0<=_py<dh): continue
                vm[_py][_px] = rn
                if dataMap[_py][_px] not in (' ','d','>'):  continue
                # if in a corner, prevent diagonal rays
                #
                #          # _p1
                #         _p  #
                #   h
                #
                _filter = []
                _T = dataMap[_py+1][_px  ] not in (' ','d','>')
                _B = dataMap[_py-1][_px  ] not in (' ','d','>')
                _L = dataMap[_py  ][_px-1] not in (' ','d','>')
                _R = dataMap[_py  ][_px+1] not in (' ','d','>')
                if _T and _R : _filter += [(_rx+1,_ry+1)]
                if _B and _R : _filter += [(_rx+1,_ry-1)]
                if _T and _L : _filter += [(_rx-1,_ry+1)]
                if _B and _L : _filter += [(_rx-1,_ry-1)]
                _newp = [_rr for _rr in rm[(_rx,_ry)] if _rr not in _filter]
                _process(_newp)
        _process(rm[(0,0)].copy())

    def updateVisibilityLoop(self):
        dw,dh=self.size()
        hx,hy = self._heroPos
        dataMap = self._dataFloor
        vm = self._visibilityMap
        rm = self._rayMap
        toBeProcessed = rm[(0,0)].copy()
        def _s(_p,_r): return _p-1 if _r<0 else _p+1
        while toBeProcessed:
            _rx,_ry=_rayPos = toBeProcessed.pop()
            _px,_py = hx+_rx,hy+_ry
            if not (-25<_rx<25 and -13<_ry<13): continue
            if not (0<=_px<dw-1 and 0<=_py<dh): continue
            vm[_py][_px] = 1
            if dataMap[_py][_px] not in (' ','d','>'):  continue
            # if in a corner, prevent diagonal rays
            #
            #          # _p1
            #         _p  #
            #   h
            #
            filter = []
            _T = dataMap[_py+1][_px  ] not in (' ','d','>')
            _B = dataMap[_py-1][_px  ] not in (' ','d','>')
            _L = dataMap[_py  ][_px-1] not in (' ','d','>')
            _R = dataMap[_py  ][_px+1] not in (' ','d','>')
            if _T and _R : filter += [(_rx+1,_ry+1)]
            if _B and _R : filter += [(_rx+1,_ry-1)]
            if _T and _L : filter += [(_rx-1,_ry+1)]
            if _B and _L : filter += [(_rx-1,_ry-1)]
            toBeProcessed += [_rr for _rr in rm[(_rx,_ry)] if _rr not in filter]


    def updateVisibilityOld(self):
        dw,dh=self.size()
        vm = self._visibilityMap
        dataMap = self._dataFloor
        def _recurseMark(_pos):
            _px,_py = _pos
            vm[_py][_px] = 1
            toBeProcessed = [
                (_px  ,_py-1),
                (_px  ,_py+1),
                (_px-1,_py  ),
                (_px+1,_py  ),
                (_px+1,_py-1),
                (_px+1,_py+1),
                (_px-1,_py-1),
                (_px-1,_py+1)]
            # Move Right
            while toBeProcessed:
                _x,_y = toBeProcessed.pop()
                if not (0<=_x<dw-1 and 0<=_y<dh): continue
                if abs(_x-_px) > 60 or abs(_y-_py)>15: continue
                vm[_y][_x] = 1
                if dataMap[_y][_x] not in (' ','d','<'): continue
                if _y<_py:
                    if abs(_x-_px)<_py-_y:
                        toBeProcessed.append((_x  ,_y-1))
                        if   _x<_px: toBeProcessed.append((_x-1  ,_y-1))
                        elif _x>_px: toBeProcessed.append((_x+1  ,_y-1))
                if _y>_py:
                    if abs(_x-_px)<_y-_py:
                        toBeProcessed.append((_x  ,_y+1))
                        if   _x<_px: toBeProcessed.append((_x-1  ,_y+1))
                        elif _x>_px: toBeProcessed.append((_x+1  ,_y+1))
                if _x<_px:
                    if abs(_y-_py)<_px-_x:
                        toBeProcessed.append((_x-1  ,_y))
                        if   _y<_py: toBeProcessed.append((_x-1  ,_y-1))
                        elif _y>_py: toBeProcessed.append((_x-1  ,_y+1))
                if _x>_px:
                    if abs(_y-_py)<_x-_px:
                        toBeProcessed.append((_x+1  ,_y))
                        if   _y<_py: toBeProcessed.append((_x+1  ,_y-1))
                        elif _y>_py: toBeProcessed.append((_x+1  ,_y+1))
                # if _y>_py:
                #     if abs(_x-_px)<=abs(_y-_py): toBeProcessed.append((_x  ,_y+1))
                #     else:toBeProcessed.append((_x  ,_y+1))
                # if _x<_px:
                #     if abs(_x-_px)>=abs(_y-_py): toBeProcessed.append((_x-1,_y  ))
                #     else:toBeProcessed.append((_x-1,_y  ))
                # if _x>_px:
                #     if abs(_x-_px)>=abs(_y-_py): toBeProcessed.append((_x+1,_y  ))
                #     else:toBeProcessed.append((_x+1,_y  ))
        _recurseMark(self._heroPos)

    def heroPos(self):
        return self._heroPos

    def moveMouse(self, x,y):
        self._mousePos = (x,y)

    def moveHero(self, direction):
        d = self._dataFloor
        hx,hy = nx,ny = self._heroPos
        if   direction == self.UP:    ny -= 1
        elif direction == self.DOWN:  ny += 1
        elif direction == self.LEFT:  nx -= 1
        elif direction == self.RIGHT: nx += 1

        # Check if the floor is empty
        if tile:=d[ny][nx] in (' ','d'):
            self._heroPos = (nx,ny)
            self.updateVisibility()
            return

        # Check if the floor is empty
        if tile:=d[ny][nx] == 'D':
            d[ny][nx] = 'd'
            self._heroPos = (nx,ny)
            self.updateVisibility()
            return

        # check if I am hitting a wall
        if tile:=d[ny][nx] == '#':
            # Ouch!!!
            return


    def setFading(self, fading):
        self._fading = fading

    # draw the Layers:
    def _drawLayer(self, l, pos, canvas):
        x,y = pos
        for la in l:
            ll = la['layer']
            px,py = la['pos']
            # w,h = ll.size()
            ll.drawInCanvas(pos=(x+px,y+py),canvas=canvas)

    def drawDungeon(self, pos, canvas:ttk.TTkCanvas):
        x,y = pos
        hx,hy = self._heroPos
        w,h = canvas.size()
        dataFloor = self._dataFloor
        dataType  = self._dataType
        dataFoes  = self._dataFoes
        dataObjs  = self._dataObjs
        visMap    = self._visibilityMap
        rn        = self._rayNum
        # Draw the plane:
        self._drawLayer(self._layerPlane, pos, canvas)
        # Draw the Dungeon:
        fd = self._fading
        dw = int(math.ceil(fd*len(dataFloor[0])))
        dh = int(math.ceil(fd*len(dataFloor)))

        ssh = slice(0,dh+1)
        ssw = slice(0,dw+1)
        for cy,(rof,rot,rofoe,roobj,rvm) in enumerate(zip(dataFloor[ssh],dataType[ssh],dataFoes[ssh],dataObjs[ssh],visMap[ssh]),y):
            for cx,(fl,ty,fo,ob,vm) in enumerate(zip(rof[ssw],rot[ssw],rofoe[ssw],roobj[ssw],rvm[ssw])):
                if not fl or not vm: continue
                if   rn==vm and fo: ch = Tiles.get(fo)
                elif ob: ch = Tiles.get(ob)
                else:    ch = Tiles.get(fl)
                color = self._floor[dataType[cy-y][cx]][0 if vm==rn else 1][(cx+cy+hy+1)%2]
                if ch:
                    canvas.drawTTkString(pos=(x+cx*2,cy),text=ch,color=color)
                # else:
                #     canvas.drawText(pos=(x+cx*2,cy),text="XX",color=color)
        # Place Hero:
        he = Tiles.get('@')
        color = self._floor[dataType[hy][hx]][0][(hx+hy)%2]
        canvas.drawTTkString(pos=(x+hx*2,y+hy),text=he,color=color)

        if self._mousePos:
            mpx,mpy = self._mousePos
            if 0<=mpx<dw and 0<=mpy<dh and visMap[mpy][mpx]:
                canvas.drawTTkString(pos=(x+mpx*2,y+mpy),text=self._mouseIcon,color=color)



