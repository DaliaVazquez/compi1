class Tokens:
  tokens = None

  def __init__(self):
    self.tokens = []

  def empty(self):
    return len(self.tokens) == 0

  def append(self, ans):
    self.tokens.append(ans)

  def peek(self):
    return self.tokens[0]["type"]

  def last(self):
    return self.tokens[len(self.tokens) - 1]["type"]

  def match(self, simbol):
    ans = self.tokens.pop(0)
    if ans["type"] != simbol:
      print("error")
      exit()
    return ans

  def __str__(self):
    v = ""
    for ans in self.tokens:
      v += ans["type"]
      if "val" in ans:
        v += ": " + ans["val"]
      v += ", "
    return v