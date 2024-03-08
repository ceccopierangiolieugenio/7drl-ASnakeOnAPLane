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

__all__ = ['HouseBG_1_1','HouseBG_1_2',
           'HouseBG_2_1','HouseBG_2_2',
           'HouseBG_3_1',
           'CLOUD_1','CLOUD_2',
           'PLANE_FRONT','PLANE_BACK','PLANE_BODY_1',
           'TEST_TILES','Tiles' ]

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
from  TermTk import TTkUtil,TTkString,TTkColor

HouseBG_1_1 = TTkUtil.base64_deflate_2_obj(
    "eJxrYJmayM0ABrVTNHpYUhJLEqfETtEAoh5GhSkZLJiwh/nRtKYpIHIaVnkETAWagqaX5cP8te1TwFTLFAyZ6TAhNvxGgRSv2QMxpgtCNWJ3CxumgZiuwuJHkAX70I0U" +
    "IN4A4oNkCOhN7WFLzs/JLyqGpgw/v7YpxOIedmULUwsTS5Mp6BxSTEHHqQRcgcdWBI8KHJweIsmnuHyD2xc09BIqB6eXKAwfghFJQz9RHM/0sgc9nAY8GEYOZzS8R8N7" +
    "OHNGw5vO4Z1aqgcAL7yIzQ==")

HouseBG_1_2 = TTkUtil.base64_deflate_2_obj(
    "eJxrYJn6lY8BDGqnaPSwpCSWJE6JnaIBRD2MClMyWHDBHuZH0xqngMgmPKoQMBVoIk6zWD7MX7toCprARLDpzVNAnDV7wdTaBpx2YTcfZML0KRlsQDYHFl2cGWxg0/dg" +
    "MRaHgSBXLCfKxzgM44AbM504Y/hAnpgGUcsG8VLLlAxR/EGKH4LMaJ2SIU7It6TDQWdOag9bcn5OflExNFX7+bVNIQf3sCtbmFqYWJpMQeeQayI6TiXDdagOQfDI4+D2" +
    "I/V8T6wv8dtIXX/TMKxoFiQD4mkqc8gIGyLDAHccDLyvaZfysAcSwfQJDuMB99aw5uCJAEqNHo29ocwZjb2hzBmNvaHMSU0t1QMAlN+srA==")

HouseBG_2_1 = TTkUtil.base64_deflate_2_obj(
    "eJztl8FKw0AQhhXTFBHBYw4eBC89eRGiT9E38FA1kINQqHoUaoWqGPSybUEoBb3qG/g0PoGPYHYbjEs26e5mk9nAdFrKx6abf+ef2U2HzmTkr7HXDelEznnvqkdOSCd+" +
    "R+t7JHT0Itr4nt6SsEW/RyRyfhafQ+3J8iKIRcqKmSd3Z1IW/+FNoIsNzAn94bMh2dJi6a0fCIcz46nT0ucyMU9LO8dSmuilH19Fl7qGRUoHNTeuyW3BWHupil4xYUVw" +
    "R0IvbNWtkIutgrEdTVVeHKL1pzmiTj8K7WND9yw7L0bKU6Bx08C8K3PzFy5dy1SwFk4ZzZmB1cpErGf2TsLdhGjCX4vkFZWITsinThCVNYJ6eKlpVqjK+GSFqkygqsar" +
    "CiL3rH/RH1wmj3Td7pjU/Yna+/6hf3x0SuQBQqfKJzCYS37hKRVBbrJ0JjMLzTAV2kA5N0EM5MECr0z6Jrv/GM8beCuWr2xLLQVrBXBLle3RKXjI4xtLw+S+Df9sALKJ" +
    "6RSUTp0DOGuZowobArjWGp9/VhWdZS4ilNibwCWVrOtyZ7qo0iVmhM8GgnLhwCup8LjSbX+F/sBdHyFbROByLADdwwZeOQKCHVD+/yy2FwJCfnvxjVPtvVgvwq8aAQFB" +
    "BbBxERAaCNi4CAgNBGxcBIQGQhBcH/wCnyVIJQ==")

HouseBG_2_2= TTkUtil.base64_deflate_2_obj(
    "eJxrYJm6hI8BDGqnaPSwpCSWJE6JnaIBRD2MClMyWNBhD/Ojab0QcVZMWUyYCjQJuylTp4DIbpBZ7BkcQDGWD/PXtk8BUWv2QW0Gc/ZMgWlpmZLBA6L7p+C1ghNoIFj9" +
    "BLAVnVOAIvwgVtcUqDWNUzIEYeav7ULzJliwbwp248GSi7AEDC4I1tCD3TRe4o0BQnEg5kYxgwcISTEBEjhgs7DHC2lw0JiR2sOWnJ+TX1QMTbp+fm1TiME97MpmxmYW" +
    "5klTCAlSilOJdBWK5RguoUSWeD8TZw6xviPXzSQ4ibCDUQURPGpz8IYWrlCil+OGJofkIMXUMOB+GGQc/BkIJWyJM2M0BVM9VohThj+ORjmDgTMaR4OfMxpHg5+Tmlqq" +
    "BwBHZ7KE")

# HouseBG_3_1 = TTkUtil.base64_deflate_2_obj(
#     "eJztV81OGzEQLmpISzjApSeKRBSJRkqJIjZU4coD5A045GeRD5WQWnpEavmJetgW2k6qSqgFCYlTeYS+DE/AnQu2dzebdXaDN2uzTjWZON7vs/fbyXjGcT7m+ndbT/hr" +
#     "H8pOrtvaa8E2lOnbmVkBkpMxJ3d7fv0ZWPf3n+Q9yc2mPknMm+Xe9Lg31wcw8O+Ly3wDks/At1nynMyNsAUyr9YbyRhpt4f8cJ7e/OzHZgobPVGaR9MSF7IQO7L4uPHg" +
#     "xfIjchH40B/FdS63QvzRF24l/4IQe+my4aximUT3gCVBZ4nxn4B9HiX8HpJ+UuVLGEZnwnO4s9998sVgoBhilhU4NbrtTGTc4a8S0TKp1mjk4Zitc/8UyCvWX9F+YOXI" +
#     "62h2FI0bjb5eNSk2bmKw3DwEUuH8S2qsr7iYjR0DeT3M8TnCPDrDNZET7xO0e0DWfI94ev0G7ljRnwBAany4JtHLcjI9s9LQYolfeM1z3Od9XPEsjhN14vR8PlisYoAz" +
#     "sgIvKLZMSfdMDVY1qpIy94L6YTv5zu7b3XfvveN7s9kDlc15VrIsa91qgAhUP0l3sxVFJz4i4fAESACyAlPQ0sQ0dRzVgilfldTZ/UhhnggYEF/tFWBAmOVqI+uIYwWY" +
#     "1bACTGlpK8Cw1ZiKmKuIe1MMt/zxQ/bclOxW2RzJ5pikN9zjiyLqdhVllMCFFILalmiSJTFst0GgAChPsIlqPfMwINALFCUW1WxsNOqbdZa3bau93qm5OYwsssgii6wx" +
#     "LD8IDBMIECBQBLzTUGunZbc7/v+x6KnO4CBGr+pdZrEsquhUQb9RxWyVsfrBZpNs9+nazMQjQwSLKjpV0G9UMVslwe4jf1+w/73hr1gWVXSqoN+oYraK+n9eCBAgSPzb" +
#     "jtWFAIGu6sreJQQI/keA1YUAgbbqsj9U7wEuEcBK")

HouseBG_3_1 = TTkUtil.base64_deflate_2_obj(
    "eJztW8tu1DAUBTEtUBawYVWQGFWCSqVV6QxhRlPUqnQ9exYsZtogL5Aq8Vgi8eqIRXi7CAnxkCqxop/Amv/gC/gEbMdOHE/SOhM78Qy3t2nmHNsnN9f3Oo7aPqnt/b59" +
    "jH09xvNBbbv3sIfv4HnyHRy/hFFNx4La328HLzE9/fylOSa/+cQnjX5TzJsB8+bgGY78exUy7zCarsC3KXQKnR5iZ9AZs95oxsi6HeVHcOLPx73MTKGtb4zm0bjEBZ3N" +
    "bDlXbjxYsXxInQTW9NVwnevNELv097CSP+EEux+yyayimUTWgFlFZ5byTzH9+SLnfWj6SZT3sYw+K9dhzr4X5PmooZ5gLhpwanjZGcmYw681ouVSrZHI4106z3tvMbpC" +
    "zz/IObL51M/p7DA6rDX982WXYhMmBs3N5xgtMP4CMXpeCDFt28XoqsyxPko/0iM0lVPHKdoDjBaFRyy9vmDmWF10wBgts+ZljbMup3OmNidNlnrDi9xxwQu8wC2LU3Wy" +
    "9AQfT1Y9xhXZDCsoOk1510wLtpSsJJ7FXsJG0fWOtJRROlUdPnFQSzb+dGorJveRNWReHZOw2B9+1Q7q8GutpliHWbrfHclYbx7pm8yGVbJ05Bitxkokk9bQGl8L1okR" +
    "JGmqKoJfS9h6wgSbrRL5w2OyIWltCOORS466lTBVk48i0dkkRlWysiG8xia36JrOPB38YHpr597O/Qf8VbDbHWCTR3ByrtForDRaWAWmr2T78A1FJzsiyfDESAG6AmNw" +
    "FIlp4TiaBWM+K4Wzu6QwjwQciK/1CnAgzHq1UXXEoQLcOqACXDmKVoBjszEWMTcR964abv3th+6+Kd9Q3RypZptkN9yHF0XacBNllMOFAoLWpmiUKXFstQFgABhPsJFq" +
    "vfIwALALDCUW0WxdbzXbTZq3/UZ/ZWs5zGFggQUWWGCdYdlGQCYAAABgCPDdUO9uz+9vifex9K5BtBEjn5rb1DJZULGpAn6Ditsqh+rHi02+1Wfbp6ZuGVJYULGpAn6D" +
    "itsqOVYf/XHx+uexr0wWVGyqgN+g4raK+TcvAAAA5H62Q3UBAGCrugwqjgdb/RxMGnBhVv8/tvp55w/nttdu9q5JXjKPrbDdkkC5dwXsJLGQicBmsWLDxZvCuU4HgfxX" +
    "FMCWxGpOTlnAhZAAC4mYBGIV426HremAfPYaXutGHwNbHqs5OYWBC/cK7CSxZWWuJuBvuNLvjUKXmfvA8nBZAi7cXuk3DRGY4KiVy4ptmkv/+AUAwGQA33+09A9zRLsz")

# Little Cloud
CLOUD_1 = TTkUtil.base64_deflate_2_obj(
    "eJxrYJn6nZkBDGqnaPSwpCSWJE6JnaIBRD2MClN6WD7MX9sFoRqnZLBgQrBUL1jFmn1AFakgnSCxZqzKUbT1T4GrnkxY9XywaihnKoZ6sPA8iFNnwWVTU3vYkvNz8ouK" +
    "ob7y82ub0sOunAYGU9A5fgjeAHHwuA2IweE1uBxMsSeHq58wUtrgSELIODW1VA8Ap3OJ+A==")

CLOUD_2 = TTkUtil.base64_deflate_2_obj(
    "eJxrYJm6kJcBDGqnaPSwpCSWJE6JnaIBRD2MClMyWHpYPsxf2wJk4INgRX14FaWCTAQpayZgFtRE5kfTF+NRCTduKlHG4XV4/xSIeRBbl1JkYAYnxCQkyEeOORimkAUx" +
    "TQF7eDnJXgQFzJIpeByF15MQ3SgOS+1hS87PyS8qhiY2P7+2KSDcw66cBgZTQAII3lDloPqHTAxO7MMsYOgVfiM47AYzByNeU6GFwGhcDToOSpSkIhXW6Hg07mjKwRf0" +
    "fqMhPgAhPprg6Vm8DNMYwKgKsTZjUkv1AO6fDyc=")

# PLANE_FRONT = TTkUtil.base64_deflate_2_obj(
#     "eJztWMtOwkAU1VhBg36BGxMXsjCIUCr9ie5cuqBQMwsTEh9LE6MBTRgNmgsaYzSRxJX8gf6MX+An2HkA0xZLoVRe7YXOPbczc+7cORkazqXa3tocvc4gjqVC7iQH+xA3" +
#     "P3h+HZDkNLzwXb8CtGg3Ei8DijAjqAQoSgxLP6/NOyDNx1fXOYkZJmeHoQEt742NiAn3nkYZbwAtoWU3It+2amcY4tycQSzeJzhYVhzFiTniok9KChjI/b69FZSjAu0O" +
#     "9Qrla1ZZcyuy+1khYQXK/WSTAeVpMLoH1pRZc8EaDFYVDbvQvAS0uSYp1i8BbVoTCYTz3boLL11YSMFKJKdaFdC2YIkB+ADQFnWe2bIewXVPE5xW5uaRkq/FTsTMMHAk" +
#     "XzwsHh3zo0bD0Y0DekEZRg86vhYCArQ+v4b3PTV9uZAupBSYzP5TDYYojz4kEYLxBj5VESph1sAAgpmhX5BJ7+9hsK8pPSbHw10Gt5/0k1xvmYbn2P+CoKUVQBqmryh6" +
#     "yvT7iWpuIFTdrIE/5ZJMKvmCKjwPLtpSnZ7WU/kkzzAEUwwsOrB04WHPoOMLx5eqqHJuh3cdHjD9bCYrqzJMcjTAAk0boOLKqHrKXlYe1dyA+BanpJXsrs6nHy3A5F2C" +
#     "GIxbdPS1GdWGcF9zA44/OozTxC+zQ7ep")
PLANE_FRONT = TTkUtil.base64_deflate_2_obj(
    "eJztWEtOwlAU1VhBg+7AgYkDGRhEKJVuojtwQGnNG5iQ+BmaGA1owtOguaAxRhNIHMkOdDOuwCXY9xH6oVA+tQXaS/vuuX3tue/ekwK9EOrNjQW6nUMSC1rhtAAHkDQ+" +
    "eHETkOBmeOm7cQ1o2W4kXgEUY0ZQGVCcGBZ+3tr3QIaPL9c76waznacFf16TXZcwHQca5b0FtIJWB9ONbet2nokzcB5zOT/BhWvNUa6EI272SZEBAzk+dFpEmarQmdCo" +
    "UtZ2jQ135hzGXy3hBprBs00klK3FSB/ZUGHDJRswWDXmT+l5OehwQxJtXAHatqbjI/O7tS+vrlykhGWSX70GaNdkqRFYAdAOdV7YEp/AQ69TnFzk5pGYr8tOx0zXcaxY" +
    "Oiodn/DHlKJUwLLj+NYh3SAg0PWVCIC9PR523dzW0RogalktI8F0zp9pMEHNdHQS+KIiEGbNUJ0EvogIhA6MoKvJayls3z7zNt/DxWPd0mNyPNzj4s6ZYZIbrOboqRhK" +
    "4LcCfUjD8CVJzRj+MFGlH4jEGYGewFVV6bRU1GTTef+i5v8dalbNFNMQgTkGFpVYpvCwZ9D1e7wGkSVZLOyBr8Dw87m8KIswzdH/qtYMAKq4nKxm7GXlUaUfcLys40qV" +
    "slJ+X4UwAEx+sRCDsEWDr01QDeG+0g843uHoZ6lfIs0vHA==")

#PLANE_BACK = TTkUtil.base64_deflate_2_obj(
#    "eJztWLtu1EAUBbEkHb/ASkuRBhTWG5MtaREyBTWFd9eRC6RIPEokBGRFMbzEjZUOKUHQJAXUIP4lX5BPYF72+jHjRzye2PHs7Hr2zMNzfM7cGduvB/v21hX6eQUbaLBw" +
#    "X7jwBDbwF10dgj9IJnTtdP83sCNGg7NvJx+AZMf/Mm2bSx5mJ6y57q9RloTXJ8brjyZeUk5JVkinWiJOlAWEw3NquiWTEvu+GjpJDYF/Qz8nPnggYJWY/SdfmHJ/G1Mu" +
#    "h92P+KAxfvrFyshFFopfZLkIQKAMLoePpBY+A8fBEUR1wWHYZ8TzWymcztP1+TQj3W6Kr5EQCyi9A8W2Sqf/ezablix7Eyp3GyelBIrJhXQwgbf0+I4e9+hxyfQYJhMn" +
#    "O/Qn9D/bIQQWR7ZuRzpHtvtTcU7OgGLnkbVj9Ll6/CqOS7nH2Nf1nPTEGtwvlphSO2JG/2TZV41bqJxY7GLaQzFndxVQ9R/EarAje+A7ZEbiufNImJwmuWXSQ6miIcvH" +
#    "qSTn58hbeR5am+8+3X32nN/QOc4Scn9ofbRDP4BXoPXR1J5O3LtQXJruyP87KVA4fgd/XlVd1YjcQ8XrKW1kb0jy5IXr1L8nZjRlgnGkKTfa6khJezrtlTZ/tJplgAHq" +
#    "QdlY6cR6piKGJwtrMbbTBAWlVc9Si4LpfNk6a43CFoVY08FnwCUHlZ+FckHp/agTIWSAAeWiB5fZlr19b1YYIRJQdbNpdal436nf1ra3xpaV+55c0KRExxJnKb/rms71" +
#    "O/fEs8xaklhHnBWKrzAXvuhdCKgyT9R5YkDzsdsZkAnQNOAtVbz+NMCAHgPZUyluM7Nm4/km5AJnhQwwoLXA3XG92Vw5qPL+UxBh/OErFzgrdD6A4vezprRGaW0rDFAA" +
#    "6sRciZiU33RKnhfPAxB5HUMS9KW0tmQNgjboo101z3t55z+ESQZp")
PLANE_BACK = TTkUtil.base64_deflate_2_obj(
    "eJztWstu00AUBRHaHb9ApHTRDYjGwSRLtgiZBWsWTuLKC6RKPJZICGjEYniJadQdEkV00y5gDeJf+AI+gXnZsSczjl8zdpObaTw583DOnDN3xnb6snO0M7zEXi/wLupM" +
    "/Wc+foR3yR+63MVhJ53Qlb9HPzE/EtT59+X8HabZ2Z+ltjZSQHgqa66GW4wvZfiBM/xlnaGWXZofakZBFTvGB0dEBMnmZNRS/LYgkSaJcHitSXaCxlzBLxUv55+4mr8t" +
    "qJnB83vy6xNM7SRdfEgS0uXmB1105lihFinH72kt/ogFnp/guG7+NerTE/mOhOVcrs9LONbyunq0lOKcET02Zro2YN7yWTfj2atIzRskGaKymmZEjFB5zY5v2PGQHWdc" +
    "o246CdrdcMA+811IMQFi04ex9vGkCEfqnJ4BJc6jaycPRCgqxnOWy1s+jqozgvYkatwtIjsjecKnwSnPPjeydespJgbYRrIZu7qCdHgvUUP8OsShR2cumWMPlMmzw3Ip" +
    "3deqHPF9KCU9Uy9PqyBAW5ODxwdPnooLTs+b4cw32u7tsxcm69h2b+SOBv4eXl0qdxSfPQms/P41eQdFta5HeHChBvXBCos2pMWw6ckGG2TKGHDJpkNtdSmnZWvnnzXP" +
    "rBoIAIABUCF+LsS6V0dcD6bOtO/KBBWlRc9SiQJ0XrfOJWLWdKy2KBBNhygAAMpYK3yXlgly73YXIvQAADAMovAjZa7jDu+MV4aYBhTd5Vpdqt7wqrd13dt9x8n8SUHR" +
    "JEfHHGfJv91D5+qdN8Sz+hej1ELkLVByiWqcaCOgyERrkalrDUD9YmApwmUgWtbxzBgAAADFQMYNOWk3dsb9yS2cCbwFAgCgtcDf94PxxAjIw6DEE2ZFQIq7zEzgLVA5" +
    "gJLX3VBaobSyFQDMgpK//ZSIXP0VsObutwxA9OkUTXhTSitLZhC0QR/7qqn+BSJ4fvM/ZnQSZQ==")

#PLANE_BODY_1 = TTkUtil.base64_deflate_2_obj(
#    "eJztWUtOwzAQBVGK6AVgWQkJWCFIQqAcojcAqaVBLJAq8VkisYFVQCCmfFYgCmLFpTgBRyB2nMR2nbT5tU07nabOm3jsl/k4VnNV6hxoM/RzCet2qdU4b8A+rDtfe7YK" +
#    "x6VA7Lnf5w9Bk62Q8bvC+JbDgp3P5zevIGVh7nmH05N3z+Tc51dh7aLUVtTXHVu4BfL7AMp+8ngeLkt+SOdfAMrhJX4Uy9lwSCbu3IT5HeV/D+x+/Nh4/lL16ari5/l5" +
#    "mbVLQR9/zAidHx+J31OEf/tdz0JIDX3CyGJVdX1BWHz13GNk/Fb9PkGM1tQtGcHmxunpJ9ZQ1UW+T1ZkTmliQiw71P41hn0QH7v09/YDOS6qnFRVBKhs5jszvcn3sJWd" +
#    "I0H8eA3HhtN2nNhuK8VIQEFTadVVQsl2gTbfbvPIU/fI7UkSTssQeimpUDqWXT5sn7RPz9jzt16/gbDDXlg5oh8gigAhQJAciFkVclhSamIqIhh3EJnYdMfCd3CA0dJb" +
#    "mgnJpkLjIhvHHXLc+BfBmJ3LT5WRrxMIhlw8CAauFKwQBAgC0FMP2axIqVawHIyLzh+NJ814tPU5xGdvgdgiKCoIznGPh2AqgVACyn/khsjENLc1XZcXfYU27iipKKDx" +
#    "JMdseBu5nlJTvdXJsfSyCRaCxN6f3j0tvspEUEwQumiH5TGXz029qR1uevnMEAIEeQAx32ImK5e0NbNmNLa8pGXI3Sbo5u5OE1CbTltHkB6IiTrg0S/7uSpgcYsE9QAl" +
#    "AzbZ/BGBadGmdlmOYBz8E6rlsi7mYVkXG//Bmgmk")
PLANE_BODY_1 = TTkUtil.base64_deflate_2_obj(
    "eJztWstu00AUBRFSUCI1P9AKCSmkUkEQBzcJG74gf9BFHq6yqBQJ6BKJDaxMBeImLatWCYgVP9Uv6CfUM37MI2PHz8Rubm6S8ZmZOz5zH+NJ7C+l6Yv2A/r6DA2zNOp/" +
    "6sMxNKy3+fAZjEtqMR/dXMx9W8MJGWMROIZhsVC2PHb0Z57+E7EkbXO5zT16qtQph+WQxtyj2YXjUMnuvIJUhXNXeHsKdq855a5U1tTtli58B/L9E5T95PFcXJXskMy+" +
    "AJTDZXQvVtPhEE/scxPm55T/D3Dmw2K9xuYo91mo/Ofaed8p91gfb8yAOs8/Er9ZgH1XtachJIf+wMZ8VbdtQVj8XZpjoP8OvT7MRy/VJRnB5MZZ6ifmUN1Gnk0OZE5J" +
    "fEI0p1T/dwR95h+zdHv1HzJcVDmpqwhQ0bM9M53ktd/KzpEgdvwK465VTi3fvlNKNwaFtqpWnSWU7AJo8c8ufvHUXXLvJfGn1RV6KalQOoZZHk5OJx8+OvuQXu8bRP2Y" +
    "O89P6AtIBUMI8gFE/8T8GBGCI2RAWMetkTZq6hBvUlunnGik4sw5dryuilFcqBBsaHmVQxNDEUHeQWBg059cfIfiXF9QOX3lqEPmjX8RlJ1j+aqy8XUCwZqTB0HoTMEM" +
    "QYCAgaV8SGdFSrSCZaBcdP6ofN+UN5ufa7z2FogtgqICdox7PARbCYQUUP4jt0Ymuv62qWnyoq+ojTpKIgqofJ99loMbkvxdnQxTLx1nIYht/e3d0+KtTATFBL6L9qqn" +
    "RSzFgTZoDl+78ewgBAiyAGK8xX+0qaN3Wv03btA6yN4maHr7aABYm6y2hyA5EAM15YdPmd8CQY+heMAkmz8isC21iU2WIciDfXxruaiL+jSrcfbqDu+vJqo=")


# Glyphs:
# 🍝🍜🔑🗝️🪪💳📓🎁📔📒📕📗📘📙
# 📀💿💾💽🥇🥈🥉🏅🎖️🗃️
# 🔫🪃🎣🏹🧨💣🪓🚬🪦🚀
#
# 🐍🐔🧌🧛🧑‍✈️😈🤖👾👽💀👻💩👹👿👺🎃🕺
# 🐯🦁🫎🐌
# 🐌🦖🦕🦂🕷️🪳🪲🪰🐜🐊🦈🦀🪼🦑🐙🐲🐉🔥☄️💥⚡⭐🌟❄️🌪️
#
# 🔋🛢️🚽
# 🩷❤️🧡💛💚🩵💙💜🖤🩶🤍🤎💔❤️‍🔥❤️‍🩹💝💘💖💗💟☮️
# ⚪⚫🔴🔵🟤🟣🟢🟡🟠
# ♠️♣️♥️♦️
# 🔱⚜️

# Snake:    🐍
# Enemies:  🕺🧟🧌🧛😈🤖👾👽💀👻💩👹👿👺🎃 🦖🦕 🐲🐉
#
# Armor:
# - Boots:  👢🧦👠🥿🩴🥾👟👞🩰 - 🛼⛸️
# - Head:   🪖⛑️🎓👒🧢🎩 - 🤿👓🕶️🥽
# - Body:   🎽🩱👙👗👘🥻👔👕👚🦺🥼🧥🥋
# - Legs:   🩳🩲👖
# - Shield: 🛡️
#
# Weapon:
# - Melee:  🥊🪈🪥🪓🔪🗡️🥄🥢🏓📎🧹 - 👊🤌
# - Ranged: 🏹🔫❤️‍🔥💜🎺🪄
# - Shells: ⚪⚫🔴🟣🐚🌟
# - Throw:  🪃🧨💣🥌
#
# Gold: 💵💴💶💷🪙💰👛💎
#
# Food: 🥘🥗🫔🌯🌮🥙🥪🍕🍟🍰🥧🍡🥮🥠🍥☕🍺🍻🥃🍷🍸🍹🍖🍗🧇🥞🥦🍔🍙🍯

TEST_TILES = """
        # Snake:    🐍
        # Enemies:  🕺🧟🧌🧛😈🤖👾👽💀👻💩👹👿👺🎃 🦖🦕 🐲🐉
        #
        # Armor:
        # - Boots:  👢🧦👠🥿🩴🥾👟👞🩰 - 🛼⛸️
        # - Head:   🪖⛑️🎓👒🧢🎩 - 🤿👓🕶️🥽
        # - Body:   🎽🩱👙👗👘🥻👔👕👚🦺🥼🧥🥋
        # - Legs:   🩳🩲👖
        # - Shield: 🛡️
        #
        # Weapon:
        # - Melee:  🥊🪈🪥🪓🔪🗡️🥄🥢🏓📎🧹 - 👊🤌
        # - Ranged: 🏹🔫❤️‍🔥💜🎺🪄 - 💔
        # - Shells: ⚪⚫🔴🟣🐚🌟
        # - Throw:  🪃🧨💣🥌
        #
        # Gold: 💵💴💶💷🪙💰👛💎
        #
        # Food: 🥘🥗🫔🌯🌮🥙🥪🍕🍟🍰🥧🍡🥮🥠🍥☕🍺🍻🥃🍷🍸🍹🍖🍗🧇🥞🥦🍔🍙🍯
        #
        # Stuff: 🟰✖️➗➖➕❌🔆🔅 💊🧪🛡️ 🥦⚗️ 🚽
        """

Tiles = {
    None  : TTkString(''),
    ''  : TTkString(''),
    '#' : TTkString('🧱'), # wall
    ' ' : TTkString('  '),
    '@' : TTkString('😎'),
    'X' : None,
    'D' : TTkString('🚪'),
    'DR' : TTkString('🚪',TTkColor.bg('#FF0000')),
    'DG' : TTkString('🚪',TTkColor.bg('#00FF00')),
    'DB' : TTkString('🚪',TTkColor.bg('#0000FF')),
    'DY' : TTkString('🚪',TTkColor.bg('#FFFF00')),
    'KR' : TTkString('📕'),
    'KG' : TTkString('📗'),
    'KB' : TTkString('📘'),
    'KY' : TTkString('📒'),
    'd' : TTkString('| ',TTkColor.fg('#803000')),
    'Snake'    : TTkString('🐍'),
    'Zombie'   : TTkString('🧟'),
    'Dragon1'  : TTkString('🐲'),
    'Dragon2'  : TTkString('🐉'),
    'TRex'     : TTkString('🦖'),
    'Dino'     : TTkString('🦕'),
    'Dancer'   : TTkString('🕺'),
    # 'Zombie'   : TTkString('🧟'),
    # 'Ogre'     : TTkString('🧌'),
    'Vampire'  : TTkString('🧛'),
    'Imp'      : TTkString('😈'),
    'Robot'    : TTkString('🤖'),
    'SI'       : TTkString('👾'),
    'Alien'    : TTkString('👽'),
    'Skeleton' : TTkString('💀'),
    'Ghost'    : TTkString('👻'),
    'Crap'     : TTkString('💩'),
    'Daemon'   : TTkString('👹'),
    'Nose'     : TTkString('👺'),
    'Pumpkin'  : TTkString('🎃'),
    # Armors
    'af1' : TTkString('👢'),
    'af2' : TTkString('🧦'),
    'af3' : TTkString('👠'),
    'af4' : TTkString('🥿'),
    'af5' : TTkString('🩴'),
    'ah1' : TTkString('🪖'),
    'ah2' : TTkString('⛑️'),
    'ah3' : TTkString('🎓'),
    'ah4' : TTkString('👒'),
    'ah5' : TTkString('🧢'),
    'ab1' : TTkString('🎽'),
    'ab2' : TTkString('🩱'),
    'ab3' : TTkString('👙'),
    'ab4' : TTkString('👗'),
    'ab5' : TTkString('👘'),
    'al1' : TTkString('🩳'),
    'al2' : TTkString('🩲'),
    'al3' : TTkString('👖'),
    # Weapons
    'wm1':TTkString('🥊'),
    'wm2':TTkString('🪈'),
    'wm3':TTkString('🪥'),
    'wm4':TTkString('🪓'),
    'wr1':TTkString('🏹'),
    'wr2':TTkString('🔫'),
    'wr3':TTkString('💜'),
    'wr4':TTkString('💔'),
    'ws1':TTkString('🌟'),
    'ws2':TTkString('⚫'),
    'ws3':TTkString('🟣'),
    'ws4':TTkString('🔴'),
    'wt1':TTkString('🥌'),
    'wt2':TTkString('🧨'),
    'wt3':TTkString('💣'),
    'wt4':TTkString('🚽'),
    # Gold
    'g1':TTkString('💵'),
    'g2':TTkString('💴'),
    'g3':TTkString('💶'),
    'g4':TTkString('💷'),
    'g5':TTkString('🪙'),
    'g6':TTkString('👛'),
    'g7':TTkString('💰'),
    'g8':TTkString('💎'),

    'b' : TTkString('🗃️'), # Black Box
    # Exit
    '>' : TTkString('🪜'),
}