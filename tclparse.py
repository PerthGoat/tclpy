
# big stack of parsed stuff
# contains dictionary entries of just about every token
#parse_stack = []

class TCLParse:
  def __init__(self, tcl_str):
    self.parse_tree = []
    self.cmd_list = []
    self.parentextra = ''
    self.extraind = 0
    self.tcl_str = tcl_str
  
  def EOF(self):
    return len(self.tcl_str) == 0

  # look at the next char
  def peek(self):
    assert not self.EOF()
    return self.tcl_str[0]

  # remove the next char
  def pop(self):
    self.tcl_str = self.tcl_str[1:]

  def parse_add(self, key, value):
    if self.parentextra == '':
      self.parse_tree.append({key: value})
    else:
      if self.extraind == 0:
        self.parse_tree.append({self.parentextra: []})
        self.extraind = len(self.parse_tree) - 1
      self.parse_tree[self.extraind][self.parentextra].append({key: value})

  # WORD = ALPHANUM, { ALPHANUM } ;
  def WORD(self):
    wb = ''
    while not self.EOF() and self.ALPHANUM(self.peek()):
      wb += self.peek()
      self.pop()
    return wb

  # END just matches ; or \n or EOF
  # END = ';' | '\n' | EOF ;
  def END(self):
    if self.EOF(): # end of file
      return
    # print(f'"{peek()}"')
    assert self.peek() == ';' or self.peek() == '\n'
    self.pop()

  # WHITE_SPACE just matches a space
  def WHITE_SPACE(self):
    assert self.peek() == ' '
    self.pop()

  def ALPHANUM(self, n):
    return n.isalnum() | (n in '*/+-')

  # BRACEBLOCK = '{', (BRACEBLOCK | (anychar - '}', '}')) ;
  def BRACEBLOCK(self):
    wb = ''
    assert self.peek() == '{'
    self.pop()
    while self.peek() != '}':
      if self.peek() == '{':
        wb += '{' + self.BRACEBLOCK() + '}' # preserves internal braces and only goes one level down
      if self.peek() == '}': break
      wb += self.peek()
      self.pop()
    assert self.peek() == '}'
    self.pop()
    
    return wb

  # VAREXP = '$', ([BRACEBLOCK] | WORD) ;
  def VAREXP(self):
    assert self.peek() == '$'
    self.pop()
    
    if self.peek() == '{':
      self.parse_add('VAREXP', self.BRACEBLOCK())
    elif self.ALPHANUM(self.peek()):
      self.parse_add('VAREXP', self.WORD())
    else:
      print('invalid variable expression')

  # CMDEXP = '[', CMD | ']' ;
  def CMDEXP(self):
    assert self.peek() == '['
    #self.parse_add('COMEXP_START', self.peek())
    self.parentextra = 'COMEXP'
    self.pop()
    self.CMD()
    assert self.peek() == ']'
    #self.parse_add('COMEXP_END', self.peek())
    self.parentextra = ''
    self.extraind = 0
    self.pop()

  # QUOTEBLOCK = '"', { CMDEXP | VAREXP | anychar - ('[', '$') }, " ;
  def QUOTEBLOCK(self):
    wb = ''
    assert self.peek() == '"'
    self.parentextra = 'QUOTE'
    #self.parse_add('QUOTE_START', self.peek())
    self.pop()
    while self.peek() != '"':
      if self.peek() == '[':
        self.parse_add('QUOTE_STR', wb)
        wb = ''
        self.CMDEXP()
        #wb += f'CMDEXP: {CMDEXP()}'
      elif self.peek() == '$':
        self.parse_add('QUOTE_STR', wb)
        wb = ''
        self.VAREXP()
        #wb += f'VAREXP: {VAREXP()}'
      else:
        wb += self.peek()
        self.pop()
      
    assert self.peek() == '"'
    
    if len(wb) > 0: self.parse_add('QUOTE_STR', wb)
    
    #self.parse_add('QUOTE_END', self.peek())
    self.parentextra = ''
    self.extraind = 0
    self.pop()
    
    return wb

  # CMD = { ( WORD | CMDEXP | BRACEBLOCK | QUOTEBLOCK | VAREXP ), [ WHITE_SPACE ] } ;
  def CMD(self):
    while not self.EOF():
    
      c = self.peek()
      if self.ALPHANUM(c): # WORD
        self.parse_add('WORD', self.WORD())
      elif c == '[': # CMDEXP
        self.CMDEXP()
      elif c == '{': # BRACEBLOCK
        self.parse_add('WORD', self.BRACEBLOCK())
      elif c == '"': # QUOTEBLOCK
        self.QUOTEBLOCK()
      elif c == '$': # VAREXP
        self.VAREXP()
      elif c == ']':
        break
      elif c == ' ':
        self.WHITE_SPACE()
      elif c == '\n' or c == ';':
        break
      else:
        print(f'unknown token "{self.peek()}"')
        self.pop()
        break
    
    

  # PROGRAM = { '\n' | ( '#', { anychar - '\n' } ) | ( { WHITE_SPACE }, CMD, [ END ] ) }, EOF ;
  def PROGRAM(self):
    while not self.EOF():
      if self.peek() == '\n':
        self.pop()
        continue
      
      if self.peek() == '#':
        while(not self.EOF() and self.peek() != '\n'):
          self.pop()
        self.pop() # remove newline after (END)
        continue
      
      while self.peek() == ' ':
        self.WHITE_SPACE()
      
      #self.CMD()
      self.CMD()
      self.cmd_list.append(self.parse_tree)
      self.parse_tree = []
      if not self.EOF() and self.peek() in ';\n':
        self.END()
    assert self.EOF()
    return self.cmd_list
