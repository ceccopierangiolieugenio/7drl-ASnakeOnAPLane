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
sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

from .player  import *
from .dungeon import *
from .assets  import *
from .glbls   import *
from wblib    import WBWindow, bgBLUE, bgBLACK

class ColorLAF(ttk.TTkLookAndFeelFPBar):
    def __init__(self, color, showText=True, textWidth=4):
        self._claf = color
        super().__init__(showText, textWidth)

    def color(self, value,max,min):
        # red, green = round(value*255), round((1-value)*255)
        # fg = f"#{red:02x}{green:02x}00"
        # return ttk.TTkColor.fg(fg) + self._claf
        return self._claf



# class StatWin(ttk.TTkWindow):
class StatWin(WBWindow):
    def __init__(self, **kwargs):
        # super().__init__(**(kwargs|{'layout':ttk.TTkGridLayout()}))
        super().__init__(whiteBg=False, **kwargs)

        self.setTitle("Player 😎 stuff")

        self._pbHealth = ttk.TTkFancyProgressBar(
            parent=self,pos=(13,0),size=(11,1),
            lookAndFeel=ColorLAF(showText=False, color=ttk.TTkColor.fg('#FF0000')+ttk.TTkColor.bg('#330000',modifier=ttk.TTkColorGradient(orientation=ttk.TTkK.HORIZONTAL, fgincrement=100, bgincrement=100))))
        self._pbArmor  = ttk.TTkFancyProgressBar(
            parent=self,pos=(13,1),size=(11,1),
            lookAndFeel=ColorLAF(showText=False, color=ttk.TTkColor.fg('#0000FF')+ttk.TTkColor.bg('#000033',modifier=ttk.TTkColorGradient(orientation=ttk.TTkK.HORIZONTAL, fgincrement=100, bgincrement=100))))
        self._sbRight.hide()
        self._sbBottom.hide()
        glbls.player.updated.connect(self._update)
        self._update()

    def mouseReleaseEvent(self, evt) -> bool:
        glbls.root.setFocus()
        return super().mouseReleaseEvent(evt)

    def _update(self):
        self._pbHealth.setValue(glbls.player.health/glbls.player.maxHealth)
        self._pbArmor.setValue( glbls.player.armor/glbls.player.maxArmor)
        self.update()

    def paintEvent(self, canvas:ttk.TTkCanvas):
        w,h = self.size()
        # canvas.fill(color=bgBLUE)
        p:Player  = glbls.player
        pb = glbls.player.body
        sy = 1
        sx = 1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"HEALTH: {p.health}")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"ARMOR:  {p.armor}")); sy+=1
        sy+1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Head:  {Tiles[pb.head]}"))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"Body:  {Tiles[pb.body]}")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Legs:  {Tiles[pb.legs]}"))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"Feet:  {Tiles[pb.feet]}")); sy+=1
        sy+1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Hold:  {Tiles[p.weaponHeld]} - Melee: {Tiles[p.meleeHeld]}")); sy+=1

        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Weapons:")); sy+=1
        cEn   = ttk.TTkColor.RST
        cHold = ttk.TTkColor.fg("#FFFF00")+ttk.TTkColor.bg("#333300")
        cDis  = ttk.TTkColor.fg("#AAAAAA")
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr1']} Cupid Strike |{Tiles['ws1']}:{p.shells['ws1']: 3}",cDis if 'wr1' not in p.weapons else cHold if p.weaponHeld=='wr1' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr2']} Pacekeeper   |{Tiles['ws2']}:{p.shells['ws2']: 3}",cDis if 'wr2' not in p.weapons else cHold if p.weaponHeld=='wr2' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr3']} LoveZooka    |{Tiles['ws3']}:{p.shells['ws3']: 3}",cDis if 'wr3' not in p.weapons else cHold if p.weaponHeld=='wr3' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wr4']} Friend Zoner |{Tiles['ws4']}:{p.shells['ws4']: 3}",cDis if 'wr4' not in p.weapons else cHold if p.weaponHeld=='wr4' else cEn)); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"Throwables:        Keys")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wt1']}: {p.throwables['wt1']: 2} ",cHold if p.weaponHeld=='wt1' else cEn))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"{Tiles['wt2']}: {p.throwables['wt2']: 2} ",cHold if p.weaponHeld=='wt2' else cEn))
        canvas.drawTTkString(pos=(sx+18,sy),text=ttk.TTkString(Tiles['KG'] if 'KG' in p.keys else ""))
        canvas.drawTTkString(pos=(sx+21,sy),text=ttk.TTkString(Tiles['KB'] if 'KB' in p.keys else "")); sy+=1
        canvas.drawTTkString(pos=(sx   ,sy),text=ttk.TTkString(f"{Tiles['wt3']}: {p.throwables['wt3']: 2} ",cHold if p.weaponHeld=='wt3' else cEn))
        canvas.drawTTkString(pos=(sx+10,sy),text=ttk.TTkString(f"{Tiles['wt4']}: {p.throwables['wt4']: 2} ",cHold if p.weaponHeld=='wt4' else cEn))
        canvas.drawTTkString(pos=(sx+18,sy),text=ttk.TTkString(Tiles['KR'] if 'KR' in p.keys else ""))
        canvas.drawTTkString(pos=(sx+21,sy),text=ttk.TTkString(Tiles['KY'] if 'KY' in p.keys else "")); sy+=1
        canvas.drawTTkString(pos=(sx+18,sy),text=ttk.TTkString(f"{Tiles['wt2']}: {p.throwables['wt2']: 2} ",cHold if p.weaponHeld=='wt2' else cEn)); sy+=1

        # Little hack because I don't like the default borders
        canvas.drawText(pos=(0,h-1), text='🭎' + '▂'*(w-2), color=bgBLACK)
        for y in range(1,h-1):
            canvas.drawText(pos=(w-1,y), text='█', color=bgBLACK)
        for y in range(7,11):
            canvas.drawText(pos=(w-1,y), text='▐', color=bgBLACK)
        canvas.drawText(pos=(w-1,6),  text='🭔', color=bgBLACK)
        canvas.drawText(pos=(w-1,11), text='🭃', color=bgBLACK)

        canvas.drawText(pos=(3,h-1), text=f'🭃 $ {p.money: 1} 🭎', color=bgBLACK)

        super().paintEvent(canvas)
