
# shared variable stack
class VAR_STACK:
  
  def __init__(self):
    self.V_STACK = []
  
  # create a new layer for var stack
  def new_instance(self):
    self.V_STACK.append({})
  
  # remove the most recent instance
  def drop_instance(self):
    self.V_STACK.pop()
  
  # set a variable at a particular level
  def set_variable(self, name, value, level):
    self.V_STACK[level][name] = value
  
  # get a variable at a particular level
  def get_variable(self, name, level):
    return self.V_STACK[level][name]
  
  # debug print all variables
  def _dpa(self):
    [print(v) for v in self.V_STACK]

# shared user defined process stack
class PROC_STACK(VAR_STACK):
  
  # set a variable at a particular level
  def set_process(self, name, value, level):
    self.V_STACK[level][name] = value
  
  # get a variable at a particular level
  def get_process(self, name, level):
    return self.V_STACK[level][name]
  
  # returns if a process exists
  # True is yes, False is no
  def has_process(self, name, level):
    return name in self.V_STACK[level]