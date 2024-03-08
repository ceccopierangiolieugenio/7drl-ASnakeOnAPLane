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

__all__ = ['DungeonPrime']

import sys, os, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .assets import *
from .layer  import *
from .glbls  import *
from .foe    import *

STARTING_FLOOR = [
    [''  ,''  ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,''  ,''  ,''  ,'#' ,'#' ,'#' ,''  ,''  ,''  ,'#' ,'#' ,'#' ,'#' ,'#' ,''  ,'' ,],
    [''  ,'#' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,''  ,''  ,'#' ,' ' ,' ' ,' ' ,'#' ,''  ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,'' ,],
    ['#' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,'#' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#',],
    ['#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'DB',' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#',],
    ['#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'D' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'>' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,'#' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#',],
    ['#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'DG',' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#',],
    [''  ,'#' ,' ' ,' ' ,' ' ,' ' ,'#' ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,' ' ,' ' ,' ' ,' ' ,'D' ,' ' ,'#' ,''  ,'#' ,' ' ,' ' ,' ' ,' ' ,' ' ,'#' ,'' ,],
    [''  ,''  ,'#' ,'#' ,'#' ,'#' ,''  ,''  ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,''  ,''  ,''  ,'#' ,'#' ,'#' ,'#' ,'#' ,''  ,'' ,],
    ]
STARTING_TYPE = [
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    [ 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 1  , 1  , 1  , 1  , 1  , 1  , 1  , 0  , 2  , 2  , 2  , 2  , 2  , 2  , 2  , 2  ],
    ]
STARTING_OBJS = [
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,'KG',''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,'b' ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,'KB',''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    ]
STARTING_FOES = [
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,'z' ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,'z' ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,'z' ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    [''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ,''  ],
    ]

class DungeonPrime():
    UP    = 0x01
    DOWN  = 0x02
    LEFT  = 0x03
    RIGHT = 0x04

    def __init__(self) -> None:
        self._fading = 1.0
        self._plf  = plf  = Layer(PLANE_FRONT)
        self._plb  = plb  = Layer(PLANE_BACK)
        self._plb1 = plb1 = Layer(PLANE_BODY_1)
        wplf,hplf = plf.size()
        wplb,hplb = plb.size()
        self._layerPlane = [{'layer':plf,'pos':(wplb-27,-1)},
                            {'layer':plb,'pos':(-18,-7)}]

        self._dataFloor = STARTING_FLOOR
        self._dataType  = STARTING_TYPE
        self._dataObjs  = STARTING_OBJS
        renamedFoes     = [[(f if f!='z' else 'Zombie') for f in row] for row  in STARTING_FOES]
        self._dataFoes  = [[(Foe(pos=(x,y),name=f,**FOELIST[f]) if f else None) for x,f in enumerate(row)] for y,row in enumerate(renamedFoes)]
        self._heatMap  = [[0]*len(STARTING_FLOOR[0]) for _ in STARTING_FLOOR]
        self._foes:list[Foe] = []
        for row in self._dataFoes: self._foes += [f for f in row if f]
        self._tmpData = {}
        self._size = (len(STARTING_FLOOR[0]),len(STARTING_FLOOR))

    def size(self):
        return self._size

    ####################################################
    ####################################################
    ####################################################
    def genPlane(self):
        level = glbls.level
        plf  = self._plf
        plb  = self._plb
        plb1 = self._plb1
        wplf,hplf   = plf.size()
        wplb,hplb   = plb.size()
        wplb1,hplb1 = plb1.size()

        # Based on the level [1,5] define the planes placement area
        planesArea = {
            1 : (10,10),
            2 : (40,15),
            3 : (10,30),
            4 : (30,20),
            5 : (30,30),
        }.get(level)

        # place the parts on a random position in their areas
        newLayer = self._tmpData['layer'] = []

        # Place n central body based on the available space
        bodies = []
        def _freeBodySpace():
            _availableSpaces = []
            for _x in range(planesArea[0]):
                for _y in range(planesArea[1]):
                    isItOk = True
                    for _bx,_by in bodies:
                        if abs(_bx-_x) < wplb1-15 and abs(_by-_y) < hplb1-6:
                            isItOk = False
                            break
                    if isItOk:
                        _availableSpaces.append((_x,_y))
            if _availableSpaces:
                return _availableSpaces[random.randint(0,len(_availableSpaces)-1)]
            return None

        while _pos:=_freeBodySpace():
            bodies.append(_pos)
            newLayer.append({'layer':plb1, 'pos':_pos})


        # get the leftmost bodies:
        rightmostBodies = []
        leftmostBodies = []
        for _x,_y in bodies:
            hasSomeOnTheRight = False
            hasSomeOnTheLeft = False
            for _cx,_cy in bodies:
                if (_cx,_cy)==(_x,_y): continue
                if _cx>_x and abs(_cy-_y)<hplb1-2:
                    hasSomeOnTheRight=True
                if _cx<_x and abs(_cy-_y)<hplb1-2:
                    hasSomeOnTheLeft=True
            if not hasSomeOnTheRight:
                rightmostBodies.append((_x,_y))
            if not hasSomeOnTheLeft:
                leftmostBodies.append((_x,_y))

        # place the fronts
        for _x,_y in random.sample(rightmostBodies,random.randint(1,len(rightmostBodies))):
            _x += wplb1+random.randint(-25,-5)
            _y += random.randint(4,8)
            newLayer.append({'layer':plf, 'pos':(_x,_y)})
        # place the backs
        for _x,_y in random.sample(leftmostBodies,random.randint(1,len(leftmostBodies))):
            _x -= wplb+random.randint(-35,-5)
            _y += random.randint(-8,2)
            newLayer.append({'layer':plb, 'pos':(_x,_y)})

        minx=0x1000
        miny=0x1000
        maxx=-0x1000
        maxy=-0x1000
        # Normalize
        for nl in newLayer:
            w,h=nl['layer'].size()
            px,py=nl['pos']
            minx = min(minx,px)
            miny = min(miny,py)
            maxx = max(maxx,px+w)
            maxy = max(maxy,py+h)
        # newLayer['pos'] = [(x-minx,y-miny) for (x,y) in newLayer['pos']]
        for nl in newLayer: px,py=nl['pos'] ; nl['pos'] = (px-minx,py-miny)
        newLayer = sorted(newLayer, key=lambda x: x['pos'][1], reverse=False)
        self._tmpData['layer'] = newLayer
        self._tmpData['dsize'] = ((maxx-minx)//2, maxy-miny)

    ####################################################
    ####################################################
    ####################################################
    def genMainArea(self):
        level = glbls.level
        # find the walkable places
        newLayer = self._tmpData['layer']
        dw,dh = self._tmpData['dsize']
        data0 = [['']*(dw) for _ in range(dh)]
        for nl in newLayer:
            l = nl['layer']
            lw,lh=l.size()
            x,y=nl['pos']
            for ly in range(lh):
                for lx in range(((lw-1)//2)*2):
                    cl1 = l.getColor(lx,ly)
                    cl2 = l.getColor(lx+1,ly)
                    if cl1[1] and cl2[1]:
                        data0[ly+y][(lx+x)//2]=' '


        data1 = self._tmpData['dataFloor'] = [[' ']*(dw) for _ in range(dh)]
        self._tmpData['dataType'] = [[0]*(dw) for _ in range(dh)]
        self._tmpData['dataObjs'] = [['']*(dw) for _ in range(dh)]
        self._tmpData['dataFoes'] = [['']*(dw) for _ in range(dh)]
        # reduce the area by 1
        for y,row in enumerate(data0):
            for x,ch in enumerate(row):
                if x==0 or x==dw-1 or y==0 or y==dh-1:
                    data1[y][x] = ''
                if not ch :
                    data1[max(   0,y-1)][max(   0,x-1)] = ''
                    data1[max(   0,y-1)][max(   0,x  )] = ''
                    data1[max(   0,y-1)][min(dw-1,x+1)] = ''
                    data1[max(   0,y  )][max(   0,x-1)] = ''
                    data1[max(   0,y  )][max(   0,x  )] = ''
                    data1[max(   0,y  )][min(dw-1,x+1)] = ''
                    data1[min(dh-1,y+1)][max(   0,x-1)] = ''
                    data1[min(dh-1,y+1)][max(   0,x  )] = ''
                    data1[min(dh-1,y+1)][min(dw-1,x+1)] = ''

        # add wall
        for y,row in enumerate(data1):
            for x,ch in enumerate(row):
                if ch == ' ':
                    if (
                       not data1[max(   0,y-1)][max(   0,x-1)] or
                       not data1[max(   0,y-1)][max(   0,x  )] or
                       not data1[max(   0,y-1)][min(dw-1,x+1)] or
                       not data1[max(   0,y  )][max(   0,x-1)] or
                       not data1[max(   0,y  )][max(   0,x  )] or
                       not data1[max(   0,y  )][min(dw-1,x+1)] or
                       not data1[min(dh-1,y+1)][max(   0,x-1)] or
                       not data1[min(dh-1,y+1)][max(   0,x  )] or
                       not data1[min(dh-1,y+1)][min(dw-1,x+1)] ):
                        data1[y][x] = '#'

    ####################################################
    ####################################################
    ####################################################
    def ensureConnection(self):
        level = glbls.level
        # find the walkable places
        dw,dh = self._tmpData['dsize']
        data  = self._tmpData['dataFloor']
        # Create a map with
        # 1 for walkable tiles,
        # 0 for not walkable tiles
        # I will use it to check if thre are not reachable areas
        dataMap = [[1 if ch ==' ' else 0 for ch in row] for row in data]
        # find the first walcable tile and mark it as 2
        for y,row in enumerate(dataMap):
            for x,ch in enumerate(row):
                if ch:
                    wtile = (x,y)
                    break
            if ch:break # What a piece of crap
        # Now recursively process all the tiles to check if those are connected
        # PUDATE: Reduce recursivity because bigger dungeons exceeed its max depth
        def _recurseMark(_pos,_num):
            # _x,_y = _pos
            # if  not  dataMap[_y][_x]: return
            # if _num==dataMap[_y][_x]: return
            # dataMap[_y][_x] = _num
            # if _y > 0   : _recurseMark((_x,_y-1),_num)
            # if _y < dh-2: _recurseMark((_x,_y+1),_num)
            # if _x > 0   : _recurseMark((_x-1,_y),_num)
            # if _x < dw-2: _recurseMark((_x+1,_y),_num)
            toBeProcessed = [_pos]
            # Move Right
            while toBeProcessed:
                _x,_y = toBeProcessed.pop()
                dataMap[_y][_x] = _num
                if _y > 0    and (_dm:=dataMap[_y-1][_x]) and _dm!=_num and (_x  ,_y-1) not in toBeProcessed: toBeProcessed.append((_x  ,_y-1))
                if _y < dh-2 and (_dm:=dataMap[_y+1][_x]) and _dm!=_num and (_x  ,_y+1) not in toBeProcessed: toBeProcessed.append((_x  ,_y+1))
                if _x > 0    and (_dm:=dataMap[_y][_x-1]) and _dm!=_num and (_x-1,_y  ) not in toBeProcessed: toBeProcessed.append((_x-1,_y  ))
                if _x < dw-2 and (_dm:=dataMap[_y][_x+1]) and _dm!=_num and (_x+1,_y  ) not in toBeProcessed: toBeProcessed.append((_x+1,_y  ))

        def _checkAreas():
            _a =_b = None
            _an=_bn=0,0
            for _y,_row in enumerate(dataMap):
                for _x,_ch in enumerate(_row):
                    if _ch and not _a:
                        _an=_bn=_ch
                        _a=_b=(_x,_y)
                    elif _ch and _ch!= _an:
                        _b=(_x,_y)
                        return _a,_b
            return _a,_b

        def _connect(_a,_b):
            def _surroundWall(__p):
                __x,__y = __p
                if __y>0    and not dataMap[__y-1][__x  ]: data[__y-1][__x  ]='#'
                if __y<dh-2 and not dataMap[__y+1][__x  ]: data[__y+1][__x  ]='#'
                if __x>0    and not dataMap[__y  ][__x-1]: data[__y  ][__x-1]='#'
                if __x<dw-2 and not dataMap[__y  ][__x+1]: data[__y  ][__x+1]='#'
            _xa,_ya = _a
            _xb,_yb = _b
            _w = max(_xa,_xb)-min(_xa,_xb)
            _h = max(_ya,_yb)-min(_ya,_yb)
            _num = dataMap[_ya][_xa]
            _surroundWall(a)
            _surroundWall(b)
            for _x in range(min(_xa,_xb),max(_xa,_xb)+1):
                dataMap[_ya][_x] = _num
                data[_ya][_x] = ' '
                _surroundWall((_x,_ya))
            for _y in range(min(_ya,_yb),max(_ya,_yb)+1):
                dataMap[_y][_xb] = _num
                data[_y][_xb] = ' '
                _surroundWall((_xb,_y))

        def _findRandomInArea(_pos):
            _x,_y = _pos
            _ll = []
            _num = dataMap[_y][_x]
            for _y,_row in enumerate(dataMap):
                for _x,_ch in enumerate(_row):
                    if _ch == _num:
                        _ll.append((_x,_y))
            return _ll[random.randint(0,len(_ll)-1)]

        recurseId = 2
        _recurseMark(wtile,recurseId)
        a,b = _checkAreas()
        while a!=b:
            recurseId+=1
            # _connect(a,b)
            _connect(_findRandomInArea(a),_findRandomInArea(b))
            _recurseMark(a,recurseId)
            a,b = _checkAreas()


    ####################################################
    ####################################################
    ####################################################
    def genWalls(self):
        level = glbls.level
        # find the walkable places
        dw,dh = self._tmpData['dsize']
        data  = self._tmpData['dataFloor']
        # Create a map with
        # 1 for Roomable tiles,
        # 0 for not walkable tiles
        # I will use it to check if thre are not reachable areas
        dataMap = [[1 if ch ==' ' else 0 for ch in row] for row in data]

        def _findRandomInArea(_num,_w,_h):
            _ll = []
            for _y,_row in enumerate(dataMap):
                if _y+_h >= dh: break
                for _x,_ch in enumerate(_row):
                    if _x+_w >= dw: break
                    if _ch == _num:
                        # Check if all the tiles in this area have the same _num
                        # I know, it's a bit convoluted
                        if all([
                            all([__ch == _num for __ch in dataMapY[_x:_x+_w]])
                            for dataMapY in dataMap[_y:_y+_h]]):
                            _ll.append((_x,_y))
            if not _ll: return None
            return _ll[random.randint(0,len(_ll)-1)]

        def _placeRoom(_pos,_size,_corner):
            # Draw Walls
            _x,_y = _pos
            _w,_h = _size
            # Draw Walls
            for _yy in range(_y+_corner,_y+_h-_corner+1):
                if data[_yy][_x-1]==' ':
                    data[_yy][_x ]     = '#'
                if data[_yy][_x+_w+1]==' ':
                    data[_yy  ][_x+_w] = '#'
            for _xx in range(_x+_corner,_x+_w-_corner+1):
                if data[_y-1][_xx]==' ':
                    data[_y ][_xx]     = '#'
                if data[_y+_h+1][_xx]==' ':
                    data[_y+_h][_xx] = '#'
            # Draw Walkable Floor
            for _yy in range(_y+1,_y+_h):
                for _xx in range(_x+1,_x+_w):
                    data[_yy][_xx] = ' '
            _rw = random.randint(0,_w//4)
            _rh = random.randint(0,_h//4)
            for _yy in range(_y+_rh,_y+_h-_rh+1):
                for _xx in range(_x+_rw,_x+_w-_rw+1):
                    dataMap[_yy][_xx] = 0

        # Add a room
        for i in range(random.randint(3,15)):
            rw = random.randint(4,15)
            rh = random.randint(4,6)
            if not (rpos:= _findRandomInArea(1,rw,rh)):
                break
            _placeRoom(rpos,(rw,rh),0)


    ####################################################
    ####################################################
    ####################################################
    def genDoors(self):
        level = glbls.level
        # find the walkable places
        dw,dh = self._tmpData['dsize']
        dataFloor  = self._tmpData['dataFloor']
        dataType = self._tmpData['dataType'] = [[5 if ch ==' ' else 0 for ch in row] for row in dataFloor]

        # Create a map with
        # 1 for walkable tiles,
        # 0 for not walkable tiles
        # I will use it to check if thre are not reachable areas
        areaMap = self._tmpData['areaMap'] = [[1 if ch ==' ' else 0 for ch in row] for row in dataFloor]
        # dataMapType = [[1 if ch ==' ' else 0 for ch in row] for row in dataFloor]

        # Divide the dungeons in walkable areas

        # find the first walcable tile with _num
        def _getFirst(_num):
            for y,row in enumerate(areaMap):
                for x,ch in enumerate(row):
                    if ch == _num:
                        return (x,y)
            return None

        # Process all the tiles and mark the connected ones
        def _recurseMark(_data,_pos,_num):
            toBeProcessed = [_pos]
            # Move Right
            while toBeProcessed:
                _x,_y = toBeProcessed.pop()
                _data[_y][_x] = _num
                if _y > 0    and (_dm:=_data[_y-1][_x]) and _dm!=_num and (_x  ,_y-1) not in toBeProcessed: toBeProcessed.append((_x  ,_y-1))
                if _y < dh-2 and (_dm:=_data[_y+1][_x]) and _dm!=_num and (_x  ,_y+1) not in toBeProcessed: toBeProcessed.append((_x  ,_y+1))
                if _x > 0    and (_dm:=_data[_y][_x-1]) and _dm!=_num and (_x-1,_y  ) not in toBeProcessed: toBeProcessed.append((_x-1,_y  ))
                if _x < dw-2 and (_dm:=_data[_y][_x+1]) and _dm!=_num and (_x+1,_y  ) not in toBeProcessed: toBeProcessed.append((_x+1,_y  ))


        # Assign an Area Id for all the connected tiles
        markId = 1
        while fpos := _getFirst(1):
            markId+=1
            _recurseMark(areaMap,fpos,markId)

        def _getWalls(_area):
            _walls = {}
            def __checkWall(__x,__y,_walls=_walls):
                if dataFloor[__y][__x] == '#' and (__x,__y) not in _walls:
                    # List the areas connected to this wall
                    _conn = set()
                    if __x>0    and (__a:=areaMap[__y][__x-1]): _conn.add(__a)
                    if __x<dw-1 and (__a:=areaMap[__y][__x+1]): _conn.add(__a)
                    if __y>0    and (__a:=areaMap[__y-1][__x]): _conn.add(__a)
                    if __y<dh-1 and (__a:=areaMap[__y+1][__x]): _conn.add(__a)
                    if _area in _conn and len(_conn)==2:
                        _walls[(__x,__y)]=list(_conn)
            for _y,_row in enumerate(areaMap[1:dh-1],1):
                for _x,_ch in enumerate(_row[1:dw-1],1):
                    if _ch == _area:
                        __checkWall(_x+1,_y)
                        __checkWall(_x-1,_y)
                        __checkWall(_x,_y+1)
                        __checkWall(_x,_y-1)
            return _walls

        # create an Area Tree
        processedAreas = [False]*(markId+1)
        def _treeFromArea(_area, _type, _depth):
            if processedAreas[_area]: return None
            processedAreas[_area] = True
            if _pos := _getFirst(_area):
                _recurseMark(dataType,_pos,_type)
            _walls = _getWalls(_area)
            # ttk.TTkLog.debug(f"Tree: {_area} - {_walls} ")
            _connections = []
            for _w in _walls:
                for _ca in _walls[_w]:
                    # ttk.TTkLog.debug(f"try: {_area} -> {_ca}")
                    _newType = _type if _depth<3 or _type>=3 or random.randint(0,2) else _type+1
                    if _cont := _treeFromArea(_ca, _newType, _depth+1):
                        # ttk.TTkLog.debug(f"{_area} -> {_ca}")
                        _connections.append(_cont)
            return {'area':_area, 'connections':_connections, 'walls':_walls, 'type':_type}

        fullTree = _treeFromArea(_startingArea:=random.randint(2,markId), 0, 0)

        def _getAreaType(_tree, _area):
            if _tree['area'] == _area:
                return _tree['type']
            for _c in _tree['connections']:
                if _ret:=_getAreaType(_c,_area):
                    return _ret
            return 0

        def _placeDoors(_tree):
            _tw = _tree['walls']
            for _c in _tree['connections']:
                _wllsAll = list(_tw.keys())
                _wlls = [_w for _w in _tw if _c['area'] in _tw[_w]]
                def __addDoor(__wll):
                    __x,__y = __wll
                    _type1 = _getAreaType(fullTree,_tw[__wll][0])
                    _type2 = _getAreaType(fullTree,_tw[__wll][1])
                    if _type1 != _type2 :
                        dataFloor[__y][__x] = ['D','DG','DB','DR'][max(_type1,_type2)]
                        dataType[__y][__x] = max(_type1,_type2)
                    else:
                        dataFloor[__y][__x] = 'D'
                        dataType[__y][__x] = _type1
                __addDoor(_wlls[random.randint(0,len(_wlls)-1)])
                # Add extra door randomly
                if not random.randint(0,2):
                    __addDoor(_wllsAll[random.randint(0,len(_wllsAll)-1)])
                _placeDoors(_c)

        # for _c in areasTrees:
        #     _placeDoors(_c)
        _placeDoors(fullTree)

        # Remove unreachable tiles
        self._tmpData['dataType'] = [[0 if ch ==5 else ch for ch in row] for row in dataType]

        def _findRandomInArea(_num):
            _ll = []
            for _y,_row in enumerate(areaMap):
                for _x,_ch in enumerate(_row):
                    if _ch == _num:
                        _ll.append((_x,_y))
            return _ll[random.randint(0,len(_ll)-1)]
        self._tmpData['heroPos'] = _findRandomInArea(_startingArea)


    ####################################################
    ####################################################
    ####################################################
    def placeKeys(self):
        # find the walkable places
        heroPos = self._tmpData['heroPos']
        dw,dh = self._tmpData['dsize']
        dataFloor= self._tmpData['dataFloor']
        dataType = self._tmpData['dataType']
        dataObjs  = self._tmpData['dataObjs']

        heatMap  = self._tmpData['heatMap'] = [[0x10000 if ch in (' ','D','DR','DG','DB') else 0 for ch in row] for row in dataFloor]
        listKeys = self._tmpData['listKeys'] = []

        # Build a Heat Map of the distances from the hero
        def _updateDistance(_pos,_d):
            _x,_y = _pos
            heatMap[_y][_x] = _d
            toBeProcessed = [_pos]
            # Move Right
            while toBeProcessed:
                _x,_y = toBeProcessed.pop()
                _d = heatMap[_y][_x]
                if _y > 0    and heatMap[_y-1][_x]>_d+1: heatMap[_y-1][_x]=_d+1; toBeProcessed.append((_x  ,_y-1))
                if _y < dh-2 and heatMap[_y+1][_x]>_d+1: heatMap[_y+1][_x]=_d+1; toBeProcessed.append((_x  ,_y+1))
                if _x > 0    and heatMap[_y][_x-1]>_d+1: heatMap[_y][_x-1]=_d+1; toBeProcessed.append((_x-1,_y  ))
                if _x < dw-2 and heatMap[_y][_x+1]>_d+1: heatMap[_y][_x+1]=_d+1; toBeProcessed.append((_x+1,_y  ))
        _updateDistance(heroPos,1)


        distancesByType = self._tmpData['distancesByType'] = {}
        for _y,(_rh,_rt) in enumerate(zip(heatMap,dataType)):
            for _x,(_d,_t) in enumerate(zip(_rh,_rt)):
                if not _t in distancesByType:
                  distancesByType[_t] = {'pos':(_x,_y),'max':_d,'min':_d}
                elif distancesByType[_t]['max'] < _d:
                    distancesByType[_t]['max'] = _d
                elif distancesByType[_t]['min'] > _d:
                    distancesByType[_t]['min'] = _d

        def _randomDistanceInType(_dists,_type):
            _fr,_to = _dists
            _distances = []
            for _y,(_rh,_rt,_rfl) in enumerate(zip(heatMap,dataType,dataFloor)):
                for _x,(_d,_t,_fl) in enumerate(zip(_rh,_rt,_rfl)):
                      if _fr<=_d<=_to and _t<=_type and _fl==' ':
                        _distances.append((_x,_y))
            if _distances:
                return _distances[random.randint(0,len(_distances)-1)]
            return None

        # Place the keys in the farthest position based on the previous areaType
        for _a in distancesByType:
            if not _a: continue
            _dmax = distancesByType[_a-1]['max']
            _dmin = distancesByType[_a-1]['min']
            _da = (_dmax+_dmin)//2
            _db = random.randint(_da+(_dmax-_dmin)//4,_dmax)
            if not(_rdis := _randomDistanceInType((_da,_db),_a-1)):
                continue
            _x,_y = _rdis
            dataObjs[_y][_x] = ['KG','KB','KR'][_a-1]
            listKeys.append({'type':_a,'area':dataType[_y][_x]})

    ####################################################
    ####################################################
    ####################################################
    def placeFoesObjs(self):
        level = glbls.level
        # find the walkable places
        heroPos = self._tmpData['heroPos']
        dw,dh = self._tmpData['dsize']
        areaMap = self._tmpData['areaMap']
        dataFloor= self._tmpData['dataFloor']
        dataType = self._tmpData['dataType']
        dataObjs  = self._tmpData['dataObjs']
        dataFoes = self._tmpData['dataFoes']
        foeList = self._tmpData['foes'] = []
        heatMap  = self._tmpData['heatMap']
        listKeys = self._tmpData['listKeys']
        distancesByType = self._tmpData['distancesByType']

        mapSize     = sum([sum([1 if ch == ' ' else 0 for ch in row]) for row in dataFloor])
        maxDistance = max([max([d if d < 0x10000 else 0 for d in row]) for row in heatMap])
        maxType     = max([max(row) for row in dataType])

        # Based on the level [1,5] define the planes placement area
        foesList = [
            'Zombie','Vampire','Ghost',
            'Zombie','Vampire','Ghost',
            'Zombie','Vampire','Ghost',
            'Pumpkin','Imp','Imp',
            'Pumpkin','Imp','Imp',
            'Pumpkin','Imp','Imp',
            'Robot','Robot','Crap',
            'Robot','Robot','Crap',
            'Robot','Robot','Crap',
            'SI','SI','Alien',
            'SI','SI','Alien',
            'SI','SI','Alien',
            'Dragon','TRex','TRex',
            'Dragon','TRex','TRex',
            'Dragon','TRex','TRex']

        objList = [
            'af1','ah1','ab1','al1', 'wm1','wr1', 'g1','g2','g3', 'ws1','ws1','ws1','wt1',
                                                  'g1','g2','g3', 'ws1','ws1','ws1','wt1',
                                                                  'ws1','ws1','ws1','wt1',
                                                                  'ws1','ws1','ws1','wt1',

            'af2','ah2','ab2','al2', 'wm2','wr2', 'g3','g4','g5', 'ws1','ws1','ws1','wt1',
                                                  'g3','g4','g5', 'ws1','ws1','ws1','wt1',
                                                                  'ws2','ws2','ws2','wt2',
                                                                  'ws2','ws2','ws2','wt2',

            'af3','ah3','ab3','al3', 'wm3','wr3', 'g4','g5','g7', 'ws1','ws1','ws1','ws1','wt1',
                                                  'g4','g5','g7', 'ws2','ws2','ws2','ws2','wt2',
                                                                  'ws3','ws3','ws3','ws3','wt3',
                                                                  'ws3','ws3','ws3','ws3','wt3',

            'af4','ah4','ab3','al3', 'wm4','wr4', 'g5','g7','g8', 'ws1','ws1','ws1','ws1','ws1','wt1',
                                                  'g5','g7','g8', 'ws2','ws2','ws2','ws2','ws2','wt2',
                                                                  'ws3','ws3','ws3','ws3','ws3','wt3',
                                                                  'ws4','ws4','ws4','ws4','ws4','wt4',

            'af4','ah4','ab4','al3', 'wm4','wr4', 'g6','g7','g8', 'ws1','ws1','ws1','ws1','ws1','wt1','wt1',
                                                  'g6','g7','g8', 'ws2','ws2','ws2','ws2','ws2','wt2','wt2',
                                                                  'ws3','ws3','ws3','ws3','ws3','wt3','wt3',
                                                                  'ws4','ws4','ws4','ws4','ws4','wt4','wt4',
        ]

        # Reduce the number of possible foes based on the level
        # I assume that the latest foes are stronger
        foesList = foesList[0:level*len(foesList)//5]
        objList  = objList[(level-1)*len(objList)//5:level*len(objList)//5]

        # At least 1 foe every 20x3
        # and no more than 6x3
        foes = random.randint(mapSize//(20*3),mapSize//(6*3))
        objs = random.randint(foes,3*foes//2)

        def _randomDistanceInType(_dists,_type):
            _fr,_to = _dists
            _distances = []
            for _y,(_rh,_rt,_rfl,_rob,_rfo) in enumerate(zip(heatMap,dataType,dataFloor,dataObjs,dataFoes)):
                for _x,(_d,_t,_fl,_ob,_fo) in enumerate(zip(_rh,_rt,_rfl,_rob,_rfo)):
                      if _fr<=_d<=_to and _t<=_type and _fl==' ' and not _fo and not _ob:
                        _distances.append((_x,_y))
            return _distances[random.randint(0,len(_distances)-1)]

        for i in range(foes):
            # Pick a random distance
            _foeDist = random.randint(15,maxDistance)
            # Trying to map the foe type to 1-5 based on the current level the distance and the areatype
            _x,_y = _randomDistanceInType((_foeDist-10,_foeDist),5)
            _type = dataType[_y][_x]
            _rfoes = foesList[_type*len(foesList)//4:]
            _foe = _rfoes[random.randint(0,len(_rfoes)-1)]
            newFoe = Foe(pos=(_x,_y),name=_foe, **FOELIST[_foe])
            dataFoes[_y][_x] = newFoe
            foeList.append(newFoe)
        for i in range(objs):
            # Pick a random distance
            _objDist = random.randint(15,maxDistance)
            # Trying to map the foe type to 1-5 based on the current level the distance and the areatype
            _x,_y = _randomDistanceInType((_objDist-10,_objDist),5)
            _type = dataType[_y][_x]
            _robjs = objList[_type*len(objList)//4:]
            _obj = _robjs[random.randint(0,len(_robjs)-1)]
            dataObjs[_y][_x] = _obj

    def placeBoss(self):
        level = glbls.level
        # find the walkable places
        heroPos = self._tmpData['heroPos']
        dw,dh = self._tmpData['dsize']
        areaMap = self._tmpData['areaMap']
        dataFloor= self._tmpData['dataFloor']
        dataType = self._tmpData['dataType']
        dataObjs  = self._tmpData['dataObjs']
        dataFoes = self._tmpData['dataFoes']
        heatMap  = self._tmpData['heatMap']
        listKeys = self._tmpData['listKeys']
        distancesByType = self._tmpData['distancesByType']

        # mapSize     = sum([sum([1 if ch == ' ' else 0 for ch in row]) for row in dataFloor])
        # maxDistance = max([max([d if d < 0x10000 else 0 for d in row]) for row in heatMap])
        maxType = max([max(row) for row in dataType])
        maxDist = distancesByType[maxType]['max']

        def _randomDistanceInTypes(_dists,_types):
            _fr,_to = _dists
            _ta,_tb = _types
            _distances = []
            for _y,(_rh,_rt,_rfl) in enumerate(zip(heatMap,dataType,dataFloor)):
                for _x,(_d,_t,_fl) in enumerate(zip(_rh,_rt,_rfl)):
                      if _fr<=_d<=_to and _ta<=_t<=_tb and _fl==' ':
                        _distances.append((_x,_y))
            if _distances:
                return _distances[random.randint(0,len(_distances)-1)]
            return None

        while not (snakePos := _randomDistanceInTypes([maxDist-10,maxDist-6],[0,maxType])):
            maxDist -= 1
        sx,sy = snakePos

        def _areaDoors(_x,_y):
            _doors = []
            _area = areaMap[_y][_x]
            _areaTiles = []
            for _y,_row in enumerate(areaMap):
                for _x,_a in enumerate(_row):
                    if _a==_area:
                        _areaTiles.append((_x,_y))
            # _areaTiles = [(__x,__y,__a) for _y,_row in list(enumerate(areaMap)) ]
            for __x,__y in _areaTiles:
                if __y > 0    and dataFloor[__y-1][__x  ]in('D','DR','DG','DB','DY','d',) and (_doorPos:=(__x  ,__y-1)) not in _doors:_doors.append(_doorPos)
                if __y < dh-2 and dataFloor[__y+1][__x  ]in('D','DR','DG','DB','DY','d',) and (_doorPos:=(__x  ,__y+1)) not in _doors:_doors.append(_doorPos)
                if __x > 0    and dataFloor[__y  ][__x-1]in('D','DR','DG','DB','DY','d',) and (_doorPos:=(__x-1,__y  )) not in _doors:_doors.append(_doorPos)
                if __x < dw-2 and dataFloor[__y  ][__x+1]in('D','DR','DG','DB','DY','d',) and (_doorPos:=(__x+1,__y  )) not in _doors:_doors.append(_doorPos)
            return _doors

        # Process all the tiles and mark the connected ones
        def _recurseMark(_pos,_num):
            toBeProcessed = [_pos]
            while toBeProcessed:
                _x,_y = toBeProcessed.pop()
                dataType[_y][_x] = _num
                if _y > 0    and areaMap[_y-1][_x] and dataType[_y-1][_x]!=_num and (_x  ,_y-1) not in toBeProcessed: toBeProcessed.append((_x  ,_y-1))
                if _y < dh-2 and areaMap[_y+1][_x] and dataType[_y+1][_x]!=_num and (_x  ,_y+1) not in toBeProcessed: toBeProcessed.append((_x  ,_y+1))
                if _x > 0    and areaMap[_y][_x-1] and dataType[_y][_x-1]!=_num and (_x-1,_y  ) not in toBeProcessed: toBeProcessed.append((_x-1,_y  ))
                if _x < dw-2 and areaMap[_y][_x+1] and dataType[_y][_x+1]!=_num and (_x+1,_y  ) not in toBeProcessed: toBeProcessed.append((_x+1,_y  ))

        # If we have enough space to place a room, do it:
        def _placeRoom(_x,_y):
            _newRoomTiles = []
            _area = areaMap[_y][_x]
            for __y in     range(max(0,_y-2),min(dh-1,_y+3)):
                for __x in range(max(0,_x-2),min(dw-1,_x+3)):
                    if areaMap[__y][__x] == _area:
                        _newRoomTiles.append((__x,__y))
            if len(_newRoomTiles) > 2:
                # Place Walls
                for _tx,_ty in _newRoomTiles:
                    areaMap[_ty][_tx]=0x10000
                    if abs(_x-_tx)<2 and abs(_y-_ty)<2: continue
                    areaMap[_ty][_tx]=0
                    dataFoes[_y][_x]=''
                    dataObjs[_y][_x]=''
                    if abs(_x-_tx)==2 and abs(_y-_ty)==2: continue
                    if dataFloor[_ty][_tx] == ' ':
                        # if abs(_x-_tx)==2 and abs(_y-_ty)==2:
                        #     dataFloor[_ty][_tx] = '#'
                        # else:
                        dataFloor[_ty][_tx] = 'd'
        _placeRoom(sx,sy)

        cx,cy = closestDoor = (sx,sy)
        for _pos in _areaDoors(sx,sy):
            _x,_y = _pos
            dataFloor[_y][_x] = 'DY'
            if heatMap[cy][cx]>=heatMap[_y][_x]>0:
                cx,cy = closestDoor = (_x,_y)
        _recurseMark((sx,sy),4)
        dataFoes[sy][sx] = 'Snake'

        while not (bossPos := _randomDistanceInTypes([maxDist-10,maxDist-6],[0,maxType])):
            maxDist -= 1
        bx,by = bossPos
        dataFoes[by][bx] = 'Nose'

    def placeExit(self):
        level = glbls.level
        # find the walkable places
        heroPos = self._tmpData['heroPos']
        dw,dh = self._tmpData['dsize']
        areaMap = self._tmpData['areaMap']
        dataFloor= self._tmpData['dataFloor']
        dataType = self._tmpData['dataType']
        dataObjs  = self._tmpData['dataObjs']
        dataFoes = self._tmpData['dataFoes']
        heatMap  = self._tmpData['heatMap']
        listKeys = self._tmpData['listKeys']
        distancesByType = self._tmpData['distancesByType']

        maxType = max([max(row) for row in dataType])
        maxDist = max([distancesByType[dit]['max'] for dit in distancesByType])

        def _randomDistanceInTypes(_dists,_types):
            _fr,_to = _dists
            _ta,_tb = _types
            _distances = []
            for _y,(_rh,_rt,_rfl) in enumerate(zip(heatMap,dataType,dataFloor)):
                for _x,(_d,_t,_fl) in enumerate(zip(_rh,_rt,_rfl)):
                      if _fr<=_d<=_to and _ta<=_t<=_tb and _fl==' ':
                        _distances.append((_x,_y))
            if _distances:
                return _distances[random.randint(0,len(_distances)-1)]
            return None

        ex,ey = exitPos = _randomDistanceInTypes([maxDist//2,maxDist-5],[0,maxType])
        dataFloor[ey][ex] = '>'

    def genDungeon(self):
        self._tmpData = {
            'layer' : {'layers':[], 'pos':[]},
            'dataFoes'  : [],
            'dataObjs'  : [],
            'dataFloor'  : [],
            'dataType' : [],
            'dsize' : (0,0),
            'heroPos': (0,0)
        }

        self.genPlane()
        self.genMainArea()
        self.ensureConnection()
        self.genWalls()
        self.genDoors()
        self.placeKeys()
        self.placeFoesObjs()
        # self.placeObjs()

        if  glbls.level == 5:
            self.placeBoss()
        else:
            self.placeExit()


        self._dataFloor= self._tmpData['dataFloor']
        self._dataType = self._tmpData['dataType']
        self._dataFoes = self._tmpData['dataFoes']
        self._dataObjs = self._tmpData['dataObjs']
        self._dataObjs = self._tmpData['dataObjs']
        self._layerPlane = self._tmpData['layer']
        self._foes = self._tmpData['foes']
        self._size = (len(self._dataFloor[0]),len(self._dataFloor))
        self._heatMap  = [[0]*self._size[0] for _ in range(self._size[1])]

        # for y,row in enumerate(self._tmpData['heatMap']):
        # def _printMap(_map):
        #     for y,row in enumerate(_map):
        #         out = f"{y:02} - "
        #         for v in row:
        #             if v: out += f"{v:2} "
        #             else:out += f" . "
        #         ttk.TTkLog.debug(out)
        # _printMap(self._tmpData['areaMap'])
        # _printMap(self._tmpData['dataType'])
        # _printMap(self._tmpData['heatMap'])


        return self._tmpData['heroPos']



