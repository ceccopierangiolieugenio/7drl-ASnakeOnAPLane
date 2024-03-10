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

__all__ = ['Layer']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class Layer():
    def __init__(self, imageData) -> None:
        self._imageData = imageData
        self.processData(imageData)
        self._h = len(imageData['data'])
        self._w = len(imageData['data'][0])

    def size(self):
        return self._w, self._h

    def getGlyph(self,x,y):
        return self._imageData['data'][y][x]

    def getColor(self,x,y):
        return self._imageData['colors'][y][x]

    def forceColor(self,color):
        for sls in self._data['opaque']:
            for sl in sls[0]:
                a,b = sl[0]
                sl[2] = [color]*(b-a)
            for sl in sls[1]:
                a = sl[0]
                sl[2] = color
        for sls in self._data['transparent']:
            for sl in sls[0]:
                a,b = sl[0]
                sl[2] = [color]*(b-a)
            for sl in sls[1]:
                a = sl[0]
                sl[2] = color

    def processData(self, imageData):
        # Trying to extract for each line the slices that can be copied and the slices that are transparent (nobg is defined)
        data = imageData['data']
        colors = imageData['colors']
        opaques = []
        transparents = []
        for rowd,rowc in zip(data,colors):
            slicesOpaque = []
            slicesTrans  = []
            pixOpaque = []
            pixTrans  = []
            curSlice = []
            transparent = False

            def _pushSlice(t, cs, so=slicesOpaque, st=slicesTrans, po=pixOpaque, pt=pixTrans):
                if not cs: return
                xa,xb = cs[0]
                if transparent:
                    pix = pt
                    sl = st
                else:
                    pix = po
                    sl = so
                if xa==xb:
                    cs[0] = xa
                    cs[1] = cs[1][0]
                    cs[2] = cs[2][0]
                    pix.append(tuple(cs))
                else:
                    # cs[0] = slice(xa,xb+1)
                    cs[0] = (xa,xb+1)
                    sl.append(tuple(cs))
                cs.clear()

            for x, (ch,(fg,bg)) in enumerate(zip(rowd,rowc)):
                if ch == ' ' and fg==bg==None: # Fully transparent space
                    _pushSlice(transparent,curSlice)
                    continue
                if bg and transparent:
                    _pushSlice(transparent,curSlice)
                    transparent = False
                elif not bg and not transparent:
                    _pushSlice(transparent,curSlice)
                    transparent = True
                if not curSlice:
                    curSlice = [[x,x],[],[]]
                curSlice[0][1]=x
                curSlice[1].append(ch)
                if fg and bg:
                    curSlice[2].append(ttk.TTkColor.fg(fg)+ttk.TTkColor.bg(bg))
                elif fg:
                    curSlice[2].append(ttk.TTkColor.fg(fg))
                elif bg:
                    curSlice[2].append(ttk.TTkColor.bg(bg))
                else:
                    curSlice[2].append(ttk.TTkColor.RST)
            _pushSlice(transparent,curSlice)
            transparents.append(list([slicesTrans,pixTrans]))
            opaques.append(list([slicesOpaque,pixOpaque]))
        self._data = {'opaque':     tuple(opaques),
                      'transparent':tuple(transparents)}

    def drawInCanvas(self, pos, canvas:ttk.TTkCanvas):
        x,y = pos
        w,h = canvas.size()
        if y>=h or x>=w: return
        if x+self._w < 0 or y+self._h<0: return
        for ly,sls in enumerate(self._data['opaque'][0:h-y],y):
            if ly<0 or ly>=h: continue
            for sl in sls[0]:
                a,b = sl[0]
                if x+a>=w or x+b<0 : continue
                ca = max(0,min(w,x+a))
                cb = max(0,min(w,x+b))
                da = ca-(x+a)
                db = cb-ca+da
                # canvas._data[  ly][ca:cb] = ['X']*(cb-ca)# sl[1][da:db]
                canvas._data[  ly][ca:cb] = sl[1][da:db]
                canvas._colors[ly][ca:cb] = sl[2][da:db]
            for sl in sls[1]:
                a = sl[0]
                if not (0 <= x+a < w): continue
                canvas._data[ly][x+sl[0]] = sl[1]
                if type(sl[2]) != ttk.TTkColor:
                    pass
                canvas._colors[ly][x+sl[0]] = sl[2]
        for ly,sls in enumerate(self._data['transparent'][0:h-y],y):
            if ly<0 or ly>=h: continue
            for sl in sls[0]:
                a,b = sl[0]
                if x+a>=w or x+b<0 : continue
                ca = max(0,min(w,x+a))
                cb = max(0,min(w,x+b))
                da = ca-(x+a)
                db = cb-ca+da
                canvas._data[  ly][ca:cb] = sl[1][da:db]
                for mcx,mc in enumerate(zip(canvas._colors[ly][ca:cb],sl[2][da:db]),ca):
                    canvas._colors[ly][mcx] = mc[0] + mc[1]
            for sl in sls[1]:
                a = sl[0]
                if not (0 <= x+a < w): continue
                canvas._data[ly][x+sl[0]] = sl[1]
                canCol = canvas._colors[ly][x+sl[0]]
                newCol = canCol + sl[2]
                canvas._colors[ly][x+sl[0]] = newCol