import tclparse
import tclstate

p = tclparse.TCLParse('''proc test {x} {
  return [expr 10 $x +]
}

set x 0

for {set x 0} {10 $x <} {incr x} {
  puts $x
}
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
    elif 'COMEXP' in c:
      funcbody = c['COMEXP']
      cmd[i] = runCmd(funcbody, state)
  #print(cmd)
def F_PUTS(cmd, state):
  assert cmd[0]['WORD'] == 'puts'
  print(cmd[1]['WORD'])

# ARGS = WORD, { WHITESPACE, ('{', WORD, WORD, '}') | WORD } ;
def parseArguments(args):
  if args == '':
    return []
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
  
  lastrun = ''
  for c in parsed2:
    lastrun = runCmd(c, newstate)
  
  return lastrun
  #print(parsed2)

def F_PROC(cmd, state):
  assert cmd[0]['WORD'] == 'proc'
  
  fname = cmd[1]['WORD']
  fargs = cmd[2]['WORD']
  fbody = cmd[3]['WORD']
  
  state.setProc(fname, {'args': fargs, 'body': fbody})
  
  #runFuncByName('test', state, 14, 6)

def isFloat(str):
  try:
    float(str)
    return True
  except ValueError:
    return False

def F_EXPR(cmd, state):
  assert cmd[0]['WORD'] == 'expr'
  
  math_stack = []
  
  for c in cmd[1:]:
    if c['WORD'].isnumeric() or isFloat(c['WORD']):
      math_stack.append(float(c['WORD']))
    else:
      if c['WORD'] == '+':
        math_stack[-2] = math_stack[-1] + math_stack[-2]
        math_stack = math_stack[:-1]
      elif c['WORD'] == '>':
        math_stack[-2] = math_stack[-1] > math_stack[-2]
        math_stack = math_stack[:-1]
      elif c['WORD'] == '<':
        math_stack[-2] = math_stack[-1] < math_stack[-2]
        math_stack = math_stack[:-1]
      else:
        print(f'unknown op {c}')
  
  return {'WORD': str(math_stack[0])}

def F_FOR(cmd, state):
  assert cmd[0]['WORD'] == 'for'
  set_val = cmd[1]['WORD']
  test = cmd[2]['WORD']
  nxt = cmd[3]['WORD']
  body = cmd[4]['WORD']
  
  test_statement_setup = 'if {' + test + '} {' + body + f'\n{nxt} ' + '}'
  
  if_val = tclparse.TCLParse(test_statement_setup).PROGRAM()[0]
  while(F_IF(if_val, state)):
    pass
    #print('hi')
  
  #print(test_statement_setup)
  
  
  #print(state.getVar('x'))
  #print(test)
  
  #runCmd(set_val, state)

def F_IF(cmd, state):
  assert cmd[0]['WORD'] == 'if'
  test_val = cmd[1]['WORD']
  body = cmd[2]['WORD']
  
  full_cmd = 'expr ' + test_val
  
  f_cmd = tclparse.TCLParse(full_cmd).PROGRAM()[0]
  
  subcmd(f_cmd, state)
  
  expr_result = F_EXPR(f_cmd, state)['WORD'] == 'True'
  
  body = tclparse.TCLParse(body).PROGRAM()
  
  if expr_result:
    for cmd in body:
      runCmd(cmd, state)
  
  return expr_result
  #if(expr_result):
    
  
  #raise SystemExit('a')

def F_INCR(cmd, state):
  assert cmd[0]['WORD'] == 'incr'
  state.setVar(cmd[1]['WORD'], str(int(state.getVar(cmd[1]['WORD'])) + 1))
def toArgList(st):
  build = ''
  for c in st:
    build += c['WORD'] + ' '
  build = build.split(' ')
  build = build[:-1]
  return build
  #print(build)

def runCmd(cmd, state):
  #print(cmd)
  subcmd(cmd, state)
  #print(f'result: {cmd}')
  if state.hasProc(cmd[0]['WORD']):
    return runFuncByName(cmd[0]['WORD'], state, toArgList(cmd[1:]))
  elif cmd[0]['WORD'] == 'set':
    F_SET(cmd, state)
  elif cmd[0]['WORD'] == 'puts':
    F_PUTS(cmd, state)
  elif cmd[0]['WORD'] == 'proc':
    F_PROC(cmd, state)
  elif cmd[0]['WORD'] == 'expr':
    return F_EXPR(cmd, state)
  elif cmd[0]['WORD'] == 'return':
    return cmd[1]
  elif cmd[0]['WORD'] == 'for':
    F_FOR(cmd, state)
    #raise SystemExit('for')
  elif cmd[0]['WORD'] == 'if':
    F_IF(cmd, state)
  elif cmd[0]['WORD'] == 'incr':
    F_INCR(cmd, state)
  else:
    print(f"unknown command {cmd}")
  #print(cmd)


#print(parsed)

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