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

__all__ = ['ObjInfo']

import sys, os
sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

from .assets import *

ObjInfo = {
    '#' : [ ttk.TTkString("   This is a Wall ") + Tiles['#' ] ,
            ttk.TTkString(" Seriously, what do you expect?") ] ,
    '@' : [ttk.TTkString("   Fluid Snake ") + Tiles['@' ],
           ttk.TTkString(" Fuck Yeahhhhh!!! "), ] ,

    'D' : [ttk.TTkString("This is a closed Door ") + Tiles['D']] ,
    'd' : [ttk.TTkString("This is an open Door ") + Tiles['d']] ,

    'DR' : [ttk.TTkString("This is a RED Door ")    + Tiles['DR'],
            ttk.TTkString("You need a RED Key ")    + Tiles['KR']] ,
    'DG' : [ttk.TTkString("This is a GREEN Door ")  + Tiles['DG'],
            ttk.TTkString("You need a GREEN Key ")  + Tiles['KG']] ,
    'DB' : [ttk.TTkString("This is a BLUE Door ")   + Tiles['DB'],
            ttk.TTkString("You need a BLUE Key ")   + Tiles['KB']] ,
    'DY' : [ttk.TTkString("This is a YELLOW Door ") + Tiles['DY'],
            ttk.TTkString("You need a YELLOW Key ") + Tiles['KY']] ,
    'KR' : [ttk.TTkString(" a RED Key ")    + Tiles['KR'],
            ttk.TTkString("Use it to open a RED Door ")    + Tiles['DR']] ,
    'KG' : [ttk.TTkString(" a GREEN Key ")  + Tiles['KG'],
            ttk.TTkString("Use it to open a GREEN Door ")  + Tiles['DG']] ,
    'KB' : [ttk.TTkString(" a BLUE Key ")   + Tiles['KB'],
            ttk.TTkString("Use it to open a BLUE Door ")   + Tiles['DB']] ,
    'KY' : [ttk.TTkString(" a YELLOW Key ") + Tiles['KY'],
            ttk.TTkString("Use it to open a YELLOW Door ") + Tiles['DY']] ,
    # Armors
    'af1' : [ttk.TTkString(" Flavoury Boots ") + Tiles['af1'],
             ttk.TTkString("   Armor +15")] ,
    'af2' : [ttk.TTkString(" Magic socks ") + Tiles['af2'],
             ttk.TTkString("   Armor +20")] ,
    'af3' : [ttk.TTkString(" Comfortable Shoes ") + Tiles['af3'],
             ttk.TTkString("   Armor +25")] ,
    'af4' : [ttk.TTkString(" Sweaty Runners ") + Tiles['af4'],
             ttk.TTkString("   Armor +30")] ,
    'af5' : [ttk.TTkString(" Flipping Flops ") + Tiles['af5'],
             ttk.TTkString("   Armor +35")] ,
    'ah1' : [ttk.TTkString(" Soft Helmet ") + Tiles['ah1'],
             ttk.TTkString("   Armor +15")] ,
    'ah2' : [ttk.TTkString(" Sligtly Harder Helmet ") + Tiles['ah2'],
             ttk.TTkString("   Armor +20")] ,
    'ah3' : [ttk.TTkString(" Graduation Cap ") + Tiles['ah3'],
             ttk.TTkString("Only for the hardest heads"),
             ttk.TTkString("   Armor +23")] ,
    'ah4' : [ttk.TTkString(" Stray Hat ") + Tiles['ah4'],
             ttk.TTkString("Nothing protects you better against the UVA"),
             ttk.TTkString("   Armor +30")] ,
    'ah5' : [ttk.TTkString(" Cool Boy Cap") + Tiles['ah5'],
             ttk.TTkString("Only the fearless can wear it"),
             ttk.TTkString("   Armor +35")] ,
    'ab1' : [ttk.TTkString(" Juicy Shirt ") + Tiles['ab1'],
             ttk.TTkString("You'll be beautiful in it"),
             ttk.TTkString("   Armor +15")] ,
    'ab2' : [ttk.TTkString(" No Idea what's that ") + Tiles['ab2'],
             ttk.TTkString("   Armor +20")] ,
    'ab3' : [ttk.TTkString(" Kimono of the Power ") + Tiles['ab3'],
             ttk.TTkString("   Armor +25")] ,
    'ab4' : [ttk.TTkString(" Not yet wedding Dress ") + Tiles['ab4'],
             ttk.TTkString("   Armor +30")] ,
    'ab5' : [ttk.TTkString(" Chainmail Bikini ") + Tiles['ab5'],
             ttk.TTkString("Best armor in any RPG"),
             ttk.TTkString("   Armor +35")] ,
    'al1' : [ttk.TTkString(" Sausage Holder ") + Tiles['al1'],
             ttk.TTkString("I would recommend this Item"),
             ttk.TTkString("before starting any adventure"),
             ttk.TTkString("   Armor +10")] ,
    'al2' : [ttk.TTkString(" Small Sausage Holder ") + Tiles['al2'],
             ttk.TTkString("Less to hide, less to damage"),
             ttk.TTkString("   Armor +20")] ,
    'al3' : [ttk.TTkString(" Mystery Arse Protector ") + Tiles['al3'],
             ttk.TTkString("   Armor +30")] ,
    # Weapons
    'wm1' : [ttk.TTkString("Silk Gloves ") + Tiles['wm1']] ,
    'wm2' : [ttk.TTkString("Magic Flute ") + Tiles['wm2']] ,
    'wm3' : [ttk.TTkString("Tooth Brusher ") + Tiles['wm3']] ,
    'wm4' : [ttk.TTkString("Gourmet Knife ") + Tiles['wm4']] ,
    'wr1' : [ttk.TTkString("Cupid strike ") + Tiles['wr1']] ,
    'wr2' : [ttk.TTkString("Pacekeeper ") + Tiles['wr2']] ,
    'wr3' : [ttk.TTkString("Lovezooka ") + Tiles['wr3']] ,
    'wr4' : [ttk.TTkString("Friend Zoner ") + Tiles['wr4']] ,
    'ws1' : [ttk.TTkString("Cupid strike Shells ") + Tiles['ws1']] ,
    'ws2' : [ttk.TTkString("Pacekeeper Shells ") + Tiles['ws2']] ,
    'ws3' : [ttk.TTkString("Lovezooka Shells ") + Tiles['ws3']] ,
    'ws4' : [ttk.TTkString("Friend Zoner Shells ") + Tiles['ws4']] ,
    'wt1' : [ttk.TTkString("Friendly Curling ") + Tiles['wt1']] ,
    'wt2' : [ttk.TTkString("Enlighter ") + Tiles['wt2']] ,
    'wt3' : [ttk.TTkString("Sex Bomb ") + Tiles['wt3']] ,
    'wt4' : [ttk.TTkString("DeThronizer ") + Tiles['wt4']] ,
    # Gold
    'g1' : [ttk.TTkString("A bunch of $ - 10$ ") + Tiles['g1']] ,
    'g2' : [ttk.TTkString("A bunch of € - 13$ ") + Tiles['g2']] ,
    'g3' : [ttk.TTkString("A bunch of £ - 27$ ") + Tiles['g3']] ,
    'g4' : [ttk.TTkString("A bunch of ₤ - 44$ ") + Tiles['g4']] ,
    'g5' : [ttk.TTkString("Golden coin - 142$ ") + Tiles['g5']] ,
    'g6' : [ttk.TTkString("My aunt Purse - 364$ ") + Tiles['g6']] ,
    'g7' : [ttk.TTkString("Potato bag - 735$ ") + Tiles['g7']] ,
    'g8' : [ttk.TTkString("Piece of glass -1297$ ") + Tiles['g8']] ,

    'HIT': [ttk.TTkString("This is ") + Tiles['HIT']] ,

    'b' : [ttk.TTkString("Black Box ") + Tiles['b']] ,
    # Exit
    '>' : [ttk.TTkString("This is the Exit") + Tiles['>' ]] ,
}