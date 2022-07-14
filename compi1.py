from Tokens import Tokens
from Node import Node

global content_index
global content
content_index = 0

def peek():
    global content_index
    global content
    return content[content_index]

def advance():
    global content_index
    val = peek()
    content_index = content_index + 1
    return val

def eof():
    global content
    global content_index
    return content_index >= len(content)

def scan_digits():
    ans = {
        'val': '',
        'type': ''
    }
    while peek() in '0123456789':
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else:
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek() in '0123456789':
            ans['val'] = ans['val'] + advance()
    return ans

def scanner():
    global content_index
    global content
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n'):
        advance()
    if eof():
        ans['type'] = '$'
    else:
        if peek() in "0123456789":
            ans = scan_digits()
        else:
            ch = advance()
            if (ch in "abcdeghjklmnoqrstuvwxyz"):
                ans['type'] = 'id'
                ans['val'] = ch
            elif ch == 'f':
                ans['type'] = 'floatdcl'
            elif ch == 'i':
                ans['type'] = 'intdcl'
            elif ch == 'p':
                ans['type'] = 'print'
            elif ch == '=':
                ans['type'] = 'assign'
            elif ch == '+':
                ans['type'] = 'plus'
            elif ch == '-':
                ans['type'] = 'minus'
            else:
                print('LEXICAL ERROR')
                exit()
    return ans

#---------------------------------------------
def val():
    token = None
    current = tokens.peek()
    if current == "id" or current == "inum" or current == "fnum":
        token = tokens.match(current)
    else:
        print("error: bad convert")
        exit()
    return [Node(token["type"], token["val"])]


def ex(valNode):
    node = None
    current = tokens.peek()
    if current == "plus" or current == "minus":
        node = Node(current)
        node.addChilds(valNode)
        tokens.match(current)
        next_val = val()
        node.addChilds(ex(next_val))
    if node is not None:
        return [node]
    return valNode


def stmt():
    node = Node()
    if tokens.peek() == "id":
        token = tokens.match("id")
        tokens.match("assign")
        node.setInfo("assign")
        node.addChilds([Node(token["type"], token["val"])])
        valNode = val()
        node.addChilds(ex(valNode))
    else:
        if tokens.peek() == "print":
            tokens.match("print")
            token = tokens.match("id")
            node.setInfo("print", token["val"])
        else:
            print("error: bad convert")
            exit()
    return [node]


def stmts():
    child = []
    if tokens.peek() == "id" or tokens.peek() == "print":
        child += stmt()
        child += stmts()
    else:
        if tokens.peek() != "$":
            print("error: bad convert")
            exit()
    return child


def dcl():
    type = ""
    val = ""
    current = tokens.peek()
    if current == "floatdcl" or current == "intdcl":
        type = tokens.match(current)["type"]
        val = tokens.match("id")["val"]
    else:
        print("error: bad convert")
        exit()
    return [Node(type, val)]


def dcls():
    child = []
    if tokens.peek() == "floatdcl" or tokens.peek() == "intdcl":
        child += dcl()
        child += dcls()
    return child

def doText(child, num=0):
    current = num
    t2 = 'r' + str(num)
    new = []
    text = []
    if child.type in ['fnum', 'inum', 'id']:
      t2 = child.val
      current -= 1
    elif child.type in ['floatdcl', 'intdcl', 'print']:
      t2 = child.val
      text.append(child.type + ' ' + child.val)
      current -= 1
    elif child.type == 'assign':
      prev, current, new = doText(child.child[1],current + 1)
      text.append(child.child[0].val + ' = ' + prev)
    elif child.type == 'int2float':
      t2 = 'r' + str(current)
      der, current, new = doText(child.child[0],current + 1)
      text.append(t2 + ' = ' + child.type + ' ' + der)
    elif child.type == 'plus' or child.type == 'minus':
      t2 = 'r' + str(current)
      izq, current, izqT = doText(child.child[0], current + 1)
      der, current, derT = doText(child.child[1], current + 1)
      new = new + izqT + derT
      if child.type == 'plus':
        text.append(t2 + ' = ' + izq + ' + ' + der)
      else:
        text.append(t2 + ' = ' + izq + ' - ' + der)
    return t2, current, new + text

#----------------------------------------------------------------------
with open("s.txt", "r") as f:
    content = f.read()

tokens = Tokens()
while not eof():
    tokens.append(scanner())
if not tokens.empty() and tokens.last() != "$":
    tokens.append(scanner())

print(tokens, "\n")
root = Node()
root.setInfo("PROG")
root.addChilds(dcls())
root.addChilds(stmts())
tree = root

table = {}
for child in tree.child:
  if child.type == 'intdcl':
    if child.val not in table:
      table[child.val] = 'int'
    else:
      print("error: doble")
      exit()
  elif child.type == 'floatdcl':
    if child.val not in table:
      table[child.val] = 'float'
    else:
      print("error: doble")
      exit()
tree.checking(table)
print( tree, "\n")

text = []
for child in tree.child:
  _, _, textfile = doText(child)
  text += textfile
f = open("Three.txt", "w")
for line in text:
    f.write(line + '\n')
f.close()


