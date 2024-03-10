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

__all__ = ['YouDiedWidget']

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

DATA =[ ttk.TTkString('🭣🭔🭀 🭋🭟🭘◢▀▀▀▀▀◣ 🭢█     █🭗    █▀▀▀▀🭕🭍🬿 🭣█🭘 █▀▀▀▀▀  █▀▀▀▀🭕🭍🬿'),
        ttk.TTkString(' 🭦🭐 🭅🭛 █     █  █     █     █     🭥█  █  █       █     🭥█'),
        ttk.TTkString('  🭖🭩🭡  █     █  █     █     █      █  █  █       █      █'),
        ttk.TTkString('  🭦█🭛  █     █  █     █     █      █  █  █▀▀▀▀   █      █'),
        ttk.TTkString('   █   █     █  █     █     █     🭊█  █  █       █     🭊█'),
        ttk.TTkString('  🭇█🬼  ◥▄▄▄▄▄◤  ◥▄▄▄▄▄◤     █▄▄▄▄🭄🭞🭚 🭈█🬽 █▄▄▄▄▄  █▄▄▄▄🭄🭞🭚') ]


class YouDiedWidget(ttk.TTkWidget):
    def __init__(self, *args, **kwargs):
        self.nextAction = ttk.pyTTkSignal()
        self._fading = 100
        self._color = ttk.TTkColor.RST
        self._stringSize = DATA[0].termWidth()
        super().__init__(*args, **kwargs)

    def setFading(self, value):
        self._fading = int(value)
        r=int(255*value/100)
        self._color = ttk.TTkColor.fg(f'#{r:02X}0000')
        self.update()

    def paintEvent(self, canvas: ttk.TTkCanvas):
        canvas.fill(color=ttk.TTkColor.RST)
        w,h = self.size()

        gx,gy = 15,5
        gurucolor = ttk.TTkColor.fg("#FF0000")
        canvas.drawText(pos=(gx,gy+0),text="▀"*(70),color=gurucolor)
        canvas.drawText(pos=(gx,gy+3),text="▄"*(70),color=gurucolor)
        for y in range(0,4):
            canvas.drawText(pos=(gx   ,gy+y),text="█",color=gurucolor)
            canvas.drawText(pos=(gx+70,gy+y),text="█",color=gurucolor)

        canvas.drawText(pos=(gx+ 5,gy+1),text="Software Failure.",color=gurucolor)
        canvas.drawText(pos=(gx+30,gy+1),text="Press left mouse button to continue.",color=gurucolor)
        canvas.drawText(pos=(gx+15,gy+2),text="Error:  3P1C 7A1L         Task:  L05ER",color=gurucolor)

        x = 22
        for y,s in enumerate(DATA,12):
            canvas.drawTTkString(pos=(x,y),text=s,color=self._color)

    def mousePressEvent(self, evt) -> bool:
        self.nextAction.emit()
        return True
