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
  elif 'VAR_SUB' in word: # the variable substitution
    # try substitution here
    return t_vars.get_variable(word['VAR_SUB'][1:], exec_level)
  else:
    raise SystemExit(f"can't handle type {word}")

# read in tcl code from a file
tcl_code = ''
with open('tclcode.txt', 'r') as file:
  tcl_code = file.read()

# now break it all into commands with the tcl parsing rules

parsed_tcl = lexer.lextcl(tcl_code)

# initialize a new variable stack
vs = VAR_STACK()
vs.new_instance()

for cmd in parsed_tcl:
  cmd = [process_word(c, vs) for c in cmd]
  # command parse tree now begins here
  if cmd[0] == 'set': # set command
    tclcmds.t_set(cmd, vs, exec_level)
  elif cmd[0] == 'put': # put command
  print(cmd)


#vs._dpa()

# now try to run some tcl code

#vs.set_variable('hello', '20', 0)
#print(vs.get_variable('hello', 0))

#print(parsed_tcl)