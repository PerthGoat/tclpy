import tclparse
import tclstate

p = tclparse.TCLParse('''set x 10
set y "40 $x"
puts $y''')

parsed = p.PROGRAM()

mainstate = tclstate.TCLState()

def F_SET(cmd, state):
  assert cmd[0]['WORD'] == 'set'
  assert len(cmd) >= 2
  if len(cmd) == 2:
    return state.getVar(cmd[1]['WORD'])
  
  return state.setVar(cmd[1]['WORD'], cmd[2]['WORD'])

def subcmd(cmd, state):
  for i, c in enumerate(cmd):
    if 'VAREXP' in c:
      cmd[i] = {'WORD': state.getVar(c['VAREXP'])}
    elif 'QUOTE' in c:
      final_val = ''
      for q in c['QUOTE']:
        if 'QUOTE_STR' in q:
          final_val += q['QUOTE_STR']
        elif 'VAREXP' in q:
          final_val += state.getVar(q['VAREXP'])
        else:
          print('passed unknown quote val')
      cmd[i] = {'WORD': final_val}

def F_PUTS(cmd, state):
  assert cmd[0]['WORD'] == 'puts'
  print(cmd[1]['WORD'])

def runCmd(cmd, state):
  subcmd(cmd, state)
  
  print(cmd)

  if cmd[0]['WORD'] == 'set':
    F_SET(cmd, state)
  elif cmd[0]['WORD'] == 'puts':
    F_PUTS(cmd, state)
  else:
    print(f"unknown command {cmd}")
  #print(cmd)

for cmd in parsed:
  proc_name = cmd[0]
  if 'WORD' in proc_name:
    runCmd(cmd, mainstate)
  elif 'VAREXP' in proc_name:
    pass
  else:
    print('command must start with a word or variable expansion')

#print(mainstate.getVar('y'))
#print(parsed)