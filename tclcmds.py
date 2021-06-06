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