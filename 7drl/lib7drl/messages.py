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


__all__ = ['MessageWin','Message']

from dataclasses import dataclass
import sys, os, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk

# from .player  import *
# from .dungeon import *
# from .assets  import *
from .glbls   import *
from wblib    import WBScrollWin, bgBLUE

class Message():
    pushText = ttk.pyTTkSignal(ttk.TTkString)
    listMessages = [
        ttk.TTkString("A Snake🐍 on a Plane✈️ - The Roguelike"),
        ttk.TTkString(""),
        ttk.TTkString("Embrace the journey of"),
        ttk.TTkString("Fluid Snake 😎 in the"),
        ttk.TTkString("perilous land of"),
        ttk.TTkString("The Love air Boats 🌹"),
        ttk.TTkString(""),
        ttk.TTkString("Choose and perish"),
        ttk.TTkString(""),
        ttk.TTkString("(This is a text window)"),
        ttk.TTkString("  - you can scroll -"),
        ttk.TTkString(""),
        ttk.TTkString(""),
        ttk.TTkString("←↑↓→ or"),
        ttk.TTkString("W A S D = Direction"),
        ttk.TTkString("  Space = Wait"),
        ttk.TTkString("      E = Action"),
        ttk.TTkString("     (climb/grab)"),
        ttk.TTkString(""),
        ttk.TTkString("Use the mouse to aim,"),
        ttk.TTkString("shot, or drag the map"),
        ttk.TTkString("or change the weapon"),
        ttk.TTkString("with the weel"),
        ]
    def add(text):
        if type(text) == str:
            text = ttk.TTkString(text)
        Message.listMessages.append(text)
        Message.pushText.emit(text)


class _MessagesViewer(ttk.TTkAbstractScrollView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewChanged.connect(self.update)
        Message.pushText.connect(self._newText)

    def viewFullAreaSize(self) -> list[int, int]:
        w = max(m.termWidth() for m in Message.listMessages)
        h = len(Message.listMessages)
        return w , h

    def _newText(self):
        offx, offy = self.getViewOffsets()
        _,h = self.size()
        offy = len(Message.listMessages)-h
        self.viewMoveTo(offx, offy)
        self.viewChanged.emit()
        self.update()

    def viewDisplayedSize(self) -> list[int, int]:
        return self.size()

    def paintEvent(self, canvas):
        ox,oy = self.getViewOffsets()
        canvas.fill(color=bgBLUE)
        _,h = self.size()
        for y, message in enumerate(Message.listMessages[oy:oy+h]):
            canvas.drawTTkString(pos=(-ox,y),text=message, color=bgBLUE)


# logWin = WBScrollWin(pos=(10,10), size=(60,20),
#                 whiteBg=False,
#                 title=f"Key Press Viewer",layout=ttk.TTkVBoxLayout())
# logWin.setViewport(_TTkLogViewer())

# class StatWin(ttk.TTkWindow):
class MessageWin(WBScrollWin):
    def __init__(self, **kwargs):
        # super().__init__(**(kwargs|{'layout':ttk.TTkGridLayout()}))
        # super().__init__(whiteBg=False, **kwargs)
        super().__init__(**kwargs)
        self.setViewport(_MessagesViewer())
