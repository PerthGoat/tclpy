TCL_TYPES = {
  '[': 'COMMAND_SUB',
  '"': 'QUOTED_WORD',
  '{': 'SAFE_BRACES',
  '$': 'VAR_SUB'
}

def lextcl(tcl_code):
  # different characters that can cause nesting and their ending pairs
  nestchars = {'{':'}', '"':'"', '[':']'}

  # holds the array of separated commands
  command_list = []

  # in a nest and on what char
  nesting = 0
  nestchar = ''

  # stringbuffer
  sb = ''

  # holds the command and if inside a comment or not
  command = []
  comment = False

  # goes thru
  for c in tcl_code:
    if len(command) == 0 and c == '#':
      comment = True
      continue
      
    if (c == '\n' or c == ';') and nesting == 0:
      if sb != '':
        command.append(sb)
      command_list.append(command)
      sb = ''
      command = []
      comment = False
    elif not comment:
      if c == ' ' and nesting == 0:
        if sb != '':
          command.append(sb)
          sb = ''
      else:
        if c in nestchars and nestchar == '':
          nestchar = c
          if c == '"':
            nesting = 2
        if nestchar != '':
          if nestchar != '"':
            if c == nestchar:
              nesting += 1
            if c == nestchars[nestchar]:
              nesting -= 1
          else: # quotes are a special case because the character is the same
            if c == nestchar:
              nesting -= 1
        if(nesting == 0):
          nestchar = ''
        sb += c

  command.append(sb)
  command_list.append(command)

  # next remove empty commands
  command_list = [cmd for cmd in command_list if len(cmd) > 0]
  
  firstpass = command_list
  second_pass = []

  for i, p in enumerate(firstpass):
    second_pass.append([])
    for c in p:
      t_type = 'WORD'
      if c[0] in TCL_TYPES:
        t_type = TCL_TYPES[c[0]]
      
      second_pass[i].append({t_type : c})
  
  return second_pass

