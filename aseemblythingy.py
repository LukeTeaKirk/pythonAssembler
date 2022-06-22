pc = 0
notvar = 0
variableStack = {} 
labelStack = {}
registerStack = [0,0,0,0,0,0]
flagsStack = [0,0,0,0] #EGLV,0123
binaryStack = []
errorStack = []

def main():
    commands = takeInput()
    for x in listy:
        if(len(x) == 0):
            pc = pc + 1
            break
        commands = x.split(' ')
        if(commands[0] != "var"):
            notvar = 1
        if(commands[0] == 'var'):
            var()
        if(commands[0] == 'var'):
            var()


def takeInput():
    listy = []
    filey = open("input", "r")
    data = filey.read()
    listy = data.split("\n")
    return listy

def decodeLine():

def var(name):
    if(notvar == 1):
        errorstack.append("Variables not declared at the beginning, Line: " + pc)
        return
    if(name in variableStack):
        errorstack.append("Variables already declared")
        return
    if(name in labelStack):
        errorstack.append("Variable name already declared as label")
        return

    variableStack[name] = null
def add(r1,r2,r3):
    
def sub(r1,r2,r3):
    

def movI(r1, val):
    
def movR(r1,r2):
    
def load(r1, addr):
    

def str(r1, addr):
    

def mul(r1, r2, r3):
    

def div(r3, r4):
    

def rightS(r1, val):
    

def leftS(r1, val):


def exor(r1,r2,r3):
    

def ore(r1,r2,r3):
    

def andy(r1,r2,r3):

def invert(r1,r3):

def cmp(r1,r2):

def unconJmp(addr):

def lessJmp(addr):

def geaterJmp(addr):

def equalJmp(addr):

def hlt():





