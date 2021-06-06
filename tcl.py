import lexer
from variables import VAR_STACK, PROC_STACK

# command functions

def t_set(cmd, t_vars, scope):
  # make sure passed a set
  assert cmd[0] == 'set'
  
  # make sure arguments less than or equal to 2, but greater than 0
  arguments = len(cmd) - 1
  
  assert arguments <= 2 and arguments != 0
  
  name = cmd[1]
  if len(cmd) == 3:
    val = cmd[2]
    t_vars.set_variable(name, val, scope)
  
  return t_vars.get_variable(name, scope)

def t_puts(cmd):
  assert cmd[0] == 'puts'
  assert len(cmd) > 1
  print(' '.join(cmd[1:]))

def t_userproc(cmd, t_vars, t_proc, scope):
  assert cmd[0] == 'proc'
  assert len(cmd) == 4
  
  name = cmd[1]
  args = cmd[2][1:-1].strip()
  body = cmd[3][1:-1].replace('\t', '').strip()
  t_proc.set_process(name, [args, body], scope)
  #t_proc._dpa()

def t_runprocess(cmd, t_vars, t_proc, scope):
  given_args = len(cmd) - 1
  user_cmd = t_proc.get_process(cmd[0], scope)
  var_set = user_cmd[0]
  parsed_args = lexer.lextcl(var_set)[0]
  
  needed_arg_len = len([p for p in parsed_args if 'WORD' in p])
  
  assert given_args == needed_arg_len or given_args == len(parsed_args)
  
  t_vars.new_instance()
  t_proc.new_instance()
  
  scope += 1
  
  it = 0
  
  for v in parsed_args:
    if 'WORD' in v:
      name = v['WORD']
      val = cmd[1 + it]
      
      t_vars.set_variable(name, val, scope)
      
      it += 1
    if 'SAFE_BRACES' in v:
      dec = v['SAFE_BRACES'][1:-1]
      spl = dec.split(' ')
      name = spl[0]
      val = spl[1]
      if it < given_args:
        val = cmd[1 + it]
        it += 1
      t_vars.set_variable(name, val, scope)
  return runTCLcmds(user_cmd[1], t_vars, t_proc, scope)
  

# current execution nesting level
e_level = 0

# process a chunk
def process_word(word, t_vars, t_proc, exec_level):
  # the most traditional of words
  # return with no special stuff
  if 'WORD' in word:
    return word['WORD']
  elif 'SAFE_BRACES' in word: # place where no subs occur
    return word['SAFE_BRACES']
  elif 'VAR_SUB' in word: # the variable substitution
    # try substitution here
    return t_vars.get_variable(word['VAR_SUB'][1:], exec_level)
  elif 'QUOTED_WORD' in word: # in this case I need to do some tricky lexing
    orig_word = word['QUOTED_WORD'][1:-1]
    degraded = lexer.lextcl(word['QUOTED_WORD'][1:-1])[0] # downgrade out of the quotes using the lexer
    for d in degraded: # and so any subs needed
      if 'VAR_SUB' in d:
        orig_word = orig_word.replace(d['VAR_SUB'], process_word(d, t_vars))
    return orig_word
  elif 'COMMAND_SUB' in word:
    cmd_to_run = word['COMMAND_SUB'][1:-1]
    
    return runTCLcmds(cmd_to_run, t_vars, t_proc, exec_level)
  else:
    raise SystemExit(f"can't handle type {word}")

def runTCLcmds(t_code, t_vars, t_proc, exec_level):
  parsed_tcl = lexer.lextcl(t_code)
  # return the last result
  last_result = None
  
  for cmd in parsed_tcl:
    cmd = [process_word(c, t_vars, t_proc, exec_level) for c in cmd]
    # command parse tree now begins here
    if cmd[0] == 'set': # set command
      last_result = t_set(cmd, t_vars, exec_level)
    elif cmd[0] == 'puts': # put command
      last_result = t_puts(cmd)
    elif cmd[0] == 'proc': # proc command
      last_result = t_userproc(cmd, t_vars, t_proc, exec_level)
    elif cmd[0] == 'return': # immediately return the value
      return cmd[1]
    elif t_proc.has_process(cmd[0], exec_level): # try user defined procedures before failing out
      last_result = t_runprocess(cmd, t_vars, t_proc, exec_level)
    else:
      raise SystemExit(f"unknown command {cmd}")
    #print(cmd)
  
  t_vars.drop_instance()
  t_proc.drop_instance()
  return last_result
  
# read in tcl code from a file
tcl_code = ''
with open('tclcode.txt', 'r') as file:
  tcl_code = file.read()

# initialize a new variable stack
vs = VAR_STACK()
vs.new_instance()
# initialize a new user-defined process stack
ps = PROC_STACK()
ps.new_instance()

# run the tclcode
runTCLcmds(tcl_code, vs, ps, e_level)