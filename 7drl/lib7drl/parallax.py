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

__all__ = ['Parallax']

import sys, os, time

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .assets import *
from .layer  import *

class Parallax(ttk.TTkWidget):
    COLOR1 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#AFAEBC")
    COLOR2 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#858494")
    COLOR3 = ttk.TTkColor.fg("#FFFFFF")+ttk.TTkColor.bg("#63687B")
    COLOR4 = ttk.TTkColor.fg("#9694A1")+ttk.TTkColor.bg("#B3B2C0")
    COLOR5 = ttk.TTkColor.fg("#333238")+ttk.TTkColor.bg("#B3B2C0")
    COLOR6 = ttk.TTkColor.fg("#333238")+ttk.TTkColor.bg("#333238")

    def __init__(self, *args, **kwargs):
        self._baseTime = time.time()
        self._l11 = l11 = Layer(HouseBG_1_1)
        self._l12 = l12 = Layer(HouseBG_1_2)
        self._l21 = l21 = Layer(HouseBG_2_1)
        self._l22 = l22 = Layer(HouseBG_2_2)
        self._l31 = l31 = Layer(HouseBG_3_1)

        w11,h11 = l11.size()
        w12,h12 = l12.size()
        w21,h21 = l21.size()
        w22,h22 = l22.size()
        w31,h31 = l31.size()
        self._layer1 = {'size':w11+w12+w11+w11+w12,'layers':(l11,l12,l11,l11,l12),'off':(1,0,1,1,0)}
        self._layer2 = {'size':w21+w22+w21        ,'layers':(l21,l22,l21),'off':[0,4,0]}
        self._layer3 = {'size':w31+30             ,'layers':[l31]        ,'off':[0]}

        self._vPos = 0

        super().__init__(*args, **kwargs)
        ttk.TTkHelper._rootWidget.paintExecuted.connect(self._refreshAnimation)
        self._refreshAnimation()



    @ttk.pyTTkSlot()
    def _refreshAnimation(self):
        self.update()

    def setPlanePos(self, x,y):
        self._planePos = (int(x),int(y))
        self.update()

    def setVPos(self, v):
        self._vPos = int(v)
        self.update()

    def paintEvent(self, canvas: ttk.TTkCanvas):
        w,h = self.size()
        diff = int(200*(time.time() - self._baseTime))

        secH  = h//5
        # draw the bgColor
        canvas.fill(pos=(0,0), size=(w,secH*4), color=Parallax.COLOR1)

        # draw the Layers:
        def _drawLayer(_l, _pos, canvas=canvas):
            _lw  = _l['size']
            _la  = _l['layers']
            _off = _l['off']
            _x,_y = _pos
            for _ll,_lo in zip(_la,_off):
                __w,__h = _ll.size()
                _ll.drawInCanvas(pos=(_x,_y+_lo),canvas=canvas)
                _x += __w

        def _drawLayerScroll(_l, _d,_y, canvas=canvas):
            _lw  = _l['size']
            _x = (_d    )%(w+_lw)-_lw
            _x = (_d+_lw)%(w+_lw)-_lw
            _drawLayer(_l, ((_d    )%(w+_lw)-_lw,_y))
            _drawLayer(_l, ((_d+_lw)%(w+_lw)-_lw,_y))

        _drawLayerScroll(self._layer1, (-diff)//8, 3+self._vPos//4)
        canvas.fill(pos=(0,9+self._vPos//4),  size=(w,h),  color=Parallax.COLOR2)
        _drawLayerScroll(self._layer2, (-diff)//4, 4+self._vPos//2)
        canvas.fill(pos=(0,17+self._vPos//2), size=(w,h), color=Parallax.COLOR3)
        _drawLayerScroll(self._layer3, (-diff)//2, 5+self._vPos)

        #_drawLayer(self._layerPlane,self._planePos)

        #self._dungeon.drawDungeon(pos=(10,10), canvas=canvas)