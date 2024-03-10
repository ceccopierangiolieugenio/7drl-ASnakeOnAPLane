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

import sys, os, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .parallax import *
from .dungeon  import *
from .assets   import *
from .glbls    import *
from .statwin  import *
from .player   import *
from .messages import *
from .youdiedscreen import *

from wblib    import WBWindow

# Thanks ChatGPT
funny_plane_names = [
    "Air Force Zero",
    "Air Goose",
    "Wing Wonder",
    "Turbulence Terminator",
    "Cloud Cruiser",
    "Flyin' Banana",
    "Sky Squirrel",
    "Aero Avocado",
    "Propeller Puffin",
    "Altitude Alpaca",
    "Jet Jester",
    "Whirlybird Whiz",
    "Skyward Sloth",
    "Aero Avocado",
    "Aviary Avenger",
    "Feathered Falcon",
    "Sonic Sloth",
    "Nimbus Ninja",
    "Aerodynamic Armadillo",
    "Zephyr Zebra",
    "Gliding Gopher"
]

class Game(ttk.TTk):
    def __init__(self, debug=True, level=1, **kwargs):
        glbls.root = self
        glbls.level = min(5,max(0,level))
        glbls.debug = debug
        super().__init__(**kwargs)
        self._parallax = Parallax(pos=(0,0), size=(83,30))
        self._dungeon = Dungeon()
        self._dungeonPos = (0,0)

        self._youDiedWidget = YouDiedWidget(parent=self, visible=False)

        self._parallaxTimer = ttk.TTkTimer()
        self._parallaxTimer.timeout.connect(self.update)
        self._parallaxTimer.timeout.connect(lambda :self._parallaxTimer.start(0.05))
        self._parallaxTimer.start(0.1)

        glbls.player = Player()
        statWin = StatWin( parent=self, pos=(83,0),size=(26,15))
        msgWin  = MessageWin(parent=self, pos=(83,15),size=(26,15), title='Messages' )

        # btnMsg  = ttk.TTkButton(  parent=self, pos=( 0,0), text='Messages', border=True, checkable=True)
        # btnInfo = ttk.TTkButton(  parent=self, pos=(10,0), text='Info',     border=True, checkable=True, checked=True)

        def _attachSignal(_btn,_slots):
            _btn.clicked.connect(self.setFocus)
            for _slot in _slots:
                _btn.clicked.connect(_slot)

        def _rndButton():
            self.takingOffAnim([
                self._dungeon.genDungeon,
                self.landingAnim
            ])

        if debug:
            cbDebug = ttk.TTkCheckbox(parent=self, pos=(0,30), text='Debug', size=(8,1), checked=True)
            debugFrame = ttk.TTkFrame(parent=self, pos=(9,30), size=(50,3),layout=ttk.TTkGridLayout(), visible=True, border=False)
            debugFrame.layout().addWidget(btnTest := ttk.TTkButton(  text='TEST' , border=True),     0,0,3,1)
            debugFrame.layout().addWidget(btnRnd  := ttk.TTkButton(  text=' RND ', border=True),     0,1,3,1)
            debugFrame.layout().addWidget(           ttk.TTkLabel( text="Level:"), 0,2)
            debugFrame.layout().addWidget(sbLevel := ttk.TTkSpinBox( value=glbls.level, minimum=1, maximum=5), 1,2)
            debugFrame.layout().addWidget(cbGod   := ttk.TTkCheckbox(text='God Mode', checked=False), 2,2)
            debugFrame.layout().addWidget(cbShow  := ttk.TTkCheckbox(text='ShowMap',  checked=False), 2,3)

            cbDebug.toggled.connect(debugFrame.setVisible)
            sbLevel.valueChanged.connect(glbls.setLevel)

            @ttk.pyTTkSlot(bool)
            def _setGod(mode):
                glbls.godMode = mode
            cbGod.toggled.connect(_setGod)

            @ttk.pyTTkSlot(bool)
            def _setMap(mode):
                glbls.showMap = mode
            cbShow.toggled.connect(_setMap)

            _attachSignal(btnTest, [self._testGame])
            _attachSignal(btnRnd, [_rndButton])

        glbls.nextLevel.connect(self._nextLevel)
        glbls.endGame.connect(self._endGame)
        glbls.death.connect(self._death)

        # btnInfo.toggled.connect(statWin.setVisible)
        # btnInfo.toggled.connect(self.setFocus)
        # btnInfo.clicked.connect(statWin.raiseWidget)

        self.landingAnim()
        self.setFocus()

    @ttk.pyTTkSlot()
    def _nextLevel(self):
        def _doIt():
            glbls.level = min(5,glbls.level+1)
            glbls.player.resetKeys()
            self._dungeon.genDungeon()
            self.landingAnim()
        self.takingOffAnim([_doIt])

    @ttk.pyTTkSlot()
    def _endGame(self):
        pass
    @ttk.pyTTkSlot()
    def _death(self):
        self.deathAnim([self._youDiedScreen])

    @ttk.pyTTkSlot()
    def _testGame(self):
        win = ttk.TTkWindow(title='Test',size=(83,20),layout=ttk.TTkGridLayout())
        te = ttk.TTkTextEdit(parent=win, readOnly=False, lineNumber=True)
        te.setText(TEST_TILES)
        ttk.TTkHelper.overlay(None, win, 0,0)

    @ttk.pyTTkSlot()
    def _youDiedScreen(self):
        self._youDiedWidget.setGeometry(0,0,109,30)
        self._youDiedWidget.raiseWidget()
        _anim = ttk.TTkPropertyAnimation(self._youDiedWidget,self._youDiedWidget.setFading)
        _anim.setStartValue(0  )
        _anim.setEndValue(  100)
        _anim.setDuration(2)
        _anim.setEasingCurve(ttk.TTkEasingCurve.InOutQuad)
        # _anim.finished.connect(__animHero)
        _anim.start()
        self._youDiedWidget.show()

    def landingAnim(self):
        self._dungeon.setFading(0)
        # self._dungeon.setBouncingHero(-5,-20)

        def __animHero():
        # Dungeon Animation
            _anim = ttk.TTkPropertyAnimation(self._dungeon,self._dungeon.setBouncingHero)
            _anim.setStartValue((-5,-20))
            _anim.setEndValue(  (  0,  0))
            _anim.setDuration(1.5)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutBounce)
            _anim.start()

        def __anim():
        # Dungeon Animation
            _anim = ttk.TTkPropertyAnimation(self._dungeon,self._dungeon.setFading)
            _anim.setStartValue(0)
            _anim.setEndValue(  1)
            _anim.setDuration(1)
            _anim.setEasingCurve(ttk.TTkEasingCurve.InOutQuad)
            # _anim.finished.connect(__animHero)
            _anim.start()

        def _parallaxAnim():
            # Entering the Parallax
            _anim = ttk.TTkPropertyAnimation(self._parallax, self._parallax.setVPos)
            _anim.setStartValue(50)
            _anim.setEndValue(   0)
            _anim.setDuration(2)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutQuint)
            _anim.start()

        def _dungeonAnim():
            Message.add(ttk.TTkString(f"- Phase {glbls.level} -"))
            Message.add(ttk.TTkString(f"Entering {random.choice(funny_plane_names)}"))
            # Dungeon Animation
            _anim = ttk.TTkPropertyAnimation(self,self.setDungeonPos)
            _anim.setStartValue((-150,-30))
            _anim.setEndValue(  ( 100//2, 30//2))
            _anim.setDuration(2)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutBack)
            _anim.finished.connect(__anim)
            _anim.start()

        _parallaxAnim()
        _dungeonAnim()

    def takingOffAnim(self,next):
        self._dungeon.setFading(1)

        def _parallaxAnim():
            # Entering the Parallax
            _anim = ttk.TTkPropertyAnimation(self._parallax, self._parallax.setVPos)
            _anim.setStartValue( 0)
            _anim.setEndValue(  50)
            _anim.setDuration(2)
            _anim.setEasingCurve(ttk.TTkEasingCurve.InQuint)
            _anim.start()

        def _dungeonAnim():
            # Dungeon Animation
            _anim = ttk.TTkPropertyAnimation(self,self.setDungeonPos)
            _anim.setStartValue(  ( 100//2, 30//2))
            _anim.setEndValue(    ( 150,-30))
            _anim.setDuration(2)
            _anim.setEasingCurve(ttk.TTkEasingCurve.InBack)
            for n in next:
                _anim.finished.connect(n)
            _anim.start()

        def __anim():
        # Dungeon Animation
            _anim = ttk.TTkPropertyAnimation(self._dungeon,self._dungeon.setFading)
            _anim.setStartValue(1)
            _anim.setEndValue(  0)
            _anim.setDuration(1)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutQuint)
            _anim.start()
            _anim.finished.connect(_dungeonAnim)
            _anim.finished.connect(_parallaxAnim)

        __anim()

    def deathAnim(self,next):
        self._dungeon.setFading(1)

        def _explosionAnim():
            _anim = ttk.TTkPropertyAnimation(self._dungeon,self._dungeon.setExplosionPos)
            _anim.setStartValue((100,30))
            _anim.setEndValue(  (-65,15))
            _anim.setDuration(1)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutQuad)
            for n in next:
                _anim.finished.connect(n)
            _anim.start()

        def _dungeonAnim():
            hpx,hpy = self._dungeon.heroPos()
            dw,dh = self._dungeon.size()
            dpx,dpy = self._dungeonPos
            # Dungeon Animation
            dx,dy = self._dungeonPos
            _anim = ttk.TTkPropertyAnimation(self,self.setDungeonPos)
            _anim.setStartValue(  ( 100//2, 30//2))
            # _anim.setEndValue(    ( 100//2+50, hpy))
            _anim.setEndValue(    ( 100//2+50, 40+hpy))
            _anim.setDuration(1.5)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutQuart)
            _anim.finished.connect(_explosionAnim)

            _anim.start()

        def __anim():
        # Dungeon Animation
            _anim = ttk.TTkPropertyAnimation(self._dungeon,self._dungeon.setFading)
            _anim.setStartValue(1)
            _anim.setEndValue(  0)
            _anim.setDuration(1)
            _anim.setEasingCurve(ttk.TTkEasingCurve.OutQuint)
            _anim.start()

        __anim()
        _dungeonAnim()

    def setDungeonPos(self, x,y):
        self._dungeonPos = (int(x),int(y))
        self.update()

    def checkGameProgress(self):
        player:Player = glbls.player
        if player.health <= 0:
            glbls.death.emit()

    def keyEvent(self, evt) -> bool:
        d = self._dungeon
        if evt.type != ttk.TTkK.SpecialKey:
            if glbls.debug and evt.key == 'r': self._dungeon.genDungeon()
            elif glbls.debug and evt.key == 't': self._death()
            elif evt.key == 'w': self._dungeon.moveHero(d.UP)    ; self._dungeon.foesAction()
            elif evt.key == 's': self._dungeon.moveHero(d.DOWN)  ; self._dungeon.foesAction()
            elif evt.key == 'a': self._dungeon.moveHero(d.LEFT)  ; self._dungeon.foesAction()
            elif evt.key == 'd': self._dungeon.moveHero(d.RIGHT) ; self._dungeon.foesAction()
            elif evt.key == 'e': self._dungeon.heroAction()      ; self._dungeon.foesAction()
            elif evt.key == 'g': self._dungeon.heroAction()      ; self._dungeon.foesAction()
            elif evt.key == '<': self._dungeon.heroAction()      ; self._dungeon.foesAction()
            elif evt.key == ' ': self._dungeon.foesAction()#
            self.checkGameProgress()
            self.update()
            return True
        if   evt.key == ttk.TTkK.Key_Up:    self._dungeon.moveHero(d.UP)    ; self._dungeon.foesAction()
        elif evt.key == ttk.TTkK.Key_Down:  self._dungeon.moveHero(d.DOWN)  ; self._dungeon.foesAction()
        elif evt.key == ttk.TTkK.Key_Left:  self._dungeon.moveHero(d.LEFT)  ; self._dungeon.foesAction()
        elif evt.key == ttk.TTkK.Key_Right: self._dungeon.moveHero(d.RIGHT) ; self._dungeon.foesAction()
        else:
            return super().keyEvent(evt)
        self.checkGameProgress()
        self.update()
        return True

    def wheelEvent(self, evt) -> bool:
        if evt.evt == ttk.TTkK.WHEEL_Down:
            glbls.player.nextWeapon()
        else:
            glbls.player.prevWeapon()
        return True

    def mousePressEvent(self, evt) -> bool:
        self._dragging = False
        self._mouseSavePos = (evt.x,evt.y)
        self._dungeonSavePos = self._dungeonPos
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        hpx,hpy = self._dungeon.heroPos()
        dpx,dpy = self._dungeonPos
        px,py   = self._parallax.pos()
        mpx,mpy = evt.x-px-dpx,evt.y-py-dpy
        if glbls.debug:
            self._dungeon._heroPos = (mpx//2+hpx,mpy+hpy)
            return True
        return super().mouseDoubleClickEvent(evt)

    def mouseReleaseEvent(self, evt) -> bool:
        hpx,hpy = self._dungeon.heroPos()
        dpx,dpy = self._dungeonPos
        px,py   = self._parallax.pos()
        mpx,mpy = evt.x-px-dpx,evt.y-py-dpy
        if not self._dragging:
            self._dungeon.shotWeapon(mpx//2+hpx,mpy+hpy)
            self.checkGameProgress()
        self._dragging = False
        return True

    def mouseMoveEvent(self, evt) -> bool:
        self._dragging = False
        hpx,hpy = self._dungeon.heroPos()
        dpx,dpy = self._dungeonPos
        px,py   = self._parallax.pos()
        mpx,mpy = evt.x-px-dpx,evt.y-py-dpy
        self._dungeon.moveMouse(mpx//2+hpx,mpy+hpy)
        return True

    def mouseDragEvent(self, evt) -> bool:
        self._dragging = True
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
        px,py,pw,ph = self._parallax.geometry()
        canvas.paintCanvas(pc,cg:=(px,py,pw,ph),cg,cg)


