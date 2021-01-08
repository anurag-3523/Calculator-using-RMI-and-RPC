import xmlrpc.client as xc
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional, ZeroOrMore, Forward, nums, alphas, oneOf)
from subprocess import Popen

addHost = xc.ServerProxy("http://localhost:8001/")
subHost = xc.ServerProxy("http://localhost:8002/")
multHost = xc.ServerProxy("http://localhost:8003/")
divHost = xc.ServerProxy("http://localhost:8004/")

# def startHosts():
#     Popen("pyhton3 addition_Host.py")
#     Popen("pyhton3 subtraction_Host.py")
#     Popen("pyhton3 multiplication_Host.py")
#     Popen("pyhton3 division_Host.py")



class ExpressionParser(object):

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        
        point = Literal(".")
        fnumber = Combine( Word("+-" + nums, nums) + Optional( point + Optional(Word(nums)) ) )
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div

        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar| fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)

        factor = Forward()
        factor << atom 
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        self.opn= { '+': (lambda n1, n2: addHost.add(n1,n2)),
                    '-': (lambda n1, n2: subHost.sub(n1,n2)),
                    '*': (lambda n1, n2: multHost.mult(n1,n2)),
                    '/': (lambda n1, n2: divHost.div(n1,n2)) }
        
    def evalStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evalStack(s)
        if op in "+-*/":
            op2 = self.evalStack(s)
            op1 = self.evalStack(s)
            return self.opn[op](op1, op2)
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def evalExpr(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        value = self.evalStack(self.exprStack[:])
        return value

if __name__ == "__main__":
    # startHosts()
    expression = input("Enter an expression: ")
    calculator = ExpressionParser()
    result = calculator.evalExpr(expression.replace(" ", ""))
    print(result)
    #result = calculator.evalExpr('5*10/(2+4)')
    
