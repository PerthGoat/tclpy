class TCLState:
  def __init__(self):
    self.variables = {}
    self.procedures = {}
  
  def setVar(self, name, value):
    self.variables[name] = value
  def getVar(self, name):
    return self.variables[name]
  def setProc(self, name, value):
    self.procedures[name] = value
  def getProc(self, name):
    return self.procedures[name]
  def hasProc(self, name):
    return name in self.procedures