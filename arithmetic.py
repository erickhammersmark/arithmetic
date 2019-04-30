#!/usr/bin/env python

import sys


class ArithmeticElement(object):

  def __init__(self, *args, **kwargs):
    self.value = None
    if args:
      self.value = args[0]

  @staticmethod
  def classify(string):
    data = ArithmeticData.classify(string)
    if data:
      return data

    value = ArithmeticOperator.classify(string)
    if value:
      return value

    return None

  def __repr__(self):
    return str(self.value)


class ArithmeticOperator(ArithmeticElement):

  @staticmethod
  def classify(string):
    if string == "+":
      return Plus
    if string == "-":
      return Minus
    return None
    
  def operate(self, a, b):
    return -1

class Plus(ArithmeticOperator):

  def operate(self, a, b):
    return a + b

class Minus(ArithmeticOperator):

  def operate(a, b):
    return a - b


class ArithmeticData(ArithmeticElement):

  @staticmethod
  def classify(string):
    if Constant.matches(string):
      return Constant
    if Variable.matches(string):
      return Variable
    return None

  @staticmethod
  def matches(string):
    return False

class Constant(ArithmeticData):

  def __init__(self, *args, **kwargs):
    ArithmeticData.__init__(self, *args, **kwargs)
    self.value = float(self.value)

  @staticmethod
  def matches(string):
    if string.isdigit():
      return True

    for c in string:
      if not c.isdigit() and c != ".":
        return False

    return True

class Variable(ArithmeticData):

  @staticmethod
  def matches(string):
    return string.isalpha()


def parseArithmeticExpression(expr):
  parts = expr.split()
  for idx, part in enumerate(parts):
    kind = ArithmeticElement.classify(part)
    if kind:
      parts[idx] = kind(part)
  return parts


def evaluate(expr):
  parts = parseArithmeticExpression(expr)
  return parts

def main():
  print(evaluate(sys.argv[1]))

if __name__ == "__main__":
  main()
