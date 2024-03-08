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
from .foe    import *

class Dungeon(DungeonPrime):
    UP    = 0x01
    DOWN  = 0x02
    LEFT  = 0x03
    RIGHT = 0x04

    def __init__(self) -> None:
        super().__init__()
        self._mousePos  = (5,3)
        self._heroPos   = (5,3)
        self._mouseLine = []
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
        invMap = {}
        for dx in range(-60,60):
            for dy in range(-30,30):
                invMap[(dx,dy)] = []
                if -50<dx<50 or -50<dy<50:
                    if dy and abs(dy) >= abs(dx):
                        _a = 1 if dy>0 else -1
                        _d = dx/dy
                        for _y in range(0,abs(dy)):
                            _x = math.floor(_d*_y)
                            invMap[(dx,dy)].append((_x*_a,_y*_a))
                    elif dx:
                        _a = 1 if dx>0 else -1
                        _d = dy/dx
                        for _x in range(0,abs(dx)):
                            _y = math.floor(_d*_x)
                            invMap[(dx,dy)].append((_x*_a,_y*_a))
        maps = {}
        for r in invMap:
            for a,b in zip(invMap[r],invMap[r][1:]):
                x,y=a
                if a not in maps: maps[a]=[]
                if (x**2)+(y**2)>15**2:continue
                if b not in maps[a]:maps[a].append(b)
        self._rayMap = maps
        self._ratInvMap = invMap

    def genDungeon(self):
        self._heroPos=super().genDungeon()
        dw,dh = self.size()
        self._rayNum = 1
        self._visibilityMap = [[0]*(dw) for _ in range(dh)]
        self.updateVisibility()

    def updateHeatMap(self):
        dw,dh=self.size()
        hx,hy = self._heroPos
        hmw,hmh = 50,40
        dataMap = self._dataFloor
        vm = self._visibilityMap
        rm = self._rayMap
        rn = self._rayNum = self._rayNum+1
        hm = self._heatMap

        dmy1,dmy2 = max(0, hy-hmh//2), hy+hmw//2
        dmx1,dmx2 = max(0, hx-hmh//2), hx+hmw//2
        for y,row in enumerate(dataMap[dmy1:dmy2],dmy1):
            for x,dm in enumerate(row[dmx1:dmx2],dmx1):
                hm[y][x] = 0x10000 if dm in (' ','d','>') else 0
        # Build a Heat Map of the distances from the hero
        # def _updateDistance(_pos,_d):
        #     _x,_y = _pos
        #     hm[_y][_x] = _d
        #     toBeProcessed = [_pos]
        #     # Move Right
        #     while toBeProcessed:
        #         _x,_y = toBeProcessed.pop()
        #         _d = hm[_y][_x]
        #         if _y > 0    and hm[_y-1][_x]>_d+1: hm[_y-1][_x]=_d+1; toBeProcessed.append((_x  ,_y-1))
        #         if _y < dh-2 and hm[_y+1][_x]>_d+1: hm[_y+1][_x]=_d+1; toBeProcessed.append((_x  ,_y+1))
        #         if _x > 0    and hm[_y][_x-1]>_d+1: hm[_y][_x-1]=_d+1; toBeProcessed.append((_x-1,_y  ))
        #         if _x < dw-2 and hm[_y][_x+1]>_d+1: hm[_y][_x+1]=_d+1; toBeProcessed.append((_x+1,_y  ))
        # _updateDistance((hx,hy),1)
        def _updateDistance(_pos,_d):
            _x,_y = _pos
            if hm[_y][_x] <= _d: return
            hm[_y][_x] = _d
            if _y > 0   :_updateDistance((_x  ,_y-1),_d+1)
            if _y < dh-2:_updateDistance((_x  ,_y+1),_d+1)
            if _x > 0   :_updateDistance((_x-1,_y  ),_d+1)
            if _x < dw-2:_updateDistance((_x+1,_y  ),_d+1)
        _updateDistance((hx,hy),1)

    def updateVisibility(self):
        self.updateHeatMap()
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
        _T = dataMap[hy+1][hx  ] in (' ','d','>')
        _B = dataMap[hy-1][hx  ] in (' ','d','>')
        _L = dataMap[hy  ][hx-1] in (' ','d','>')
        _R = dataMap[hy  ][hx+1] in (' ','d','>')
        if _T or _R : _process([(+1,+1)])
        if _B or _R : _process([(+1,-1)])
        if _T or _L : _process([(-1,+1)])
        if _B or _L : _process([(-1,-1)])
        # _process(rm[(0,0)].copy())
        _process([(1,0),(-1,0),(0,1),(0,-1)])

    def heroPos(self):
        return self._heroPos

    def moveMouse(self, x,y):
        hx,hy = self._heroPos
        self._mousePos = (x,y)
        rim = self._ratInvMap
        dx,dy=x-hx,y-hy
        if (dx,dy) in rim:
            self._mouseLine = [(hx+_x,hy+_y) for _x,_y in rim[(dx,dy)]]
        else:
            self._mouseLine = []
        pass

    def foesAction(self):
        visMap = self._visibilityMap
        rn     = self._rayNum
        dm = self._dataFloor
        df = self._dataFoes
        hm = self._heatMap
        hx,hy = self._heroPos
        for foe in self._foes:
            x,y = foe.pos
            if rn==visMap[y][x]: foe.active = True
            if abs(x-hx)>40 or abs(y-hy)>15: foe.active = False
            if not foe.active: continue
            move,shot = foe.getActions()
            if move:
                ch = hm[y][x]
                if ch < foe.distance:
                    chNew = ch+1
                else:
                    chNew = ch-1
                if chNew > 1:
                    nextTiles = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                    movableTiles = [(_x,_y) for (_x,_y) in nextTiles if (hm[_y][_x]==chNew and not df[_y][_x])]
                    if not movableTiles: # all the tiles are busy or not available
                        movableTiles = [(_x,_y) for (_x,_y) in nextTiles if (hm[_y][_x] and not df[_y][_x])]
                    if movableTiles:
                        _rx,_ry = movableTiles[random.randint(0,len(movableTiles)-1)]
                        foe.pos = (_rx,_ry)
                        df[y][x],df[_ry][_rx] = df[_ry][_rx],df[y][x]

    def heroAction(self):
        pass

    def moveHero(self, direction):
        self._mouseLine = []
        d = self._dataFloor
        hx,hy = nx,ny = self._heroPos
        if   direction == self.UP:    ny -= 1
        elif direction == self.DOWN:  ny += 1
        elif direction == self.LEFT:  nx -= 1
        elif direction == self.RIGHT: nx += 1

        # Check if the floor is empty
        if tile:=d[ny][nx] in (' ','d','>'):
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
                if   rn==vm and fo: ch = Tiles.get(fo.name)
                elif ob: ch = Tiles.get(ob)
                else:    ch = Tiles.get(fl)
                color = self._floor[dataType[cy-y][cx]][0 if vm==rn else 1][(cx+cy+hy+1)%2]
                if (cx,cy-y) in self._mouseLine:
                    color = self._mouseColor
                else:
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

        # for cx,cy in self._mouseLine:
        #     canvas.drawText(pos=(x+cx*2,y+cy),text='XX')



