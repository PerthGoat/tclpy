import tclparse

p = tclparse.TCLParse('''set x 10
set y 40
puts $y''')

parsed = p.PROGRAM()

for cmd in parsed:
  print(cmd)

#print(parsed)