import lexer
from variables import VAR_STACK
import tclcmds

# current execution nesting level
exec_level = 0

# process a chunk
def process_word(word, t_vars):
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
    
    return runTCLcmds(cmd_to_run, t_vars)
  else:
    raise SystemExit(f"can't handle type {word}")

def runTCLcmds(t_code, t_vars):
  parsed_tcl = lexer.lextcl(t_code)
  
  # return the last result
  last_result = None
  
  for cmd in parsed_tcl:
    cmd = [process_word(c, vs) for c in cmd]
    # command parse tree now begins here
    if cmd[0] == 'set': # set command
      last_result = tclcmds.t_set(cmd, vs, exec_level)
    elif cmd[0] == 'puts': # put command
      last_result = tclcmds.t_puts(cmd)
    print(cmd)
  return last_result
  
# read in tcl code from a file
tcl_code = ''
with open('tclcode.txt', 'r') as file:
  tcl_code = file.read()

# initialize a new variable stack
vs = VAR_STACK()
vs.new_instance()

# run the tclcode
runTCLcmds(tcl_code, vs)


#vs._dpa()