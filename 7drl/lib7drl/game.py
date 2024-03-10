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
GEOMETRIES = {
    'hackPos'  : {'pos':(-1,-1),'size':(  1, 1)},
    'root'     : {'pos':(0 , 0),'size':(109,30)},
    'stat'     : {'pos':(83, 0),'size':( 26,15)},
    'msgs'     : {'pos':(83,15),'size':( 26,15)},
    # 'msgsInit' : {'pos':(10, 3),'size':( 85,18)},
    'dungeon'  : {'pos':( 0, 0),'size':( 83,30)},
    'parallax' : {'pos':( 0, 0),'size':( 83,30),'v0':48,'v1':0},
    'deathWid' : {'pos':( 0, 0),'size':(105,30)},
}

LOSER_SENTENCE = [
                ["You are an individual whose efforts in the realm of ","success resemble a floundering fish in ","a dry desert.",],
                ["You are one who dances with failure so skillfully, ","it's as if they've crafted an intricate ","waltz with defeat.",],
                ["You are a connoisseur of calamity, navigating the ","waters of misfortune with unparalleled finesse.",],
                ["You are an aficionado of inadequacy, painting ","masterpieces of mediocrity on the canvas of life.",],
                ["You are a virtuoso of defeat, orchestrating symphonies ","of disappointment with breathtaking precision.",],
                ["You are a purveyor of pitiful pursuits, forever ","chasing the elusive shadow of accomplishment.",],
                ["You are a curator of catastrophe, sculpting monuments ","of ineptitude in the grand gallery of existence.",],
                ["You are a maestro of misfortune, conducting the orchestra ","of their own downfall with ","unwavering dedication.",],
                ["You are a savant of subpar performance, crafting ","opuses of underachievement in the theater of life.",],
                ["You are a luminary of loss, illuminating the path ","to defeat with a radiant glow of ineptitude."],
                ["You are a prodigy of patheticness, whose achievements in the realm ","of success are but mere whispers in ","the cacophony of triumph.",],
                ["You are an architect of adversity, constructing monuments of ","failure that defy the laws of probability.",],
                ["You are a bard of blunder, spinning tales of misfortune that ","captivate the hearts of all who witness their journey.",],
                ["You are a paragon of pitifulness, whose escapades in the pursuit ","of victory rival the exploits of Sisyphean legend.",],
                ["You are a luminary of lamentation, casting a shadow of defeat so ","vast it blots out the very sun of success.",],
                ["You are a harbinger of humiliation, heralding the arrival of ","failure with a flourish and a fanfare.",],
                ["You are a virtuoso of defeat, composing sonnets of sorrow that ","resonate across the vast expanse of human experience.",],
                ["You are a titan of tragedy, whose endeavors in the arena of achievement ","are akin to a Greek epic of unfulfilled potential.",],
                ["You are an artisan of inadequacy, sculpting monuments of mediocrity ","with the precision of a master craftsman.",],
                ["You are a doyen of disappointment, whose exploits in the pursuit of ","excellence are a testament to the ","boundless depths of human folly.",],
                ["You are a luminary of lackluster performance, whose endeavors in ","the pursuit of greatness are a testament ","to the resilience of ineptitude.",],
                ["You are a maestro of mishap, conducting symphonies of failure with ","the grace and poise of a seasoned virtuoso.",],
                ["You are a sage of subpar achievement, dispensing wisdom born of ","countless missteps and foiled ambitions.",],
                ["You are an oracle of underachievement, whose prophecies of failure ","are as inevitable as the rising sun.",],
                ["You are a maestro of missteps, choreographing dances of disappointment ","that leave audiences both bemused and bewildered.",],
                ["You are a luminary of lowliness, whose exploits in the realm of ","success are a beacon for all who seek ","the path of least resistance.",],
                ["You are a juggernaut of junk, bulldozing through the landscape ","of success with all the finesse of a wrecking ball.",],
                ["You are a phoenix of failure, rising from the ashes of defeat ","with all the grace and dignity of a clumsy ostrich.",],
                ["You are a savant of stagnation, whose mastery of the art ","of underachievement is matched only by ","their steadfast refusal to improve.",],
                ["You are a virtuoso of vulgarity, whose exploits in the ","realm of success are a testament to the ","boundless depths of human folly.",],
                ["You are a connoisseur of catastrophe, whose palate for failure is as refined as it is insatiable."],

            ]


class Game(ttk.TTk):
    def __init__(self, debug=True, level=1, skipIntro=False, **kwargs):
        glbls.root = self
        glbls.level = min(5,max(0,level))
        glbls.debug = debug
        super().__init__(**kwargs)
        boundL = ttk.TTkLayout(**GEOMETRIES['root'])
        self.rootLayout().addItem(boundL)

        self._parallax = Parallax(**GEOMETRIES['parallax'])
        self._dungeon = Dungeon()

        self._youDiedWidget = YouDiedWidget(**(GEOMETRIES['hackPos']|{'parent':self,'visible':False}))

        self._parallaxTimer = ttk.TTkTimer()
        self._parallaxTimer.timeout.connect(self.update)
        self._parallaxTimer.timeout.connect(lambda :self._parallaxTimer.start(0.05))
        self._parallaxTimer.start(0.1)

        glbls.player = Player()

        self._statWin = StatWin(   **(GEOMETRIES['stat']|{'parent':self,'title':'Messages'}))
        self._msgWin  = MessageWin(**(GEOMETRIES['msgs']|{'parent':self,'title':'Messages'}))
        self._btnNext          = ttk.TTkButton( pos=(0,-10), text=' Next '           , border=True,enabled=False)
        self._btnNewGame       = ttk.TTkButton( pos=(0,-10), text=' New Game '       , border=True,enabled=False)
        self._btnNewGamePlus   = ttk.TTkButton( pos=(0,-10), text=' New Game Plus '  , border=True,enabled=False)
        self._btnNewGameMinus  = ttk.TTkButton( pos=(0,-10), text=' New Game Minus ' , border=True,enabled=False)
        glbls.seed = f" Seed: 0x{random.randint(0,0xFFFFFFFF):08X}"
        self._textSeed         = ttk.TTkLineEdit(pos=(0,-10), size=(20,1), text=glbls.seed)

        self.layout().addWidget(self._btnNext)
        boundL.addWidgets([
                self._btnNewGame, self._btnNewGamePlus, self._btnNewGameMinus,
                self._textSeed
            ])


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

        if skipIntro:
            self.landingAnim()
            glbls.playing = True
        else:
            self._initialScreen()
        self.setFocus()

    def _quickAnim(self,fr,to,time,trans,obj,fn,cbks=[]):
        _anim = ttk.TTkPropertyAnimation(obj,fn)
        _anim.setStartValue(fr)
        _anim.setEndValue(  to)
        _anim.setDuration(time)
        _anim.setEasingCurve(trans)
        for n in cbks:
            _anim.finished.connect(n)
        _anim.start()

    def _disableMenuBtns(self):
        # Little hack to overcome the button being cleared during the signal
        self._btnNext.clicked.clear()
        self._btnNewGame.clicked.clear()
        self._btnNewGamePlus.clicked.clear()
        self._btnNewGameMinus.clicked.clear()
        self._btnNext.setEnabled(False)
        self._btnNewGame.setEnabled(False)
        self._btnNewGamePlus.setEnabled(False)
        self._btnNewGameMinus.setEnabled(False)
        self._youDiedWidget.nextAction.clear()

    def _initialScreen(self):
        #If there is time I will add a snake anim
        self._initialScreenMenu()

    def _initialScreenMenu(self):
        glbls.player.resetStats()
        self._dungeon.initDungeonZero()
        glbls.playing = False
        x,y = GEOMETRIES['parallax']['pos']
        w,h = GEOMETRIES['parallax']['size']
        self._dungeonPos = (0,-10)
        self._parallax.setVPos(GEOMETRIES['parallax']['v0'])
        self._msgWin.setGeometry(x+10,y+3,w-20,18)
        self._btnNext.move(-10,18)
        self._statWin.move(83,-15)
        self._statWin.resize(*GEOMETRIES['stat']['size'])
        self._disableMenuBtns()

        self._youDiedWidget.hide()
        self._btnNewGame.raiseWidget()
        self._btnNewGame.setFocus()
        self._btnNewGamePlus.raiseWidget()
        self._btnNewGameMinus.raiseWidget()
        self._textSeed.raiseWidget()

        self._btnNewGame.clicked.connect(self._newGameIntro)
        # self._btnNewGamePlus
        # self._btnNewGameMinus
        self._btnNewGame.setEnabled(True)
        # self._btnNewGamePlus.setEnabled(True)
        # self._btnNewGameMinus.setEnabled(True)

        EC = ttk.TTkEasingCurve
        self._quickAnim(( 0,h),(16,22), 1, EC.OutBounce, self._btnNewGame,      self._btnNewGame.move)
        self._quickAnim((25,h),(30,22), 1, EC.OutBounce, self._btnNewGamePlus,  self._btnNewGamePlus.move)
        self._quickAnim((60,h),(49,22), 1, EC.OutBounce, self._btnNewGameMinus, self._btnNewGameMinus.move)
        self._quickAnim((25,h),(25,26), 1, EC.Linear,    self._textSeed,        self._textSeed.move)

        Message.clean(ttk.TTkString("  A Snake on a Plane🛩️- The Roguelike"))
        Message.add(ttk.TTkString(""),)
        Message.add(ttk.TTkString("Embrace the journey of Fluid Snake 😎 in the"),)
        Message.add(ttk.TTkString("perilous land of The Love air Boats 🌹"),)
        Message.add(ttk.TTkString(""),)
        Message.add(ttk.TTkString("  ←↑↓→ or W A S D = Direction"),)
        Message.add(ttk.TTkString("            Space = Wait"),)
        Message.add(ttk.TTkString("                E = Action (climb/grab/interact)"),)
        Message.add(ttk.TTkString(""),)
        Message.add(ttk.TTkString("Use the mouse to aim, shot, or drag the map"),)
        Message.add(ttk.TTkString("or change the weapon with the weel"),)
        Message.add(ttk.TTkString(""),)
        Message.add(ttk.TTkString("(This is a text window)"),)
        Message.add(ttk.TTkString("  - you can scroll -"),)
        Message.add(ttk.TTkString(""),)
        Message.add(ttk.TTkString("  Choose and perish"),)

    def _newGameIntro(self):
        glbls.playing = False
        mwx,mwy,mww,mwh=self._msgWin.geometry()
        swx,swy,sww,swh=self._statWin.geometry()
        x,y = GEOMETRIES['parallax']['pos']
        w,h = GEOMETRIES['parallax']['size']

        self._youDiedWidget.hide()

        EC = ttk.TTkEasingCurve
        self._quickAnim((20,22),( 0,h), 0.5, EC.Linear, self._btnNewGame,      self._btnNewGame.move)
        self._quickAnim((32,22),(25,h), 0.5, EC.Linear, self._btnNewGamePlus,  self._btnNewGamePlus.move)
        self._quickAnim((50,22),(60,h), 0.5, EC.Linear, self._btnNewGameMinus, self._btnNewGameMinus.move)
        self._quickAnim((25,26),(25,h), 0.5, EC.Linear, self._textSeed,        self._textSeed.move)

        glbls.seed = self._textSeed.text().toAscii()
        random.seed(glbls.seed)
        Message.add(ttk.TTkString(f""))
        Message.add(ttk.TTkString(f"Seed Used: '{glbls.seed}'"))
        Message.add(ttk.TTkString(f""))
        ttk.TTkLog.debug(f"Seed Used: '{glbls.seed}'")

        messages = {
            'id':0,
            'msg':[
                [
                    ttk.TTkString(""),
                    ttk.TTkString("################################"),
                    ttk.TTkString(""),
                    ttk.TTkString("🥸 Hello Fluid Snake..."),
                    ttk.TTkString(""),
                ],
                [
                    ttk.TTkString("   Who are you?            😎"),
                    ttk.TTkString("")
                ],
                [
                    ttk.TTkString("🥸 No time to explain"),
                    ttk.TTkString("   The world is in danger"),
                    ttk.TTkString("   There is 'A Snake on a Plane'"),
                    ttk.TTkString("   You need to find it!!!"),
                    ttk.TTkString(""),
                ],
                [
                    ttk.TTkString("   Cool, which plane?      😎"),
                    ttk.TTkString("")
                ],
                [
                    ttk.TTkString("🥸 You are not paid to make questions"),
                    ttk.TTkString("")
                ],
            ]
        }

        def _nextMessage(m=messages):
            if m['id'] >= len(m['msg']):
                self._btnNext.clicked.clear()
                self._newGame()
                return
            for msg in m['msg'][m['id']]:
                Message.add(msg)
            m['id']+=1

        self._btnNext.setEnabled(True)
        self._btnNext.clicked.connect(_nextMessage)

        mwx,mwy,mww,mwh=self._msgWin.geometry()
        swx,swy,sww,swh=self._statWin.geometry()
        self._quickAnim(( mwx,mwy),(x+10,y+5), 0.5, EC.Linear, self._msgWin,  self._msgWin.move)
        self._quickAnim(( mww,mwh),(w-20, 12), 0.5, EC.Linear, self._msgWin,  self._msgWin.resize)
        self._quickAnim(( -10,-18),(  20, 18), 0.5, EC.Linear, self._btnNext, self._btnNext.move, [_nextMessage])

    def _firstBreak(self):
        glbls.playing = False
        messages = {
            'id':0,
            'msg':[
                [
                    ttk.TTkString(""),
                    ttk.TTkString("################################"),
                    ttk.TTkString(""),
                    ttk.TTkString("🥸 Hey Fluid Snake..."),
                    ttk.TTkString("   How is it going?"),
                    ttk.TTkString(""),
                ],
                [
                    ttk.TTkString("   I was having fun till   😎"),
                    ttk.TTkString("   you arrived, what's up?"),
                    ttk.TTkString("")
                ],
                [
                    ttk.TTkString("🥸 Remember"),
                    ttk.TTkString("   Don't harm the Snake"),
                    ttk.TTkString(""),
                ],
            ]
        }

        x,y = GEOMETRIES['parallax']['pos']
        w,h = GEOMETRIES['parallax']['size']
        mwx,mwy,mww,mwh=self._msgWin.geometry()
        EC = ttk.TTkEasingCurve

        def _nextMessage(m=messages):
            if m['id'] >= len(m['msg']):
                self._btnNext.clicked.clear()
                self._nextLevel()
                self._quickAnim((20,18),(-10,18), 0.5, EC.Linear, self._btnNext, self._btnNext.move)
                self._quickAnim((mwx,mwy),GEOMETRIES['msgs']['pos'],  1, EC.OutBounce, self._msgWin, self._msgWin.move)
                self._quickAnim((mww,mwh),GEOMETRIES['msgs']['size'], 1, EC.OutBounce, self._msgWin, self._msgWin.resize)
                return
            for msg in m['msg'][m['id']]:
                Message.add(msg)
            m['id']+=1

        self._btnNext.setEnabled(True)
        self._btnNext.clicked.connect(_nextMessage)

        self._quickAnim(( mwx,mwy),(x+10,y+5), 0.5, EC.Linear, self._msgWin,  self._msgWin.move)
        self._quickAnim(( mww,mwh),(w-20, 12), 0.5, EC.Linear, self._msgWin,  self._msgWin.resize)
        self._quickAnim((-10,18),  (20  , 18), 0.5, EC.Linear, self._btnNext, self._btnNext.move, [_nextMessage])


    def _endBreak(self):
        glbls.playing = False
        last_message = [
                    ttk.TTkString( "🥸 Don't be greedy, you collected"),
                    ttk.TTkString(f"   {glbls.player.money}$ along the way"),
                    ttk.TTkString()]
        for ls in random.choice(LOSER_SENTENCE):
            last_message.append(ttk.TTkString(f"   {ls}"))
        last_message.append(ttk.TTkString())
        messages = {
            'id':0,
            'msg':[
                [
                    ttk.TTkString(""),
                    ttk.TTkString("################################"),
                    ttk.TTkString(""),
                    ttk.TTkString("🥸 Good Job Fluid Snake..."),
                    ttk.TTkString("   You saved the world"),
                    ttk.TTkString(""),
                ],
                [
                    ttk.TTkString("   Thanks...               😎"),
                    ttk.TTkString("   What about the payment?"),
                    ttk.TTkString("")
                ],
                last_message
            ]
        }

        x,y = GEOMETRIES['parallax']['pos']
        w,h = GEOMETRIES['parallax']['size']
        mwx,mwy,mww,mwh=self._msgWin.geometry()
        EC = ttk.TTkEasingCurve

        def _nextMessage(m=messages):
            if m['id'] >= len(m['msg']):
                self._btnNext.clicked.clear()
                self._initialScreen()
                return
            for msg in m['msg'][m['id']]:
                Message.add(msg)
            m['id']+=1

        self._btnNext.setEnabled(True)
        self._btnNext.clicked.connect(_nextMessage)

        self._quickAnim(( mwx,mwy),(x+10,y+5), 0.5, EC.Linear, self._msgWin,  self._msgWin.move)
        self._quickAnim(( mww,mwh),(w-20, 12), 0.5, EC.Linear, self._msgWin,  self._msgWin.resize)
        self._quickAnim((-10,18),  (20  , 18), 0.5, EC.Linear, self._btnNext, self._btnNext.move, [_nextMessage])


    def _showDeadStats(self):
        x,y = GEOMETRIES['root']['pos']
        w,h = GEOMETRIES['root']['size']
        mwx,mwy,mww,mwh=self._msgWin.geometry()
        EC = ttk.TTkEasingCurve

        self._youDiedWidget.lowerWidget()
        #self._youDiedWidget.nextAction.clear()
        self._btnNext.raiseWidget()
        self._msgWin.raiseWidget()
        self._btnNext.setEnabled(True)
        self._btnNext.clicked.connect(self._initialScreen)

        def _showStats():
            Message.add(ttk.TTkString())
            for ds in glbls.player.deathSentence:
                Message.add(ds)
            Message.add(ttk.TTkString(f"You lost {glbls.player.money}$ in the explosion"))
            Message.add(ttk.TTkString("and your kids will get NOTHING,"))
            Message.add(ttk.TTkString(""))
            for ls in random.choice(LOSER_SENTENCE):
                Message.add(ttk.TTkString(ls))
            Message.add(ttk.TTkString(""))

        self._quickAnim(( 30,10),(x+10,y+5), 0.5, EC.Linear, self._msgWin,  self._msgWin.move)
        self._quickAnim(( 0,0),(w-20, 12), 0.5, EC.Linear, self._msgWin,  self._msgWin.resize)
        self._quickAnim((-10,18),(20, 18), 0.5, EC.Linear, self._btnNext, self._btnNext.move, [_showStats])

    def _newGame(self):
        mwx,mwy,mww,mwh=self._msgWin.geometry()
        swx,swy,sww,swh=self._statWin.geometry()
        w,h = GEOMETRIES['root']['size']

        EC = ttk.TTkEasingCurve
        self._quickAnim((20,18),(-10,18), 0.5, EC.Linear, self._btnNext, self._btnNext.move)
        self._quickAnim((mwx,mwy),GEOMETRIES['msgs']['pos'],  1, EC.OutBounce, self._msgWin, self._msgWin.move)
        self._quickAnim((mww,mwh),GEOMETRIES['msgs']['size'], 1, EC.OutBounce, self._msgWin, self._msgWin.resize)
        self._quickAnim((swx,swy),GEOMETRIES['stat']['pos'],  1, EC.OutBounce, self._statWin,self._statWin.move)
        self._quickAnim((sww,swh),GEOMETRIES['stat']['size'], 1, EC.Linear,    self._statWin,self._statWin.resize, [self._disableMenuBtns])
        self.landingAnim()
        self.setFocus()
        glbls.playing = True

    @ttk.pyTTkSlot()
    def _nextLevel(self):
        if glbls.level <= 1:
            glbls.level = 2
            self._firstBreak()
            return
        def _doIt():
            glbls.player.resetKeys()
            self._dungeon.genDungeon()
            self.landingAnim()
            glbls.playing = True
            self.setFocus()
            glbls.level = min(5,glbls.level+1)
        self.takingOffAnim([_doIt])

    @ttk.pyTTkSlot()
    def _endGame(self):
        glbls.playing = False
        glbls.level = 1
        self.takingOffAnim([self._endBreak])

    @ttk.pyTTkSlot()
    def _death(self):
        glbls.playing = False
        glbls.level = 1
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
        self._youDiedWidget.raiseWidget()
        self._youDiedWidget.nextAction.connect(self._showDeadStats)


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
            _anim.setStartValue(GEOMETRIES['parallax']['v0'])
            _anim.setEndValue(  GEOMETRIES['parallax']['v1'])
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
            _anim.setStartValue(GEOMETRIES['parallax']['v1'])
            _anim.setEndValue(  GEOMETRIES['parallax']['v0'])
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
        if not glbls.playing: return False
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
        if not glbls.playing: return False
        if evt.evt == ttk.TTkK.WHEEL_Down:
            glbls.player.nextWeapon()
        else:
            glbls.player.prevWeapon()
        return True

    def mousePressEvent(self, evt) -> bool:
        if not glbls.playing: return False
        self._dragging = False
        self._mouseSavePos = (evt.x,evt.y)
        self._dungeonSavePos = self._dungeonPos
        return True

    def mouseDoubleClickEvent(self, evt) -> bool:
        if not glbls.playing: return False
        hpx,hpy = self._dungeon.heroPos()
        dpx,dpy = self._dungeonPos
        px,py   = self._parallax.pos()
        mpx,mpy = evt.x-px-dpx,evt.y-py-dpy
        if glbls.debug:
            self._dungeon._heroPos = (mpx//2+hpx,mpy+hpy)
            return True
        return super().mouseDoubleClickEvent(evt)

    def mouseReleaseEvent(self, evt) -> bool:
        if not glbls.playing: return False
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
        if not glbls.playing: return False
        self._dragging = False
        hpx,hpy = self._dungeon.heroPos()
        dpx,dpy = self._dungeonPos
        px,py   = self._parallax.pos()
        mpx,mpy = evt.x-px-dpx,evt.y-py-dpy
        self._dungeon.moveMouse(mpx//2+hpx,mpy+hpy)
        return True

    def mouseDragEvent(self, evt) -> bool:
        if not glbls.playing: return False
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


