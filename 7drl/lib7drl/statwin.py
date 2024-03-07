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


__all__ = ['StatWin']

from dataclasses import dataclass
import sys, os, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .player  import *
from .dungeon import *
from .assets  import *
from .glbls import *

class ColorLAF(ttk.TTkLookAndFeelFPBar):
    def __init__(self, color, showText=True, textWidth=4):
        self._claf = color
        super().__init__(showText, textWidth)

    def color(self, value,max,min):
        # red, green = round(value*255), round((1-value)*255)
        # fg = f"#{red:02x}{green:02x}00"
        # return ttk.TTkColor.fg(fg) + self._claf
        return self._claf



class StatWin(ttk.TTkWindow):
    def __init__(self, player:Player, **kwargs):
        # super().__init__(**(kwargs|{'layout':ttk.TTkGridLayout()}))
        super().__init__(**kwargs)

        self.setTitle("Player 😎 stuff 📈")

        self._pbHealth = ttk.TTkFancyProgressBar(
            parent=self,pos=(13,3),size=(15,1),
            lookAndFeel=ColorLAF(showText=False, color=ttk.TTkColor.fg('#FF0000')+ttk.TTkColor.bg('#330000',modifier=ttk.TTkColorGradient(orientation=ttk.TTkK.HORIZONTAL, fgincrement=100, bgincrement=100))))
        self._pbArmor  = ttk.TTkFancyProgressBar(
            parent=self,pos=(13,4),size=(15,1),
            lookAndFeel=ColorLAF(showText=False, color=ttk.TTkColor.fg('#0000FF')+ttk.TTkColor.bg('#000033',modifier=ttk.TTkColorGradient(orientation=ttk.TTkK.HORIZONTAL, fgincrement=100, bgincrement=100))))

        self._player = player
        self._player.updated.connect(self._update)

    def mouseReleaseEvent(self, evt) -> bool:
        glbls.root.setFocus()
        return super().mouseReleaseEvent(evt)

    def _update(self):
        self._pbHealth.setValue(self._player.health/100)
        self._pbArmor.setValue( self._player.armor/100)
        self.update()

    def paintEvent(self, canvas:ttk.TTkCanvas):
        p  = self._player
        pb = self._player.body
        sy = 6
        sx = 1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"HEALTH: {p.health}")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"ARMOR:  {p.armor}")); sy+=1
        sy+1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Head:  {Tiles[pb.head]}"))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"Body:  {Tiles[pb.body]}")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Legs:  {Tiles[pb.legs]}"))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"Feet:  {Tiles[pb.feet]}")); sy+=1
        sy+1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Hold:  {Tiles[p.weaponHeld]} - Melee:")); sy+=1

        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Weapons:")); sy+=1
        cEn   = ttk.TTkColor.RST
        cHold = ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#333300")
        cDis  = ttk.TTkColor.fg("#AAAAAA")
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr1']} Intimate Bow | {Tiles['ws1']}:{p.shells['ws1']: 3}",cDis if 'wr1' not in p.weapons else cHold if p.weaponHeld=='wr1' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr2']} Feeling Gun  | {Tiles['ws2']}:{p.shells['ws2']: 3}",cDis if 'wr2' not in p.weapons else cHold if p.weaponHeld=='wr2' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr3']} LoveZooka    | {Tiles['ws3']}:{p.shells['ws3']: 3}",cDis if 'wr3' not in p.weapons else cHold if p.weaponHeld=='wr3' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr4']} Friend Zoner | {Tiles['ws4']}:{p.shells['ws4']: 3}",cDis if 'wr4' not in p.weapons else cHold if p.weaponHeld=='wr4' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Throwables:")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wt1']}: {p.throwables['wt1']: 2} ",cHold if p.weaponHeld=='wt1' else cEn))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"{Tiles['wt2']}: {p.throwables['wt2']: 2} ",cHold if p.weaponHeld=='wt2' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wt3']}: {p.throwables['wt3']: 2} ",cHold if p.weaponHeld=='wt3' else cEn))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"{Tiles['wt4']}: {p.throwables['wt4']: 2} ",cHold if p.weaponHeld=='wt4' else cEn)); sy+=1

        return super().paintEvent(canvas)