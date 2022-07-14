import copy

class Node:
  child = None
  def __init__(self, type = "", val = "", datType = ""):
    self.type = type
    self.val = val
    self.datType = datType
    self.child = []

  def setInfo(self, type = "", val = ""):
    self.type = type
    self.val = val

  def addChilds(self, ch):
    self.child += ch

  def checking(self, table):
    for child in self.child:
      child.checking(table)
    if self.val in table:
      self.datType = table[self.val]
    elif self.type == 'fnum':
      self.datType = 'float'
    elif self.type == 'inum':
      self.datType = 'int'
    elif self.type == 'plus' or self.type == 'minus':
      type = ' '
      if self.child[0].datType == 'float' or self.child[0].datType == 'float':
        type = 'float'
      else:
        type = 'int'
      self.convert(self.child[0], type)
      self.convert(self.child[1], type)
      self.datType = type
    elif self.type == 'assign':
      self.datType = self.convert(self.child[1], self.child[0].datType)

  def __str__(self, level=0):
    st = "\t" * level + (self.type + ': ' + str(self.val) + ' (' + self.datType + ')') + "\n"
    for child in self.child:
      st += child.__str__(level + 1)
    return st

  def convert(self, node, type):
    if node.datType == 'float' and type == 'int':
      print("error: bad convert")
      exit()
    elif node.datType == 'int' and type == 'float':
      temp = copy.deepcopy(node)
      node.type = "int2float"
      node.val = ""
      node.datType = "float"
      node.child = []
      node.addChilds([temp])
      return 'float'
    return type

