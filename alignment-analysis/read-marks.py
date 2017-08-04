# encoding: utf-8

# code python3
"""
exec(open('read-marks.py').read())
"""

import re

name = "../logs/log.log"

encoding = 'latin-1'
with open(name, 'r', encoding=encoding) as f:
    _lines = f.readlines()

lines = list(map(lambda l: l.strip('\n'), _lines))

lbae = []
for i,l in enumerate(lines):
    if l.startswith('Layout Cell '):
        lbae.append((i,'B'))
    elif l.startswith('Elapsed time for pattern '):
        lbae.append((i,'E'))
    elif re.match(r'Markers[ \t]*:[ \t]*expected[ \t]+observed', l) != None:
        lbae.append((i,'A'))
       
def readAblock(lines, i):
    if re.match(r'Markers[ \t]*:[ \t]*expected[ \t]+observed', lines[i]) == None:
        raise Exception('bad Ablock Markers line at ' + str(i+1))
    if re.match(r'[ \t]*X \[mm\][ \t]*Y \[mm\][ \t]*X \[mm\][ \t]*Y \[mm\]', lines[i+1]) == None:
        raise Exception('bad Ablock XYXY line at ' + str(i+2))
    ret = []
    ok = True
    ii = i+1
    while(ok):
        ii += 1
        try:
            m = re.match(r'[ \t]*([0-9]+)[ \t]*:[ \t]*([^ \t]+)[ \t]*,[ \t]*([^ \t]+)[ \t]+([^ \t]+)[ \t]*,[ \t]*([^ \t]+)', lines[ii])
            ieo = int(m.groups()[0])
            xe = float(m.groups()[1])
            ye = float(m.groups()[2])
            xo = float(m.groups()[3])    
            yo = float(m.groups()[4])
            ret.append((ieo, xe, ye, xo, yo))
        except:
            ok = False
    return ret

for b in lbae:
    if b[1] == 'A':
        r = readAblock(lines, b[0])
        print(str(b[0]+1) + '\t' + '\t'.join(list(map(lambda x:'\t'.join(map(str,x)), r))))



