#!/usr/bin/env python3

import sys


class ArithmeticElement(object):
  '''
  Parent of all of the classes below
  Initializes self.value to whatever is passed to its constructor
  '''

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
    return "x" + str(self.value)


class ArithmeticOperator(ArithmeticElement):
  '''
  Parent of all of the arithmetic operation objects
  Inherits from ArithmeticElement
  '''

  operators = {}

  @staticmethod
  def classify(string):
    if string in ArithmeticOperator.operators:
      return ArithmeticOperator.operators[string]
    return None
    
  def operate(self, a, b):
    return -1


class Plus(ArithmeticOperator):
  symbol = "+"

  def operate(self, a, b):
    return a + b


class Minus(ArithmeticOperator):
  symbol = "-"

  def operate(self, a, b):
    return a - b


for cls in ArithmeticOperator.__subclasses__():
  ArithmeticOperator.operators[cls.symbol] = cls


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
  result = 0

  parts = parseArithmeticExpression(expr)

  if not parts:
    print("Error parsing expression {}".format(expr))
    return result

  if not isinstance(parts[0], ArithmeticData):
    print("First part of expression {0} is not data: {1}".format(expr, parts[0]))
    return result

  result = parts.pop(0).value

  while parts:
    part = parts.pop(0)
    if isinstance(part, ArithmeticOperator):
      if not parts:
        print("Error, last element in expression is operator {0}".format(part))
        return result
      if not isinstance(parts[0], ArithmeticData):
        print("Error, element following operator is not data: {0} {1}".format(part, parts[0]))
      arg = parts.pop(0).value
      result = part.operate(result, arg)

  return result


def main():
  print(evaluate(sys.argv[1]))

if __name__ == "__main__":
  main()
