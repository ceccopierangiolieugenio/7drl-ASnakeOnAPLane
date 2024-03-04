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


__all__ = ['Game']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .parallax import *
from .dungeon  import *

class Game(ttk.TTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parallax = Parallax(pos=(5,3), size=(100,26))
        self._dungeon = Dungeon()
        self._dungeonPos = (0,0)

        self._parallaxTimer = ttk.TTkTimer()
        self._parallaxTimer.timeout.connect(self.update)
        self._parallaxTimer.timeout.connect(lambda :self._parallaxTimer.start(0.05))
        self._parallaxTimer.start(0.1)

        btnRnd = ttk.TTkButton(parent=self, text=' RND ', border=True)

        btnRnd.clicked.connect(self.setFocus)
        btnRnd.clicked.connect(self._dungeon.genDungeon)
        btnRnd.clicked.connect(self.landingAnim)

        self.landingAnim()

    def landingAnim(self):
        self._dungeon.setFading(0)

        # Entering the Parallax
        animVPos = ttk.TTkPropertyAnimation(self._parallax, self._parallax.setVPos)
        animVPos.setStartValue(50)
        animVPos.setEndValue(   0)
        animVPos.setDuration(2)
        animVPos.setEasingCurve(ttk.TTkEasingCurve.OutQuint)
        animVPos.start()

        def _animFading():
        # Dungeon Animation
            animFading = ttk.TTkPropertyAnimation(self._dungeon,self._dungeon.setFading)
            animFading.setStartValue(0)
            animFading.setEndValue(  1)
            animFading.setDuration(1)
            animFading.setEasingCurve(ttk.TTkEasingCurve.OutQuint)
            animFading.start()

        # Dungeon Animation
        animPlane = ttk.TTkPropertyAnimation(self,self.setDungeonPos)
        animPlane.setStartValue((-150,-30))
        animPlane.setEndValue(  ( 50, 15))
        animPlane.setDuration(2)
        animPlane.setEasingCurve(ttk.TTkEasingCurve.OutBack)
        animPlane.start()
        animPlane.finished.connect(_animFading)

    def setDungeonPos(self, x,y):
        self._dungeonPos = (int(x),int(y))
        self.update()

    def keyEvent(self, evt) -> bool:
        if evt.type != ttk.TTkK.SpecialKey:
            if evt.key == 'r':
                self._dungeon.genDungeon()
            return super().keyEvent(evt)
        d = self._dungeon
        if   evt.key == ttk.TTkK.Key_Up:
            self._dungeon.moveHero(d.UP)
        elif evt.key == ttk.TTkK.Key_Down:
            self._dungeon.moveHero(d.DOWN)
        elif evt.key == ttk.TTkK.Key_Left:
            self._dungeon.moveHero(d.LEFT)
        elif evt.key == ttk.TTkK.Key_Right:
            self._dungeon.moveHero(d.RIGHT)
        else:
            return super().keyEvent(evt)
        self.update()
        return True


    def paintEvent(self, canvas: ttk.TTkCanvas):
        super().paintEvent(canvas)
        # Update Parallax
        pc = self._parallax.getCanvas()
        self._parallax.paintEvent(pc)
        # Draw Dungeon in the Parallax canvas
        hpx,hpy = self._dungeon.heroPos()
        dpx,dpy = self._dungeonPos
        self._dungeon.drawDungeon((dpx-hpx*2,dpy-hpy),pc)
        pw,ph = pc.size()
        canvas.paintCanvas(pc,cg:=(5,3,pw,ph),cg,cg)


