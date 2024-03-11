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
from .glbls  import *
from .player import *
from .objinfo  import *
from .messages import *

class Dungeon(DungeonPrime):
    UP    = 0x01
    DOWN  = 0x02
    LEFT  = 0x03
    RIGHT = 0x04

    def __init__(self) -> None:
        super().__init__()
        self._mouseColor        = ttk.TTkColor.fg('#88BB88')+ttk.TTkColor.bg('#BBBB88')
        self._mouseColorVisible = ttk.TTkColor.fg('#00FF00')+ttk.TTkColor.bg('#FFFF88')
        # self._mouseIcon = ttk.TTkString("🔆",self._mouseColor)
        self._mouseIcon = ttk.TTkString("🔆")
        self._floorOld = [
                [[ttk.TTkColor.bg('#eeddee'),ttk.TTkColor.bg('#ccccee')],
                 [ttk.TTkColor.bg('#eeeeee'),ttk.TTkColor.bg('#cccccc')]], # Base
                [[ttk.TTkColor.bg('#ddffdd'),ttk.TTkColor.bg('#aaddaa')],
                 [ttk.TTkColor.bg('#eeeeee'),ttk.TTkColor.bg('#dddddd')]], # Green
                [[ttk.TTkColor.bg('#ddddff'),ttk.TTkColor.bg('#aaaadd')],
                 [ttk.TTkColor.bg('#cccccc'),ttk.TTkColor.bg('#bbbbbb')]], # Blue
                [[ttk.TTkColor.bg('#ffdddd'),ttk.TTkColor.bg('#ddaaaa')],
                 [ttk.TTkColor.bg('#dddddd'),ttk.TTkColor.bg('#cccccc')]], # Red
                [[ttk.TTkColor.bg('#ffffdd'),ttk.TTkColor.bg('#ddddaa')],
                 [ttk.TTkColor.bg('#ffffdd'),ttk.TTkColor.bg('#ddddaa')]], # Yellow
                [[ttk.TTkColor.bg('#DAA06D'),ttk.TTkColor.bg('#B87333')],
                 [ttk.TTkColor.bg('#D2B48C'),ttk.TTkColor.bg('#C19A6B')]], # Crap
            ]
        def _genTile(r,g,b):
            r1,g1,b1    = int(r*0.9),int(g*0.9),int(b*0.9)
            r2,g2,b2    = int(r*0.8),int(g*0.8),int(b*0.8)
            r3,g3,b3    = int(r*0.7),int(g*0.7),int(b*0.7)
            # rg=gg=bg    = (r+g+b)//3
            # rg1=gg1=bg1 = (r1+g1+b1)//3
            # rg1,gg1,bg1 = r1,g1,b1
            return [
                [ttk.TTkColor.bg(f"#{r :02x}{g :02x}{b :02x}"),
                 ttk.TTkColor.bg(f"#{r1:02x}{g1:02x}{b1:02x}")],
                [ttk.TTkColor.bg(f"#{r2:02x}{g2:02x}{b2:02x}"),
                 ttk.TTkColor.bg(f"#{r3:02x}{g3:02x}{b3:02x}")]]
        self._floor = [
            _genTile(0xee,0xdd,0xee), # 0 Base
            _genTile(0xdd,0xff,0xdd), # 1 Green
            _genTile(0xdd,0xdd,0xff), # 2 Blue
            _genTile(0xff,0xdd,0xdd), # 3 Red
            _genTile(0xff,0xff,0xee), # 4 Yellow
            _genTile(0xd2,0xb4,0x8c), # 5 Crap
            _genTile(0xaa,0xff,0xaa), # 6 Exit
            ]

        self._makeRayMap()
        dw,dh = self.size()
        self._rayNum = 1
        self._visibilityMap = [[0]*(dw) for _ in range(dh)]
        self.updateVisibility()

    def initDungeonZero(self):
        self._oneOff = []
        self._animShells = []
        self._ongoingAnimation = False
        self._mousePos  = (5,3)
        self._heroPos   = (5,3)
        self._heroBouncing = (0,0)
        self._mouseLine        = []
        self._mouseVisibleLine = []
        super().initDungeonZero()

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
        self._mouseLine = []
        self._mouseVisibleLine = []
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

    # Return a line, visibleLine, hitPoint, visible bool
    def getRays(self, fr, to) -> list[list,list,bool]:
        hx,hy = fr
        x,y   = to
        dw,dh = self.size()
        dataMap = self._dataFloor
        rim = self._ratInvMap
        dx,dy=x-hx,y-hy
        line = []
        if (dx,dy) in reversed(rim):
            line = [(hx+_x,hy+_y) for _x,_y in rim[(dx,dy)]]
        if 0<=x<dw and 0<=y<dh:
            line += [to]

        # ttk.TTkLog.debug(f"{fr=} {to=}")
        # ttk.TTkLog.debug(line)
        visibleLine = []
        hitPos = (hx,hy)
        for a,b in zip(line,line[1:]+[(x,y)]):
            dx,dy=a
            bx,by=b
            visibleLine.append(a)
            if dataMap[dy][dx] not in (' ','d','>'):
                hitPos=(dx,dy)
                break
            _T = dataMap[dy+1][dx  ] not in (' ','d','>')
            _B = dataMap[dy-1][dx  ] not in (' ','d','>')
            _L = dataMap[dy  ][dx-1] not in (' ','d','>')
            _R = dataMap[dy  ][dx+1] not in (' ','d','>')
            if bx>dx and by>dy and _T and _R : hitPos=(dx,dy); break
            if bx>dx and by<dy and _B and _R : hitPos=(dx,dy); break
            if bx<dx and by>dy and _T and _L : hitPos=(dx,dy); break
            if bx<dx and by<dy and _B and _L : hitPos=(dx,dy); break
        if len(line)==len(visibleLine): hitPos=to
        return line, visibleLine, hitPos, len(line)==len(visibleLine)

    def animShot(self,fr,to,path,glyph,endingCallback):
        shell = {'pos':fr,'to':to,'glyph':glyph,'path':path,'id':0}
        def _shotAnimation(value:int):
            self._ongoingAnimation = True
            shell['pos'] = shell['path'][value]
        def _finishedAnimation():
            self._ongoingAnimation = False
            self._animShells.remove(shell)
            shell['glyph']=Tiles['HIT']
            shell['pos']=shell['to']
            self._oneOff.append(shell)
            endingCallback()

        # Entering the Parallax
        animShell = ttk.TTkPropertyAnimation(None, _shotAnimation)
        animShell.setStartValue(0)
        animShell.setEndValue(  len(path)-1)
        dur = ((fr[0]-to[0])**2+(fr[1]-to[1])**2)/400 # 20 tiles per second
        animShell.setDuration(dur)
        animShell.finished.connect(_finishedAnimation)
        # animShell.setEasingCurve(ttk.TTkEasingCurve.OutQuint)
        animShell.start()
        self._animShells.append(shell)

    def moveMouse(self, x,y):
        if self._ongoingAnimation: return
        line, visible, _,__ = self.getRays(self._heroPos,(x,y))
        self._mousePos = (x,y)
        self._mouseLine = []
        self._mouseVisibleLine = []
        dataFloor = self._dataFloor
        dataFoes  = self._dataFoes
        dataObjs  = self._dataObjs
        visMap    = self._visibilityMap
        dw,dh=self.size()
        if 0<=x<dw and 0<=y<dh:
            if ((visMap[y][x] and dataFoes[y][x]) or
                ((obj:=dataObjs[y][x])  and obj in ObjInfo)):
                self._mouseLine = line
                self._mouseVisibleLine = visible

    def hitFoe(self, foe:Foe, amount, suicide=False):
        dfoes = self._dataFoes
        dobjs = self._dataObjs
        dataMap = self._dataFloor
        foes  = self._foes
        foe.health -= amount
        if foe not in foes: return
        x,y = foe.pos
        if foe.health <= 0: # the foe is dead
            if type(foe) == Snake:
                glbls.death.emit()
            foes.remove(foe)
            for drop in foe.drop():
                allPos = [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                random.shuffle(allPos)
                for dpx,dpy in allPos:
                    if dataMap[dpy][dpx] not in (' ','d'):continue
                    if not dobjs[dpy][dpx] or drop in ['KR','KG','KB','KY']:
                        dobjs[dpy][dpx] = drop
                        break

            dfoes[y][x] = None
            if suicide:
                Message.add(
                    ttk.TTkString(f"{foe.fullName} {foe.picture}",ttk.TTkColor.fg("FFFF00")) +
                    ttk.TTkString(f" Died in a pool of crap"))
                Message.add(
                    ttk.TTkString(f" Surely it's your fault"))
            else:
                Message.add(
                    ttk.TTkString(f"You Killed ") +
                    ttk.TTkString(f"{foe.fullName} {foe.picture}",ttk.TTkColor.fg("FFFF00")))
        else:
            Message.add(ttk.TTkString(f"You Hit ") +
                    ttk.TTkString(f"{foe.fullName} {foe.picture}",ttk.TTkColor.fg("FFFF00")))

    def _poolOfCrap(self, pos, size):
        dw,dh=self.size()
        _x,_y = pos
        _dt = self._dataType
        _df = self._dataFloor
        def _crapStep(_pos,_step):
            _cx,_cy = _pos
            if not (0<=_cx<dw and 0<=_cy<dh):return
            _dt[_cy][_cx] = 5
            if _df[_cy][_cx] not in (' ','d','>'): return
            if _step<0: return
            _crapStep((_cx+1,_cy  ),_step-1)
            _crapStep((_cx-1,_cy  ),_step-1)
            _crapStep((_cx  ,_cy+1),_step-1)
            _crapStep((_cx  ,_cy-1),_step-1)
        _crapStep((_x,_y),size)

    def _areaShot(self, pos, size):
        hx,hy = self._heroPos
        dw,dh=self.size()
        _x,_y = pos
        _dt = self._dataType
        _df = self._dataFloor
        dfoes = self._dataFoes
        player:Player = glbls.player
        _shotTiles = []
        def _crapStep(_pos,_step):
            _cx,_cy = _pos
            if not (0<=_cx<dw and 0<=_cy<dh):return
            _shotTiles.append((_cx,_cy))
            if _df[_cy][_cx] not in (' ','d','>'): return
            if _step<0: return
            _crapStep((_cx+1,_cy  ),_step-1)
            _crapStep((_cx-1,_cy  ),_step-1)
            _crapStep((_cx  ,_cy+1),_step-1)
            _crapStep((_cx  ,_cy-1),_step-1)
        _crapStep((_x,_y),size)
        for p in _shotTiles:
            nx,ny = p
            shell = {'pos':p,'glyph':Tiles['HIT']}
            self._oneOff.append(shell)
            if foe:=dfoes[ny][nx]:
                if type(foe) == Snake:
                    glbls.endGame.emit()
                else:
                    self.hitFoe(foe,player.wpn,False)
            if p == self._heroPos:
                player.hit(player.wpn, [f"You burned your ARSE to death!!!","DumbASS"])



    def shotWeapon(self,x,y):
        self._mouseLine = []
        self._mouseVisibleLine = []
        self._mousePos = None
        dw,dh=self.size()
        if not (0<=x<dw and 0<=y<dh): return
        line, visible, hitPos, hit = self.getRays(self._heroPos,(x,y))
        hx,hy = hitPos
        df = self._dataFoes
        dfoes = self._dataFoes
        player:Player = glbls.player
        foes  = self._foes
        self._mouseLine = []
        if self._ongoingAnimation: return
        if hit and (foe:=df[y][x]):
            # Process Melee Action
            if not player.shot():
                Message.add(ttk.TTkString(" - You have no ammo - ",ttk.TTkColor.bg('#0000AA')+ttk.TTkColor.fg('#FFFF00')))
                return
            def _endingCallback():
                if player.weaponHeld == 'wt4': # Add a pool of crap
                    self._poolOfCrap((x,y),2)
                if player.weaponHeld == 'wr4':
                    self._areaShot((x,y),2)
                if player.weaponHeld == 'wt2':
                    self._areaShot((x,y),1)
                if player.weaponHeld == 'wt3':
                    self._areaShot((x,y),2)
                # if player.weaponHeld == 'wt4': # Add a pool of crap
                #     self._poolOfCrap((x,y),2)
                self.hitFoe(foe,player.wpn,False)
                self.foesAction()
            self.animShot(self._heroPos,hitPos,visible,player.shellGlyph(),_endingCallback)


    def foesAction(self):
        visMap = self._visibilityMap
        rn     = self._rayNum
        dm = self._dataFloor
        df = self._dataFoes
        hm = self._heatMap
        dt = self._dataType
        player:Player = glbls.player
        hx,hy = self._heroPos
        if self._ongoingAnimation: return
        # Check hazards:
        if dt[hy][hx] == 5: # Player is on shit
            player.hit(3,["Died sinking in a pool of crap"])
        for foe in self._foes:
            # ttk.TTkLog.debug(foe.name)
            x,y = foe.pos
            if dt[hy][hx] == 5 and foe.name != 'Crap': # Foe is on a sea of crap
                self.hitFoe(foe,3,True)
            if rn==visMap[y][x]: foe.active = True
            if abs(x-hx)>40 or abs(y-hy)>15: foe.active = False
            if not foe.active: continue
            move,shot = foe.getActions()

            def _moveAction():
                ch = hm[y][x]
                if ch == 2: # Melee Attack
                    player.hit(foe.atk, [f"{foe.fullName} the {foe.name}{foe.picture} killed you, LOSER!!!"])
                    return
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

            def _shotAction(_foe=foe):
                # ttk.TTkLog.debug(f"shot {foe.name}")
                if not _foe.wpn: return
                line, visible, hitPos, hit = self.getRays((x,y),self._heroPos)
                if hit:
                    def _endingCallback(_foe=_foe):
                        player.hit(_foe.wpn, [f"{foe.fullName} the {foe.name}{foe.picture} killed you, LOSER!!!"])
                        # ttk.TTkLog.debug(f"shot cb {_foe.name}")
                        if _foe.name == 'Crap': # Add a pool of crap
                            self._poolOfCrap(self._heroPos,1)
                        if _foe.name == 'Skeleton':
                            for gx in range(hx-1,hx+2):
                                for gy in range(hy-1,hy+2):
                                    if not df[gy][gx] and dm[gy][gx]==' ':
                                        newFoe = Foe(pos=(gx,gy),name='Ghost', **FOELIST['Ghost'])
                                        df[gy][gx] = newFoe
                                        self._foes.append(newFoe)
                                        return

                    self.animShot((x,y),self._heroPos,visible,foe.shellGlyph(),_endingCallback)
            if shot:
                _shotAction()
            elif move:
                _moveAction()

    def heroAction(self):
        dataFloor = self._dataFloor
        dataType  = self._dataType
        dataObjs  = self._dataObjs
        hx,hy = self._heroPos
        player:Player = glbls.player
        if obj:=dataObjs[hy][hx]:
            if player.grab(obj):
                dataObjs[hy][hx] = ''
        elif dataFloor[hy][hx] == '>':
            glbls.nextLevel.emit()

    def moveHero(self, direction):
        self._mouseLine = []
        self._mouseVisibleLine = []
        self._mousePos = None
        if self._ongoingAnimation: return
        dtile = self._dataFloor
        dfoes = self._dataFoes
        dobjs = self._dataObjs
        foes  = self._foes
        hx,hy = nx,ny = self._heroPos
        player:Player = glbls.player
        if   direction == self.UP:    ny -= 1
        elif direction == self.DOWN:  ny += 1
        elif direction == self.LEFT:  nx -= 1
        elif direction == self.RIGHT: nx += 1

        if foe:=dfoes[ny][nx]:
            if type(foe) == Snake:
                glbls.endGame.emit()
            else:
                self.hitFoe(foe,player.atk,False)
            return

        # Check if the floor is empty
        if tile:=dtile[ny][nx] in (' ','d','>'):
            self._heroPos = (nx,ny)
            if (obj:=dobjs[ny][nx]) in ['g1','g2','g3','g4','g5','g6','g7','g8']:
                if player.grab(obj):
                    dobjs[ny][nx] = ''
            self.updateVisibility()
            return

        keysMap = {'DR':'KR','DG':'KG','DB':'KB','DY':'KY'}

        if (tile:=dtile[ny][nx]) in ['D','DR','DG','DB','DY']:
            if (reqKey := keysMap.get(tile)) and reqKey not in player.keys:
                Message.add(ttk.TTkString(f"You need {Tiles[reqKey]}"))
                Message.add(ttk.TTkString(f"to open this door"))
                return
            dtile[ny][nx] = 'd'
            self._heroPos = (nx,ny)
            self.updateVisibility()
            return

        # check if I am hitting a wall
        if tile:=dtile[ny][nx] == '#':
            # Ouch!!!
            return


    def setFading(self, fading):
        self._fading = fading

    def setExplosionPos(self, x,y):
        self._expPos = (int(x),int(y))

    def setBouncingHero(self, x,y):
        self._heroBouncing = (int(x),int(y))

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
        self._drawLayer(self._layerExplosion, self._expPos, canvas)

        # Draw the Dungeon:
        fd = self._fading
        dw = len(dataFloor[0])
        dh = len(dataFloor)
        if fd == 1:
            ssh = slice(0,dh+1)
            ssw = slice(0,dw+1)
            fdx,fdy=0,0
        else:
            _fw,_fh = fd*25,fd*15
            ssw = slice(fdx:=max(0,int(hx-_fw)),int(hx+_fw))
            ssh = slice(fdy:=max(0,int(hy-_fh)),int(hy+_fh))

        for cy,(rof,rot,rofoe,roobj,rvm) in enumerate(zip(dataFloor[ssh],dataType[ssh],dataFoes[ssh],dataObjs[ssh],visMap[ssh]),y+fdy):
            for cx,(fl,ty,fo,ob,vm) in enumerate(zip(rof[ssw],rot[ssw],rofoe[ssw],roobj[ssw],rvm[ssw]),fdx):
                if not fl: continue
                if not glbls.showMap and not vm: continue
                if (glbls.showMap or rn==vm) and fo:
                         ch = Tiles.get(fo.name)
                elif ob: ch = Tiles.get(ob)
                else:    ch = Tiles.get(fl)
                color = self._floor[dataType[cy-y][cx]][0 if vm==rn else 1][(cx+cy+hy+1)%2]
                if (cx,cy-y) in self._mouseVisibleLine:
                    color = self._mouseColorVisible
                elif (cx,cy-y) in self._mouseLine:
                    color = self._mouseColor
                else:
                    color = self._floor[dataType[cy-y][cx]][0 if vm==rn else 1][(cx+cy+hy+1)%2]
                if ch:
                    canvas.drawTTkString(pos=(x+cx*2,cy),text=ch,color=color)
                # else:
                #     canvas.drawText(pos=(x+cx*2,cy),text="XX",color=color)

        # Place Hero:
        he = Tiles.get('@')
        hbx,hby = self._heroBouncing
        nhx,nhy=hbx+hx,hby+hy
        if 0<=nhx<dw and 0<=nhy<dh:
            color = self._floor[dataType[nhy][nhx]][0][(hx+hy)%2]
        else:
            color =ttk.TTkColor.RST
        canvas.drawTTkString(pos=(x+nhx*2,y+nhy),text=he,color=color)

        for sh in self._animShells+self._oneOff:
            shx,shy = sh['pos']
            canvas.drawTTkString(pos=(x+shx*2,y+shy),text=sh['glyph'],color=color)
        self._oneOff = []

        if self._mousePos:
            mpx,mpy = self._mousePos
            if 0<=mpx<dw and 0<=mpy<dh and visMap[mpy][mpx]:
                # canvas.drawTTkString(pos=(x+mpx*2,y+mpy),text=self._mouseIcon,color=color)

                def _drawInfo(info,y=y,x=x):
                    iw,ih = max(l.termWidth() for l in info), len(info)
                    if (y+mpy)>(h-ih-10) and (x+mpx*2)>=(w-iw-8):
                        px,py = (w-iw-4,1)
                    else:
                        px,py = (w-iw-4,h-ih-3)
                    canvas.fill(pos=(px,py),size=(iw+2,ih+2))
                    canvas.drawText(pos=(px,py    ),text="🭟"+"▀"*(iw)+"🭔")
                    canvas.drawText(pos=(px,py+ih+1),text="🭎"+"▄"*(iw)+"🭃")
                    for y,l in enumerate(info,py+1):
                        canvas.drawText(pos=(px     ,y),text="▌")
                        canvas.drawText(pos=(px+iw+1,y),text="▐")
                        canvas.drawTTkString(pos=(px+1,y),text=l)

                # Draw Info Box
                if foe := dataFoes[mpy][mpx]:
                    _drawInfo(foe.info)
                elif (obj:=dataObjs[mpy][mpx]) and obj in ObjInfo:
                    _drawInfo(ObjInfo[obj])
                elif (obj:=dataFloor[mpy][mpx]) and obj in ObjInfo:
                    _drawInfo(ObjInfo[obj])


        # for cx,cy in self._mouseLine:
        #     canvas.drawText(pos=(x+cx*2,y+cy),text='XX')



