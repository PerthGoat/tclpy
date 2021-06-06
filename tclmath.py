# this is a library im making
# to assist with doing math in tcl
# by making my own math parsing machine

def find_matching_paren(s):
  index_l_paren = s.index('(')
  b = 1
  for i in range(index_l_paren + 1, len(s)):
    c = s[i]
    if c == '(':
      b += 1
    if c == ')':
      b -= 1
    if b == 0:
      break
  if b != 0:
    print('left paren without matching right')
    return -1
  return i
def process_math_ex(stack):
  #print(stack)
  # parens are highest priority
  if('(' in stack):
    left_paren = stack.index('(')
    right_paren = find_matching_paren(stack)
    
    if(right_paren == -1):
      print('bad op returning 0')
      return 0
      
    #input()
    process_stack = stack[left_paren+1:right_paren]
    new_paren_val = process_math_ex(process_stack) # new val after calculating paren
    
    stack = stack[0:left_paren] + [new_paren_val] + stack[right_paren+1:]
  elif('*' in stack): # this means there is multiplication
    op = stack.index('*')
    res = float(stack[op - 1]) * float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif('/' in stack): # division
    op = stack.index('/')
    res = float(stack[op - 1]) / float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif('+' in stack): # addition
    op = stack.index('+')
    res = float(stack[op - 1]) + float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif('-' in stack): # subtraction
    op = stack.index('-')
    res = float(stack[op - 1]) - float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif('>' in stack): # greater than
    op = stack.index('>')
    res = float(stack[op - 1]) > float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif('<' in stack): # less than
    op = stack.index('<')
    res = float(stack[op - 1]) < float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif('=' in stack): # equal to
    op = stack.index('=')
    res = float(stack[op - 1]) == float(stack[op + 1])
    stack.remove(stack[op - 1])
    stack.remove(stack[op - 1])
    stack[op - 1] = res
  elif len(stack) == 0:
    return 0
  elif(stack[0].isdigit()):
    return float(stack[0])
  else: # unknown op
    print(f"unknown op {stack} this might bubble down, returning 0")
    return 0
  
  if(len(stack) > 1):
    return process_math_ex(stack)
  return float(stack[0])
  
def eval_math_expr(ex):
  math_stack = []
  sb = ''
  
  for c in ex:
    if c.isdigit() or c == '.':
      sb += c
    else:
      if(len(sb) > 0):
        math_stack.append(sb)
      if(c != ' '):
        math_stack.append(c)
      sb = ''
  
  if(len(sb) > 0):
    math_stack.append(sb)
    
  return process_math_ex(math_stack)

def run_tests():
  # test cases

  assert eval_math_expr('3.5 * 4') == 14
  assert eval_math_expr('4 * 4 * 4') == 64
  assert eval_math_expr('4 * 4 * 4.5') == 72
  assert eval_math_expr('4 + (4 * 4.5)') == 22
  assert eval_math_expr('4 + 4 * (4.5 + 0.5 + 1 * (3 + 4 * (1)))') == 52
  assert eval_math_expr('4+(4*4.5)') == 22
  assert eval_math_expr('4') == 4
  assert eval_math_expr('4 (') == 0 # this should make error
  assert eval_math_expr('4(3)') == 4 # multiplcation for this doesn't work since it's not in the TCL standard
  assert eval_math_expr('a') == 0 # this tests if letters are handled sanely
