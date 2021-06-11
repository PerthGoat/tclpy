class TCLState:
  def __init__(self, proccopy=None): # optionally copy procedures to new state to make global setup
    self.variables = {}
    if proccopy == None:
      self.procedures = {}
    else:
      self.procedures = proccopy.procedures
  
  def setVar(self, name, value):
    if type(name) == dict:
      if name['name'] not in self.variables:
        self.variables[name['name']] = {}
      
      if 'WORD' in name['index']:
        name['index'] = name['index']['WORD']
      if 'VAREXP' in name['index']:
        name['index'] = self.getVar(name['index']['VAREXP'])
        
      self.variables[name['name']][name['index']] = value
    else:
      self.variables[name] = value
  def getVar(self, name):
    if type(name) == dict:
      if 'WORD' in name['index']:
        name['index'] = name['index']['WORD']
      if 'VAREXP' in name['index']:
        name['index'] = self.getVar(name['index']['VAREXP'])
      return self.variables[name['name']][name['index']]
    else:
      return self.variables[name]
  def setProc(self, name, value):
    self.procedures[name] = value
  def getProc(self, name):
    return self.procedures[name]
  def hasProc(self, name):
    return name in self.procedures