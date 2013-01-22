#!/usr/bin/env python

import sys
o = sys.stdout

# Things will break if Ctl isn't last (fixable if necessary)
layers = ["TX", "RX", "FW", "Ctl"]

start = "L"
events = (
        ( 0 , "TX" , "H"),
        ( 4 , "TX" , "L"),
        ( 6 , "TX" , "H"),
        (10 , "RX" , "L"),
        (12 ,"Ctl" , "H"),
        )
end = "H"
end_CLK = 15

##############################################################

def double(T):
    'double() - return a tuple with each tuple element (e) doubled.'
    return tuple( [ int( e * 2 ) for e in T ] )

def process(l, adj):
    cur = start

    starts = zip(*events)[0]
    starts = double(starts)

    ends = list(starts[1:])
    ends.append((end_CLK+1)*2)
    for t0,t1 in zip(starts,ends):
        e = events[starts.index(t0)]
        offset = (layers.index(l) - layers.index(e[1])) % len(layers)
        if offset == 0:
            if adj:
                d = (len(layers) * 2 - adj) * .2
            else:
                d = 0
        else:
            d = (offset * 2 - adj ) * .2

        o.write("%1.1f%s" % (d, cur))
        o.write("%d{2%s}" % (t1-t0-1, e[2]))
        o.write("%1.1f%s" % (2-d, e[2]))
        cur = e[2]

def process_din(l):
    process(l, 1)

def process_dout(l):
    process(l, 0)

o.write('\\begin{figure}[!h]\n')
o.write('  \\begin{center}\n')
o.write('    \\small\n')
o.write('    \\begin{tikztimingtable}\n')

for l in layers:
    o.write('      Din  & ')
    o.write(start)
    process_din(l)
    o.write(end)
    o.write(' \\\\\n')
    #
    o.write('      Dout & ')
    o.write(start)
    process_dout(l)
    o.write(end)
    o.write(' \\\\\n')
    #
    if l != "Ctl":
        o.write('      \\\\\n')

o.write('      CLK  & C')
o.write(str(2*end_CLK+1)+'{2C}')
o.write('{2'+end+'}'+end)
o.write(' \\\\\n')

o.write('''\
      \\extracode
        \\begin{pgfonlayer}{background}
          \\begin{scope}[semitransparent,semithick,dashed]
            \\vertlines{1,5,...,65}
          \\end{scope}
        \\end{pgfonlayer}
        \\begin{scope}
          [font=\\sffamily\\large,shift={(-3.0em,-0.5)},anchor=east]
''')
depth = 0
for l in layers:
    if l == "Ctl":
        depth -= 1
    o.write('          \\node at (0, %d) {%s};\n' % (depth, l))
    depth -= 6
o.write('''\
        \\end{scope}
        \\begin{scope}
          [font=\sc\\footnotesize,anchor=north,shift={(0,3em)}]
''')
STATES = ("Drive1", "Latch1", "Drive2", "Latch2")
idx = 0
for t in xrange(1, end_CLK*4, 4):
    o.write('          \\node [rotate=45] at (%d, 0) {%s};\n' % (t, STATES[idx]))
    idx = (idx + 1) % 4
o.write('''\
        \\end{scope}
    \\end{tikztimingtable}
  \\end{center}
\\end{figure}
''')
