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

__all__ = ['TTkAppTemplate']

from dataclasses import dataclass
from TermTk.TTkCore.canvas import TTkCanvas

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.string import TTkString
from TermTk.TTkLayouts import TTkLayout, TTkGridLayout
from TermTk.TTkWidgets.container import TTkWidget, TTkContainer
from TermTk.TTkWidgets.menubar import TTkMenuBarLayout

class TTkAppTemplate(TTkContainer):
    ''' TTkAppTemplate Layout:

    ::

        App Template Layout
        ┌─────────────────────────────────┐
        │         Header                  │
        ├─────────┬──────────────┬────────┤ H
        │         │   Top        │        │
        │         ├──────────────┤        │ T
        │         │              │        │
        │  Right  │   Main       │  Left  │
        │         │   Center     │        │
        │         │              │        │
        │         ├──────────────┤        │ B
        │         │   Bottom     │        │
        ├─────────┴──────────────┴────────┤ F
        │         Footer                  │
        └─────────────────────────────────┘
                  R              L
    '''

    MAIN   = TTkK.CENTER
    TOP    = TTkK.TOP
    BOTTOM = TTkK.BOTTOM
    LEFT   = TTkK.LEFT
    RIGHT  = TTkK.RIGHT
    CENTER = TTkK.CENTER
    HEADER = TTkK.HEADER
    FOOTER = TTkK.FOOTER

    @dataclass(frozen=False)
    class _Panel:
        # It's either item or widget
        item:    TTkLayout = None
        widget:  TTkWidget = None
        title:   TTkString = None
        menubar: TTkMenuBarLayout = None
        size:    int  = 0
        border:  bool = True
        fixed:   bool = False

        def setGeometry(self,x,y,w,h):
            if it := self.item:
                it.setGeometry(x,y,w,h)
            elif wid := self.widget:
                wid.setGeometry(x,y,w,h)

        def isVisible(self):
            if self.widget:
                return self.widget.isVisible()
            return True

        def geometry(self):
            if it := self.item:
                return it.geometry()
            if wid := self.widget:
                return wid.geometry()
            return (0,0,0,0)

        def getSize(self):
            if it := self.item:
                return it.size()
            if wid := self.widget:
                return wid.size()
            return (0,0)

        def minimumWidth(self):
            if it := self.item:
                return it.minimumWidth()
            if wid := self.widget:
                return wid.minimumWidth()
            return 0

        def minimumHeight(self):
            if it := self.item:
                return it.minimumHeight()
            if wid := self.widget:
                return wid.minimumHeight()
            return 0

        def maximumWidth(self):
            if it := self.item:
                return it.maximumWidth()
            if wid := self.widget:
                return wid.maximumWidth()
            return 0x10000

        def maximumHeight(self):
            if it := self.item:
                return it.maximumHeight()
            if wid := self.widget:
                return wid.maximumHeight()
            return 0x10000

    __slots__ = ('_panels', '_splitters', '_menubarLines', '_selected'
                 #Signals
                 )
    def __init__(self, border=False, **kwargs):
        self._panels = {
            TTkAppTemplate.MAIN   : TTkAppTemplate._Panel(item=TTkLayout(), border=border) ,
            TTkAppTemplate.TOP    : None ,
            TTkAppTemplate.BOTTOM : None ,
            TTkAppTemplate.LEFT   : None ,
            TTkAppTemplate.RIGHT  : None ,
            TTkAppTemplate.HEADER : None ,
            TTkAppTemplate.FOOTER : None }
        self._splitters = {
            TTkAppTemplate.TOP    : None ,
            TTkAppTemplate.BOTTOM : None ,
            TTkAppTemplate.LEFT   : None ,
            TTkAppTemplate.RIGHT  : None ,
            TTkAppTemplate.HEADER : None ,
            TTkAppTemplate.FOOTER : None }
        self._menubarLines = {
            TTkAppTemplate.MAIN   : None ,
            TTkAppTemplate.TOP    : None ,
            TTkAppTemplate.BOTTOM : None ,
            TTkAppTemplate.LEFT   : None ,
            TTkAppTemplate.RIGHT  : None ,
            TTkAppTemplate.HEADER : None ,
            TTkAppTemplate.FOOTER : None }
        self._selected = None

        super().__init__( **kwargs)
        self.layout().addItem(self._panels[TTkAppTemplate.MAIN].item)
        self._updateGeometries()
        self.setFocusPolicy(TTkK.ClickFocus)

    def setWidget(self, widget, position=MAIN, size=None, title="", border=None, fixed=None):
        if not self._panels[position]:
            self._panels[position] = TTkAppTemplate._Panel()
        if wid:=self._panels[position].widget:
            self.layout().removeWidget(wid)
            self._panels[position].widget = None
        if it:=self._panels[position].item:
            self.layout().removeItem(it)
            self._panels[position].item = None
        if widget:
            self._panels[position].widget = widget
            self.layout().addWidget(widget)
            if border!=None:
                self._panels[position].border = border
            if fixed != None:
               self._panels[position].fixed = fixed
            self._panels[position].title = TTkString(title)
            self._panels[position].size = ( size if size is not None else
                                            widget.minimumWidth() if position in (TTkAppTemplate.LEFT,TTkAppTemplate.RIGHT) else
                                            widget.minimumHeight() )
        self._updateGeometries()

    def setItem(self, item, position=MAIN, size=None, title="", border=None, fixed=None):
        if not self._panels[position]:
            self._panels[position] = TTkAppTemplate._Panel()
        if wid:=self._panels[position].widget:
            self.layout().removeWidget(wid)
            self._panels[position].widget = None
        if it:=self._panels[position].item:
            self.layout().removeItem(it)
            self._panels[position].item = None
        if item:
            self._panels[position].item = item
            self.layout().addItem(item)
            if border!=None:
                self._panels[position].border = border
            if fixed != None:
               self._panels[position].fixed = fixed
            self._panels[position].title = TTkString(title)
            self._panels[position].size = ( size if size is not None else
                                            item.minimumWidth() if position in (TTkAppTemplate.LEFT,TTkAppTemplate.RIGHT) else
                                            item.minimumHeight() )
        self._updateGeometries()

    def menuBar(self, position=MAIN):
        return None if not self._panels[position] else self._panels[position].menubar

    def setMenuBar(self, menuBar, position=MAIN):
        if not self._panels[position]:
            self._panels[position] = TTkAppTemplate._Panel()
        p = self._panels[position]
        if p.menubar:
            self.rootLayout().removeItem(p.menubar)
            # TODO: Dispose the menubar
        p.menubar = menuBar
        if menuBar:
            self.rootLayout().addItem(p.menubar)
        self._updateGeometries()

    def setBorder(self, border=True, position=MAIN):
        if not self._panels[position]:
            self._panels[position] = TTkAppTemplate._Panel()
        self._panels[position].border = border
        self._updateGeometries()

    def setFixed(self, fixed=False, position=MAIN):
        if not self._panels[position]:
            self._panels[position] = TTkAppTemplate._Panel()
        self._panels[position].fixed = fixed
        self._updateGeometries()

    def resizeEvent(self, w, h):
        self._updateGeometries()

    def focusOutEvent(self):
        self._selected = None
        self.update()

    def mouseReleaseEvent(self, evt):
        self._selected = None
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._selected = []
        self._updateGeometries()
        spl = self._splitters
        pns = self._panels
        for loc in (TTkAppTemplate.TOP, TTkAppTemplate.BOTTOM, TTkAppTemplate.HEADER, TTkAppTemplate.FOOTER):
            if (s:=spl[loc]) and not pns[loc].fixed and (p:=s['pos'])[1]==evt.y and p[0] <= evt.x <=p[0]+s['size']:
                self._selected.append(loc)
        for loc in (TTkAppTemplate.LEFT, TTkAppTemplate.RIGHT):
            if (s:=spl[loc]) and not pns[loc].fixed and (p:=s['pos'])[0]==evt.x and p[1] <= evt.y <=p[1]+s['size']:
                self._selected.append(loc)
        return True

    def mouseDragEvent(self, evt):
        if not self._selected: return False
        pns = self._panels
        for loc in self._selected:
            x,y,w,h = (p:=pns[loc]).geometry()
            if   loc == TTkAppTemplate.LEFT:
                p.size = evt.x-x
            elif loc == TTkAppTemplate.RIGHT:
                p.size = w+x-evt.x
            elif loc in (TTkAppTemplate.HEADER, TTkAppTemplate.TOP):
                p.size = evt.y-y
            else:
                p.size = h+y-evt.y
        self._updateGeometries()
        return True

    def minimumWidth(self):
        pns = self._panels

        # Header and Footer sizes
        mh=mf=0
        if (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible(): mh = p.minimumWidth()
        if (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible(): mf = p.minimumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        if (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible():  mcr = p.minimumWidth() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.LEFT ]) and p.isVisible():  mcl = p.minimumWidth() + ( 1 if p.border else 0 )

        # Center Top,Bottom sizes
        mct=mcb=0
        if (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible(): mct = p.minimumWidth()
        if (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible(): mcb = p.minimumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).minimumWidth()

        return max(mh, mf, mcr+mcl+max(mct, mcb, mcm)) + (2 if p.border else 0)

    def maximumWidth(self):
        pns = self._panels

        # Header and Footer sizes
        mh=mf=0x10000
        if (p:=pns[TTkAppTemplate.HEADER]) and p.isVisible(): mh = p.maximumWidth()
        if (p:=pns[TTkAppTemplate.FOOTER]) and p.isVisible(): mf = p.maximumWidth()

        # Center Right,Left sizes
        mcr=mcl=0
        if (p:=pns[TTkAppTemplate.RIGHT]) and p.isVisible():  mcr = p.maximumWidth() + ( 1 if p.border else 0 )
        if (p:=pns[TTkAppTemplate.LEFT ]) and p.isVisible():  mcl = p.maximumWidth() + ( 1 if p.border else 0 )

        # Center Top,Bottom sizes
        mct=mcb=0x10000
        if (p:=pns[TTkAppTemplate.TOP   ]) and p.isVisible(): mct = p.maximumWidth()
        if (p:=pns[TTkAppTemplate.BOTTOM]) and p.isVisible(): mcb = p.maximumWidth()

        mcm = (p:=pns[TTkAppTemplate.MAIN]).maximumWidth()

        return min(mh, mf, mcr+mcl+min(mct, mcb, mcm)) + (2 if p.border else 0)

    def minimumHeight(self):
        pns = self._panels

        # Retrieve all the panels parameters and hide the menubar if required
        def _processPanel(_loc):
            _p = pns[_loc]
            if not (_p and _p.isVisible()):
                return None, 0, False, False
            return _p, _p.minimumHeight(), _p.border, _p.menubar

        ph,mh,bh,menh = _processPanel(TTkAppTemplate.HEADER)
        pl,ml,bl,menl = _processPanel(TTkAppTemplate.LEFT)
        pr,mr,br,menr = _processPanel(TTkAppTemplate.RIGHT)
        pt,mt,bt,ment = _processPanel(TTkAppTemplate.TOP)
        pm,mm,bm,menm = _processPanel(TTkAppTemplate.MAIN)
        pb,mb,bb,menb = _processPanel(TTkAppTemplate.BOTTOM)
        pf,mf,bf,menf = _processPanel(TTkAppTemplate.FOOTER)

        # Adjust the sizes based on the menubar and the borders
        if menh and not (bm): mh += 1
        if menl and not (bh or (bm and ph==None)): ml += 1
        if menr and not (bh or (bm and ph==None)): mr += 1
        if ment and not (bh or (bm and ph==None)): mt += 1
        if menm and not (bt or (bh and pt==None) or (bm and pt==ph==None)): mm += 1
        if menb and not (bb): mb += 1
        if menf and not (bf): mf += 1

        return mh+mf+max(mr ,ml, mm+mt+mb ) + ( 2 if bm else 0 )

    def maximumHeight(self):
        pns = self._panels

        # Retrieve all the panels parameters and hide the menubar if required
        def _processPanel(_loc):
            _p = pns[_loc]
            if not (_p and _p.isVisible()):
                return None, 0, False, False
            return _p, _p.maximumHeight(), _p.border, _p.menubar

        ph,mh,bh,menh = _processPanel(TTkAppTemplate.HEADER)
        pl,ml,bl,menl = _processPanel(TTkAppTemplate.LEFT)
        pr,mr,br,menr = _processPanel(TTkAppTemplate.RIGHT)
        pt,mt,bt,ment = _processPanel(TTkAppTemplate.TOP)
        pm,mm,bm,menm = _processPanel(TTkAppTemplate.MAIN)
        pb,mb,bb,menb = _processPanel(TTkAppTemplate.BOTTOM)
        pf,mf,bf,menf = _processPanel(TTkAppTemplate.FOOTER)

        # Adjust the sizes based on the menubar and the borders
        if menh and not (bm): mh += 1
        if menl and not (bh or (bm and ph==None)): ml += 1
        if menr and not (bh or (bm and ph==None)): mr += 1
        if ment and not (bh or (bm and ph==None)): mt += 1
        if menm and not (bt or (bh and pt==None) or (bm and pt==ph==None)): mm += 1
        if menb and not (bb): mb += 1
        if menf and not (bf): mf += 1

        # Those panels cannot have null size
        if not mm: mm=0x10000
        if not ml: ml=0x10000
        if not mr: mr=0x10000

        return mh+mf+min(mr ,ml, mm+mt+mb ) + ( 2 if bm else 0 )

    def _updateGeometries(self):
        w,h = self.size()
        if w<=0 or h<=0 or not self.isVisibleAndParent(): return
        pns = self._panels
        spl = self._splitters
        mbl = self._menubarLines

        # Retrieve all the panels parameters and hide the menubar if required
        def _processPanel(_loc):
            _p = pns[_loc]
            if not (_p and _p.isVisible()):
                if _p and (_menu:=_p.menubar):
                    _menu.setGeometry(-1,-1,0,0)
                return None, 0, 0x1000, 0, True, 0, None
            _min    = _p.minimumHeight()
            _max    = _p.maximumHeight()
            _size   = min(max(_p.size,_min),_max)
            _fixed  = _p.fixed
            _border = 1 if _p.border else 0
            return _p, _min, _max, _size, _fixed, _border, _p.menubar

        pt,ptmin,ptmax,st,ft,bt,mt = _processPanel(TTkAppTemplate.TOP)
        pb,pbmin,pbmax,sb,fb,bb,mb = _processPanel(TTkAppTemplate.BOTTOM)
        ph,phmin,phmax,sh,fh,bh,mh = _processPanel(TTkAppTemplate.HEADER)
        pf,pfmin,pfmax,sf,ff,bf,mf = _processPanel(TTkAppTemplate.FOOTER)
        pl,plmin,plmax,sl,fl,bl,ml = _processPanel(TTkAppTemplate.LEFT)
        pr,prmin,prmax,sr,fr,br,mr = _processPanel(TTkAppTemplate.RIGHT)

        # Main Boundaries
        pm=pns[TTkAppTemplate.MAIN]
        mmaxw = pm.maximumWidth()
        mminw = pm.minimumWidth()
        mmaxh = pm.maximumHeight()
        mminh = pm.minimumHeight()
        bm = 1 if pns[TTkAppTemplate.MAIN].border else 0
        w-=(bm<<1)+bl+br
        h-=(bm<<1)+bt+bb+bh+bf

        # check horizontal sizes
        if not (mminw <= (newszw:=(w-sl-sr)) <= mmaxw):
            # the main width does not fit
            # we need to move the (R,L) splitters
            # * to avoid extra complexity,
            #   Let's resize the right panel first
            #   and adjust the left one to allows the
            #   main panel to fit again
            if newszw < mminw:
                if pr:                    pr.size = sr = max(prmin, w-mminw-sl) ; newszw=w-sl-sr
                if newszw < mminw and pl: pl.size = sl = max(plmin, w-mminw-sr) ; newszw=w-sl-sr
            else:
                if pr:                    pr.size = sr = min(prmax, w-mmaxw-sl) ; newszw=w-sl-sr
                if newszw > mmaxw and pl: pl.size = sl = min(plmax, w-mmaxw-sr) ; newszw=w-sl-sr

        # check vertical sizes
        if not (mminh <= (newszh:=(h-st-sb-sh-sf)) <= mmaxh):
            # almost same as before except that there are 4 panels to be considered instead of 2
            if newszh < mminh:
                if pf:                    pf.size = sf = max(pfmin, h-mminh-sb-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and pb: pb.size = sb = max(pbmin, h-mminh-sf-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and pt: pt.size = st = max(ptmin, h-mminh-sf-sb-sh) ; newszh=h-st-sb-sh-sf
                if newszh < mminh and ph: ph.size = sh = max(phmin, h-mminh-sf-sb-st) ; newszh=h-st-sb-sh-sf
            else:
                if pf:                    pf.size = sf = min(pfmax, h-mmaxh-sb-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and pb: pb.size = sb = min(pbmax, h-mmaxh-sf-st-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and pt: pt.size = st = min(ptmax, h-mmaxh-sf-sb-sh) ; newszh=h-st-sb-sh-sf
                if newszh > mmaxh and ph: ph.size = sh = min(phmax, h-mmaxh-sf-sb-st) ; newszh=h-st-sb-sh-sf

        # Resize any panel to the proper dimension
        w+=bl+br
        h+=bt+bb+bh+bf
        def _setGeometries(_loc, _p, _x,_y,_w,_h,_bbar):
            off = 0
            if _mb:=_p.menubar:
                if _bbar:
                    off = 0
                    mbl[_loc] = None
                    if _bbar[1]: # Fixed
                        styleToMerge = {'default':{'glyphs':('├','─','┤','┄','┄','▶')}}
                    else:
                        styleToMerge = {'default':{'glyphs':('╞','═','╡','┄','┄','▶')}}
                else:
                    off = 1
                    mbl[_loc] = {'pos':(_x,_y-1+off),'text':f"┄{'─'*(_w-2)}┄"}
                    styleToMerge = {'default':{'glyphs':('├','─','┤','┄','┄','▶')}}
                for m in _mb._menus(TTkK.LEFT_ALIGN):   m.mergeStyle(styleToMerge)
                for m in _mb._menus(TTkK.RIGHT_ALIGN):  m.mergeStyle(styleToMerge)
                for m in _mb._menus(TTkK.CENTER_ALIGN): m.mergeStyle(styleToMerge)
                off = 0 if _bbar else 1
                _mb.setGeometry(_x+1,_y-1+off,_w-2,1)
            _p.setGeometry(_x,_y+off,_w,_h-off)

        _setGeometries(       TTkAppTemplate.MAIN   , pm, bm+sl+bl           , bm+sh+bh+st+bt                 , newszw , newszh        , (bt and (1,ft)) or (pt==None and (bh and (1,fh))) or (ph==pt==None and (bm and (1, 1))))
        if pl: _setGeometries(TTkAppTemplate.LEFT   , pl, bm                 , bm+sh+bh                       , sl     , h-sh-bh-sf-bf , (bh and (1,fh)) or (ph==None and (bm and (1, 1))))
        if pr: _setGeometries(TTkAppTemplate.RIGHT  , pr, bm+sl+bl+newszw+br , bm+sh+bh                       , sr     , h-sh-bh-sf-bf , (bh and (1,fh)) or (ph==None and (bm and (1, 1))))
        if ph: _setGeometries(TTkAppTemplate.HEADER , ph, bm                 , bm                             , w      , sh            , (bm and (1, 1)))
        if pt: _setGeometries(TTkAppTemplate.TOP    , pt, bm+sl+bl           , bm+sh+bh                       , newszw , st            , (bh and (1,fh)) or (ph==None and (bm and (1, 1))))
        if pb: _setGeometries(TTkAppTemplate.BOTTOM , pb, bm+sl+bl           , bm+sh+bh+st+bt+newszh+bb       , newszw , sb            , (bb and (1,fb)))
        if pf: _setGeometries(TTkAppTemplate.FOOTER , pf, bm                 , bm+sh+bh+st+bt+newszh+bb+sb+bf , w      , sf            , (bf and (1,ff)))

        # Define Splitter geometries
        w,h = self.size()
        spl[TTkAppTemplate.HEADER] = None if not bh else {'pos':(0   , bm+sh                      ) ,'size':w     , 'fixed':fh , 'panel': ph }
        spl[TTkAppTemplate.FOOTER] = None if not bf else {'pos':(0   , bm+sh+bh+st+bt+newszh+bb+sb) ,'size':w     , 'fixed':ff , 'panel': pf }

        ca = sh                          + (bm if ph else 0 )
        cb = bm+sh+bh+st+bt+newszh+bb+sb + (bf if pf else bm)
        spl[TTkAppTemplate.LEFT]   = None if not bl else {'pos':(bm+sl           , ca             ) ,'size':cb-ca , 'fixed':fl , 'panel': pl }
        spl[TTkAppTemplate.RIGHT]  = None if not br else {'pos':(bm+sl+bl+newszw , ca             ) ,'size':cb-ca , 'fixed':fr , 'panel': pr }

        ca = sl              + (bm if pl else 0 )
        cb = bm+sl+bl+newszw + (br if pr else bm)
        spl[TTkAppTemplate.TOP]    = None if not bt else {'pos':(ca        , bm+sh+bh+st          ) ,'size':cb-ca , 'fixed':ft , 'panel': pt }
        spl[TTkAppTemplate.BOTTOM] = None if not bb else {'pos':(ca        , bm+sh+bh+st+bt+newszh) ,'size':cb-ca , 'fixed':fb , 'panel': pb }

        self.update()

    def update(self, repaint: bool =True, updateLayout: bool =False, updateParent: bool =False):
        if updateLayout:
            self._updateGeometries()
        super().update(repaint=repaint,updateLayout=updateLayout,updateParent=updateParent)

    #def layout(self):
    #    return self._panels[TTkAppTemplate.MAIN].item

    #def setLayout(self, layout):
    #    self._panels[TTkAppTemplate.MAIN].item = layout

    def paintEvent(self, canvas: TTkCanvas):
        w,h = self.size()
        pns = self._panels
        spl = self._splitters
        mbl = self._menubarLines

        if b:=pns[TTkAppTemplate.MAIN].border:
            canvas.drawBox(pos=(0,0), size=(w,h))

        selectColor = TTkColor.fg('#88FF00')

        # hline = ('╞','═','╡')
        # vline = ('╥','║','╨')

        def drawVLine(sp, color=TTkColor.RST):
            _x,_y = sp['pos']
            _w,_h = 1,sp['size']
            chs = ('│','┬','┴','╿','╽') if sp['fixed'] else ('║','╥','╨','┇','┇')
            canvas.fill(pos=(_x,_y), size=(_w,_h), color=color, char=chs[0] )
            canvas.drawChar(pos=(_x,_y),           color=color, char=chs[1]if b and _y==0    else chs[3])
            canvas.drawChar(pos=(_x,_y+_h-1),      color=color, char=chs[2]if b and _y+_h==h else chs[4])
        def drawHLine(sp, color=TTkColor.RST):
            _x,_y = sp['pos']
            _w,_h = sp['size'],1
            chs = ('─','├','┤','╾','╼') if sp['fixed'] else ('═','╞','╡','╍','╍')
            canvas.fill(pos=(_x,_y), size=(_w,_h), color=color, char=chs[0] )
            canvas.drawChar(pos=(_x,_y),           color=color, char=chs[1]if b and _x==0    else chs[3])
            canvas.drawChar(pos=(_x+_w-1,_y),      color=color, char=chs[2]if b and _x+_w==w else chs[4])
            if _title:=sp['panel'].title:
                _l = min(w-2,_title.termWidth())
                _tx = (_w-_l)//2
                canvas.drawChar(pos=(_x+_tx,_y),     color=color, char=chs[2])
                canvas.drawChar(pos=(_x+_tx+_l+1,_y),color=color, char=chs[1])
                canvas.drawTTkString(pos=(_x+_tx+1,_y),text=_title,width=_l)

        # Draw the 4 splittters
        if (sp:=spl[TTkAppTemplate.HEADER]) : drawHLine(sp, color=selectColor if self._selected and TTkAppTemplate.HEADER in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.FOOTER]) : drawHLine(sp, color=selectColor if self._selected and TTkAppTemplate.FOOTER in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.LEFT])   : drawVLine(sp, color=selectColor if self._selected and TTkAppTemplate.LEFT   in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.RIGHT])  : drawVLine(sp, color=selectColor if self._selected and TTkAppTemplate.RIGHT  in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.TOP])    : drawHLine(sp, color=selectColor if self._selected and TTkAppTemplate.TOP    in self._selected else TTkColor.RST)
        if (sp:=spl[TTkAppTemplate.BOTTOM]) : drawHLine(sp, color=selectColor if self._selected and TTkAppTemplate.BOTTOM in self._selected else TTkColor.RST)

        # Draw the 12 intersect
        def drawIntersect(sph,spv,chs):
            if sph and spv:
                x = spv['pos'][0]
                y = sph['pos'][1]
                ch = chs[( 0 if sph['fixed'] else 0x01 ) | ( 0 if spv['fixed'] else 0x02 )]
                canvas.drawChar(pos=(x,y), char=ch)

        drawIntersect(spl[TTkAppTemplate.HEADER], spl[TTkAppTemplate.LEFT] , ('┬','╤','╥','╦'))
        drawIntersect(spl[TTkAppTemplate.HEADER], spl[TTkAppTemplate.RIGHT], ('┬','╤','╥','╦'))
        drawIntersect(spl[TTkAppTemplate.FOOTER], spl[TTkAppTemplate.LEFT] , ('┴','╧','╨','╩'))
        drawIntersect(spl[TTkAppTemplate.FOOTER], spl[TTkAppTemplate.RIGHT], ('┴','╧','╨','╩'))
        drawIntersect(spl[TTkAppTemplate.TOP   ], spl[TTkAppTemplate.LEFT] , ('├','╞','╟','╠'))
        drawIntersect(spl[TTkAppTemplate.TOP   ], spl[TTkAppTemplate.RIGHT], ('┤','╡','╢','╣'))
        drawIntersect(spl[TTkAppTemplate.BOTTOM], spl[TTkAppTemplate.LEFT] , ('├','╞','╟','╠'))
        drawIntersect(spl[TTkAppTemplate.BOTTOM], spl[TTkAppTemplate.RIGHT], ('┤','╡','╢','╣'))

        # Draw extra MenuBar Lines if there is no border to place them
        for l in mbl:
            if mb:=mbl[l]:
                canvas.drawText(pos=mb['pos'],text=mb['text'])

        return super().paintEvent(canvas)