# MIT License
#
# Copyrightte (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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
from .globals  import *

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

        btnMsg  = ttk.TTkButton(  parent=self, pos=( 0,0), text='Messages', border=True)
        btnInfo = ttk.TTkButton(  parent=self, pos=(10,0), text='Info',     border=True)

        cbDebug = ttk.TTkCheckbox(parent=self, pos=(16,1), text='Debug', size=(8,1), checked=False)
        debugFrame = ttk.TTkFrame(parent=self, pos=(24,0), size=(50,3),layout=ttk.TTkGridLayout(), visible=False, border=False)
        debugFrame.layout().addWidget(btnTest := ttk.TTkButton(  text='TEST' , border=True),     0,0,3,1)
        debugFrame.layout().addWidget(btnRnd  := ttk.TTkButton(  text=' RND ', border=True),     0,1,3,1)
        debugFrame.layout().addWidget(           ttk.TTkLabel( text="Level:"), 0,2)
        debugFrame.layout().addWidget(sbLevel := ttk.TTkSpinBox( value=1, minimum=1, maximum=5), 1,2)

        cbDebug.toggled.connect(debugFrame.setVisible)
        sbLevel.valueChanged.connect(globals.setLevel)

        def _attachSignal(_btn,_slots):
            _btn.clicked.connect(self.setFocus)
            for _slot in _slots:
                _btn.clicked.connect(_slot)

        _attachSignal(btnTest, [self._testGame])
        _attachSignal(btnRnd, [self._dungeon.genDungeon, self.landingAnim])

        self.landingAnim()
        self.setFocus()

    @ttk.pyTTkSlot()
    def _testGame(self):
        win = ttk.TTkWindow(title='Test',size=(100,20),layout=ttk.TTkGridLayout())
        te = ttk.TTkTextEdit(parent=win, readOnly=False, lineNumber=True)
        te.setText(TEST_TILES)
        ttk.TTkHelper.overlay(None, win, 0,0)

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
        animPlane.setEndValue(  ( 100//2, 26//2))
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

    def mousePressEvent(self, evt) -> bool:
        self._mouseSavePos = (evt.x,evt.y)
        self._dungeonSavePos = self._dungeonPos
        return True

    def mouseDragEvent(self, evt) -> bool:
        w,h=self._dungeon.size()
        x,y   = self._mouseSavePos
        hx,hy = self._dungeonSavePos
        # x=max(0,min(w-1,hx-(x-evt.x)//2))
        # y=max(0,min(h-1,hy-(y-evt.y)))
        x = hx-(x-evt.x)
        y = hy-(y-evt.y)
        # self._dungeon._heroPos = (x,y)
        self.setDungeonPos(x,y)
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


