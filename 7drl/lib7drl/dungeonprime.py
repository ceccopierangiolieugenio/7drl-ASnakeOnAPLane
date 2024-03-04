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

TEST = [
    # ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',],
    # ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',],
    # ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',],
    # ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X',],
    ['X','X','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#' ,'#','#' ,'X','X','X','#','#','#','X' ,'X' ,'X','#','#','#','#','#','X','X',],
    ['X','#',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ' ,' ','#' ,'X','X','#',' ',' ',' ','#' ,'X' ,'#',' ',' ',' ',' ',' ','#','X',],
    ['#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','KG',' ','#' ,'#','#',' ',' ',' ',' ',' ' ,'#' ,' ',' ',' ',' ',' ',' ',' ','#',],
    ['#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ' ,' ','#' ,' ',' ',' ',' ',' ',' ',' ' ,'DB',' ',' ',' ',' ',' ','b',' ','#',],
    ['#',' ',' ',' ',' ',' ',' ','D',' ',' ',' ','z',' ',' ',' ',' ',' ',' ',' ','>',' ',' ',' ',' ',' ' ,' ','#' ,' ',' ',' ',' ',' ','#','#' ,'#' ,' ',' ',' ',' ',' ',' ',' ','#',],
    ['#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ' ,' ','DG',' ',' ',' ',' ','#','z','KB','#' ,' ',' ',' ',' ',' ',' ',' ','#',],
    ['X','#',' ',' ',' ',' ','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ' ,' ','#' ,' ',' ',' ',' ','D','z','#' ,'X' ,'#',' ',' ',' ',' ',' ','#','X',],
    ['X','X','#','#','#','#','X','X','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#' ,'#','#' ,'#','#','#','#','#','#','X' ,'X' ,'X','#','#','#','#','#','X','X',],
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
        self._layerPlane = {'layers':[plb,plf]    ,'pos':[(-18,-7),(wplb-27,-1)]}

        self._data = TEST
        self._dataType = [[0 if ch ==' ' else 0 for ch in row] for row in self._data]
        self._tmpData = {}


    def genPlane(self):

        plf  = self._plf
        plb  = self._plb
        plb1 = self._plb1
        wplf,hplf   = plf.size()
        wplb,hplb   = plb.size()
        wplb1,hplb1 = plb1.size()

        # Phase 1 - Define the walkable Area
        #       1.1 - place n plane things on a tictactoe checkboard:
        cb = [
            [False, False, False],
            [False, False, False],
            [False, False, False]]
        cb[random.randint(0,2)][0] = True
        cb[random.randint(0,2)][1] = True
        cb[random.randint(0,2)][2] = True

        # Add a random Front/Back
        if random.randint(0,1):
            # Add random Front
            cb[random.randint(0,2)][2] = True
        if random.randint(0,1):
            # Add random Back
            cb[random.randint(0,2)][0] = True
        if random.randint(0,1):
            # Add random Center
            cb[random.randint(0,2)][1] = True

        # Add missing pieces to allow a full traverse
        if ((cb[0][0] and cb[2][2]) or
            (cb[2][0] and cb[0][2]) or
            (cb[0][1] and cb[2][0]) or
            (cb[0][1] and cb[2][2]) or
            (cb[2][1] and cb[0][2]) or
            (cb[2][1] and cb[0][2]) ):
            cb[1][1]=True


        # force the required central pieces
        newLayer = self._tmpData['layer']
        for y,row in enumerate(cb):
            y-=1
            if row[0]:
                px = random.randint(0,40)
                py = random.randint(0,5)+y*(hplf-5)
                newLayer['layers'].append(plb)
                newLayer['pos'].append((px,py))
            if row[2]:
                px = random.randint(0,40)+wplb+wplb1-50
                py = random.randint(0,7)+y*(hplf-5)
                newLayer['layers'].append(plf)
                newLayer['pos'].append((px,py))
            if row[1]:
                px = random.randint(0,40)+wplb-30
                py = random.randint(0,5)+y*(hplb1-8)-2
                newLayer['layers'].append(plb1)
                newLayer['pos'].append((px,py))

        # newLayer['layers'].append(plb)
        # newLayer['pos'].append((-20,-20))

        # newLayer['layers'].append(plf)
        # newLayer['pos'].append((100,-20))


        minx=0x1000
        miny=0x1000
        maxx=-0x1000
        maxy=-0x1000
        # Normalize
        for l,pos in zip(newLayer['layers'],newLayer['pos']):
            w,h=l.size()
            minx = min(minx,pos[0])
            miny = min(miny,pos[1])
            maxx = max(maxx,pos[0]+w)
            maxy = max(maxy,pos[1]+h)
        newLayer['pos'] = [(x-minx,y-miny) for (x,y) in newLayer['pos']]
        self._tmpData['dsize'] = ((maxx-minx)//2, maxy-miny)

    def genMainArea(self):
        # find the walkable places
        newLayer = self._tmpData['layer']
        dw,dh = self._tmpData['dsize']
        data0 = [['X']*(dw) for _ in range(dh)]
        for l,pos in zip(newLayer['layers'],newLayer['pos']):
            lw,lh=l.size()
            x,y=pos
            for ly in range(lh):
                for lx in range(((lw-1)//2)*2):
                    cl1 = l.getColor(lx,ly)
                    cl2 = l.getColor(lx+1,ly)
                    if cl1[1] and cl2[1]:
                        data0[ly+y][(lx+x)//2]=' '


        data1 = self._tmpData['data'] = [[' ']*(dw) for _ in range(dh)]
        # reduce the area by 1
        for y,row in enumerate(data0):
            for x,ch in enumerate(row):
                if x==0 or x==dw-1 or y==0 or y==dh-1:
                    data1[y][x] = 'X'
                if ch == 'X':
                    data1[max(   0,y-1)][max(   0,x-1)] = 'X'
                    data1[max(   0,y-1)][max(   0,x  )] = 'X'
                    data1[max(   0,y-1)][min(dw-1,x+1)] = 'X'
                    data1[max(   0,y  )][max(   0,x-1)] = 'X'
                    data1[max(   0,y  )][max(   0,x  )] = 'X'
                    data1[max(   0,y  )][min(dw-1,x+1)] = 'X'
                    data1[min(dh-1,y+1)][max(   0,x-1)] = 'X'
                    data1[min(dh-1,y+1)][max(   0,x  )] = 'X'
                    data1[min(dh-1,y+1)][min(dw-1,x+1)] = 'X'

        # add wall
        for y,row in enumerate(data1):
            for x,ch in enumerate(row):
                if ch == ' ':
                    if (
                       data1[max(   0,y-1)][max(   0,x-1)] == 'X' or
                       data1[max(   0,y-1)][max(   0,x  )] == 'X' or
                       data1[max(   0,y-1)][min(dw-1,x+1)] == 'X' or
                       data1[max(   0,y  )][max(   0,x-1)] == 'X' or
                       data1[max(   0,y  )][max(   0,x  )] == 'X' or
                       data1[max(   0,y  )][min(dw-1,x+1)] == 'X' or
                       data1[min(dh-1,y+1)][max(   0,x-1)] == 'X' or
                       data1[min(dh-1,y+1)][max(   0,x  )] == 'X' or
                       data1[min(dh-1,y+1)][min(dw-1,x+1)] == 'X' ):
                        data1[y][x] = '#'


    def ensureConnection(self):
        # find the walkable places
        dw,dh = self._tmpData['dsize']
        data    = self._tmpData['data']
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
        def _recurseMark(_pos,_num):
            _x,_y = _pos
            if  not  dataMap[_y][_x]: return
            if _num==dataMap[_y][_x]: return
            dataMap[_y][_x] = _num
            if _y > 0   : _recurseMark((_x,_y-1),_num)
            if _y < dh-2: _recurseMark((_x,_y+1),_num)
            if _x > 0   : _recurseMark((_x-1,_y),_num)
            if _x < dw-2: _recurseMark((_x+1,_y),_num)

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



    def genWalls(self):
        # find the walkable places
        dw,dh = self._tmpData['dsize']
        data    = self._tmpData['data']
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

    def genDoors(self):
        # find the walkable places
        dw,dh = self._tmpData['dsize']
        data    = self._tmpData['data']
        dataType = self._tmpData['dataType'] = [[5 if ch ==' ' else 0 for ch in row] for row in data]

        # Create a map with
        # 1 for walkable tiles,
        # 0 for not walkable tiles
        # I will use it to check if thre are not reachable areas
        dataMap     = [[1 if ch ==' ' else 0 for ch in row] for row in data]
        # dataMapType = [[1 if ch ==' ' else 0 for ch in row] for row in data]

        # Divide the dungeons in walkable areas

        # find the first walcable tile with _num
        def _getFirst(_num):
            for y,row in enumerate(dataMap):
                for x,ch in enumerate(row):
                    if ch == _num:
                        return (x,y)
            return None

        # Process all the tiles and mark the connected ones
        def _recurseMark(_data,_pos,_num):
            _x,_y = _pos
            if  not  _data[_y][_x]: return
            if _num==_data[_y][_x]: return
            _data[_y][_x] = _num
            # data[_y][_x] = 'D'
            if _y > 0   : _recurseMark(_data,(_x,_y-1),_num)
            if _y < dh-2: _recurseMark(_data,(_x,_y+1),_num)
            if _x > 0   : _recurseMark(_data,(_x-1,_y),_num)
            if _x < dw-2: _recurseMark(_data,(_x+1,_y),_num)

        # Assign an Area Id for all the connected tiles
        markId = 1
        while fpos := _getFirst(1):
            markId+=1
            _recurseMark(dataMap,fpos,markId)

        def _getWalls(_area):
            _walls = {}
            def __checkWall(__x,__y,_walls=_walls):
                if data[__y][__x] == '#' and (__x,__y) not in _walls:
                    # List the areas connected to this wall
                    _conn = set()
                    if __x>0    and (__a:=dataMap[__y][__x-1]): _conn.add(__a)
                    if __x<dw-1 and (__a:=dataMap[__y][__x+1]): _conn.add(__a)
                    if __y>0    and (__a:=dataMap[__y-1][__x]): _conn.add(__a)
                    if __y<dh-1 and (__a:=dataMap[__y+1][__x]): _conn.add(__a)
                    if _area in _conn and len(_conn)==2:
                        _walls[(__x,__y)]=list(_conn)
            for _y,_row in enumerate(dataMap[1:dh-1],1):
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

        # # parse the tree and find the longest branch
        # # use the longest path to decide which
        # # card protected areas need to be defined
        # def _parseTree(_tree):
        #     _longest = []
        #     for _c in _tree['connections']:
        #         _cc = _parseTree(_c)
        #         if len(_cc) > len(_longest):
        #             _longest = _cc
        #     return [_tree] + _longest
        # longPath = _parseTree(fullTree)
        # if _rr:=random.randint(0,max(3,len(longPath)//2)):

        # # Extract all the trees of any single area type
        # def _extractTypeTree(_tree):
        #     _type  = _tree['type']
        #     _area  = _tree['area']
        #     _walls = _tree['walls']
        #     _self  = {'area':_area, 'connections':[], 'walls':_walls, 'type':_type}
        #     _other = []
        #     for _c in _tree['connections']:
        #         _cca = _extractTypeTree(_c)
        #         if _cca and _cca[0]['type'] == _type:
        #             _self['connections'].append(_cca[0])
        #             _other += _cca[1:]
        #         else:
        #             _other += _cca
        #     return [_self] + _other
        # areasTrees = _extractTypeTree(fullTree)

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
                        data[__y][__x] = ['D','DG','DB','DR'][max(_type1,_type2)]
                    else:
                        data[__y][__x] = 'D'
                __addDoor(_wlls[random.randint(0,len(_wlls)-1)])
                # Add extra door randomly
                if not random.randint(0,2):
                    __addDoor(_wllsAll[random.randint(0,len(_wllsAll)-1)])
                _placeDoors(_c)

        # for _c in areasTrees:
        #     _placeDoors(_c)
        _placeDoors(fullTree)


        # connect all different area types with locked doors

        for y,row in enumerate(dataMap):
            out = f"{y:02} - "
            for v in row:
                if v: out += f"{v:2} "
                else:out += f"   "
            # ttk.TTkLog.debug(out)

        def _findRandomInArea(_num):
            _ll = []
            for _y,_row in enumerate(dataMap):
                for _x,_ch in enumerate(_row):
                    if _ch == _num:
                        _ll.append((_x,_y))
            return _ll[random.randint(0,len(_ll)-1)]
        return _findRandomInArea(_startingArea)



    def genDungeon(self):
        self._tmpData = {
            'layer' : {'layers':[], 'pos':[]},
            'data'  : [],
            'dataType' : [],
            'dsize' : (0,0)
        }

        self.genPlane()
        self.genMainArea()
        self.ensureConnection()
        self.genWalls()
        x,y = self.genDoors()

        self._data = self._tmpData['data']
        self._dataType = self._tmpData['dataType']
        self._layerPlane = self._tmpData['layer']

        return (x,y)



