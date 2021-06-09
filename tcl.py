import tclparse
import tclstate

p = tclparse.TCLParse('''proc test {x {y 10}} {
  puts $x
}

test 99
''')

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

# ARGS = WORD, { WHITESPACE, ('{', WORD, WORD, '}') | WORD } ;
def parseArguments(args):
  split_args = args.split(' ')
  parsed_args = []
  for i, s in enumerate(split_args):
    if '{' in s:
      left = s;
      right = split_args[i + 1]
      left = left[1:]
      right = right[:-1]
      parsed_args.append({'VAR': left, 'DEFAULT': right})
    elif '}' not in s:
      parsed_args.append(s)
  return parsed_args

def runFuncByName(name, state, inargs):
  funcStuff = state.getProc(name)
  args = funcStuff['args']
  pargs = parseArguments(args)
  body = funcStuff['body']
  newstate = tclstate.TCLState()
  p2 = tclparse.TCLParse(body)
  parsed2 = p2.PROGRAM()
  
  min_len = len([z for z in pargs if 'DEFAULT' not in z])
  assert len(inargs) >= min_len
  assert len(inargs) <= len(pargs)
  
  for i, z in enumerate(pargs):
    if type(z) is dict and i >= len(inargs):
      newstate.setVar(z['VAR'], z['DEFAULT'])
    elif type(z) is dict:
      newstate.setVar(z['VAR'], inargs[i])
    else:
      newstate.setVar(z, inargs[i])
  
  for c in parsed2:
    runCmd(c, newstate)
  
  #print(parsed2)

def F_PROC(cmd, state):
  assert cmd[0]['WORD'] == 'proc'
  
  fname = cmd[1]['WORD']
  fargs = cmd[2]['WORD']
  fbody = cmd[3]['WORD']
  
  state.setProc(fname, {'args': fargs, 'body': fbody})
  
  #runFuncByName('test', state, 14, 6)

def toArgList(st):
  build = ''
  for c in st:
    build += c['WORD'] + ' '
  build = build.split(' ')
  build = build[:-1]
  return build
  #print(build)

def runCmd(cmd, state):
  subcmd(cmd, state)
  
  #print(cmd)

  if state.hasProc(cmd[0]['WORD']):
    runFuncByName(cmd[0]['WORD'], state, toArgList(cmd[1:]))
  elif cmd[0]['WORD'] == 'set':
    F_SET(cmd, state)
  elif cmd[0]['WORD'] == 'puts':
    F_PUTS(cmd, state)
  elif cmd[0]['WORD'] == 'proc':
    F_PROC(cmd, state)
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