pc = 0
notvar = 0
variableStack = {}
varCounter = 0 
labelStack = {}
registerStack = [0,0,0,0,0,0]
flagsStack = [0,0,0,0] #EGLV,0123
binaryStack = []
errorStack = []
program = []

def main():
    global program, pc, notvar, variableStack, varCounter, labelStack, registerStack, flagsStack, binaryStack, errorStack, program
    program = takeInput()
    for x in program:
        if(len(x) == 0):
            pc = pc + 1
        else:
            try:
                if(commands[0] != "var"):
                    notvar = 1
                if(commands[0] == 'var'):
                    var(commands[1])
                if(commands[0] == 'add'):
                    add(commands[1], commands[2], commands[3])
                if(commands[0] == 'sub'):
                    sub(commands[1], commands[2], commands[3])
                if(commands[0] == 'mov'):
                    if('$' in commands[2]):
                        movI(commands[1], commands[2])
                    else:
                        movR(commands[1], commands[2])
                if(commands[0] == 'ld'):
                    load(commands[1], commands[2])
                if(commands[0] == 'st'):
                    str(commands[1], commands[2])
                if(commands[0] == 'mul'):
                    mul(commands[1], commands[2], commands[3])
                if(commands[0] == 'div'):
                    div(commands[1], commands[2])
                if(commands[0] == 'rs'):
                    rightS(commands[1], commands[2])
                if(commands[0] == 'ls'):
                    leftS(commands[1], commands[2])
                if(commands[0] == 'xor'):
                    exor(commands[1], commands[2], commands[3])
                if(commands[0] == 'or'):
                    ore(commands[1], commands[2], commands[3])
                if(commands[0] == 'and'):
                    andy(commands[1], commands[2], commands[3])
                if(commands[0] == 'not'):
                    invert(commands[1], commands[2])
                if(commands[0] == 'cmp'):
                    cmp(commands[1], commands[2])
                if(commands[0] == 'jmp'):
                    unconJmp(commands[1])
                if(commands[0] == 'jlt'):
                    lessJmp(commands[1])
                if(commands[0] == 'jgt'):
                    greaterJmp(commands[1])
                if(commands[0] == 'je'):
                    equalJmp(commands[1])
                if(commands[0] == 'hlt'):
                    hlt()
                else:
                    if(commands[0][-1] == ':'):
                        label(commands[0][::-1])
            except:
                errorStack.append("Syntax error in line number " + str(pc))
            commands = x.split(' ')
            if(len(commands) > 3){
                errorStack.append("Unexpected parameters in line number " + str(pc))
            }
            pc = pc + 1
    if(len(errorStack)==0):
        for x in binaryStack:
            print(x)
    else:
        for x in errorStack:
            print(x)
    


def takeInput():
    listy = ['var X','mov R1 $10', 'st R3 X','hlt']
    '''filey = open("input", "r")
    data = filey.read()
    listy = data.split("\n")'''
    return listy

def checkRegBounds(r1, r2, r3):
    flag = 0
    if(not(r1[0] == 'R' and r2[0] == 'R' and r3[0] == 'R')):
        errorStack.append("Syntax error, register not input correctly")
    r1 = int(r1[1:])
    r2 = int(r2[1:])
    r3 = int(r3[1:])
    if(r1 > 6 or r1 < 0):
        errorStack.append("Register is undefined " + r1)
        flag = 1
    if(r2 > 6 or r2 < 0):
        errorStack.append("Register is undefined " + r2)
        flag = 1
    if(r3 > 6 or r3 < 0):
        errorStack.append("Register is undefined " + r3)
        flag = 1
    return flag

def checkWholeRange(val):
    val = int(val[1:])
    flag = 0
    if(val>255 or val < 0):
        flag = 1
        errorStack.append("lmm is out of range " + val)
    if(val - int(val) != 0):
        errorStack.append("lmm is not a whole number " + val)
        flag = 1
    return flag

def checkVar(vari):
    if(vari not in variableStack):
        if(label in labelStack):
            errorStack.append("label is misused as a variable " + vari)
        errorStack.append("variable is undefined " + vari)

def checkLabel(addr):
    if(addr not in labelStack):
        if(addr in variableStack):
            errorStack.append("variable is misused as a label " + addr)
        errorStack.append("label is undefined" + addr)

def immtoBinary(val):
    try:
        return '{0:08b}'.format(val)
    except:
        return '{0:08b}'.format(int(val[1:])) 
    
def regtoBinary(r1):
    r1 = int(r1[1:])
    if(r1 == 0):
        return '000'
    if(r1 == 1):
        return '001'
    if(r1 == 2):
        return '010'
    if(r1 == 3):
        return '011'
    if(r1 == 4):
        return '100'
    if(r1 == 5):
        return '101'
    if(r1 == 6):
        return '111'

def var(name):
    global varCounter, variableStack
    if(notvar == 1):
        errorStack.append("Variables not declared at the beginning, Line: " + pc)
        return
    if(name in variableStack):
        errorStack.append("Variables already declared")
        return
    if(name in labelStack):
        errorStack.append("Variable name already declared as label")
        return
    varCounter = varCounter + 1
    variableStack[name] = varCounter

def label(name):
    if(name in labelStack):
        errorStack.append("Label already declared")
        return
    labelStack[name] = [pc, varCounter]
    varCounter = varCounter + 1



def add(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('10000' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def sub(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('10001' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def movI(r1, val):
    if(not checkRegBounds(r1, 'R0', 'R0') and not checkWholeRange(val)):
        binaryStack.append('10010' + regtoBinary(r1) + immtoBinary(val))

def movR(r1,r2):
    if(not checkRegBounds(r1, r2, 'R0')):
        binaryStack.append('1001100000' + regtoBinary(r1) + regtoBinary(r2))

def load(r1, vari):
    if(not checkRegBounds(r1,'R0','R0') or checkVar(vari)):
        binaryStack.append('10100' + regtoBinary(r1) + immtoBinary(variableStock.get(vari)))

def str(r1, vari):
    if(not checkRegBounds(r1,'R0','R0') or checkVar(vari)):
        binaryStack.append('10101' + regtoBinary(r1) + immtoBinary(variableStack.get(vari)))

def mul(r1, r2, r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('10110' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def div(r3, r4):
    if(not checkRegBounds(r3,r4,'R0')):
        binaryStack.append('10111' + '00000' + regtoBinary(r3) + regtoBinary(r4))

def rightS(r1, val):
    if(not checkRegBounds(r1,'R0','R0') or not checkWholeRange(val)):
        binaryStack.append('11000' + regtoBinary(r1) + immtoBinary(val))


def leftS(r1, val):
    if(not checkRegBounds(r1,'R0','R0') or not checkWholeRange(val)):
        binaryStack.append('11001' + regtoBinary(r1) + immtoBinary(val))

def exor(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('11010' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))


def ore(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('11011' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))


def andy(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('11100' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def invert(r1,r2):
    if(not checkRegBounds(r1,r2,'R0')):
        binaryStack.append('10111' + '00000' + regtoBinary(r1) + regtoBinary(r2))

def cmp(r1,r2):
    if(not checkRegBounds(r1,r2,'R0')):
        binaryStack.append('10111' + '00000' + regtoBinary(r1) + regtoBinary(r2))

def unconJmp(label):
    if(not checkLabel(label)):
        binaryStack.append('11111' + '000' + immtoBinary(labelStack.get(label)[1]))

def lessJmp(addr):
    if(not checkLabel(label)):
        binaryStack.append('01100' + '000' + immtoBinary(labelStack.get(label)[1]))

def greaterJmp(addr):
    if(not checkLabel(label)):
        binaryStack.append('01101' + '000' + immtoBinary(labelStack.get(label)[1]))

def equalJmp(addr):
    if(not checkLabel(label)):
        binaryStack.append('01111' + '000' + immtoBinary(labelStack.get(label)[1]))

def hlt():
    if(pc != len(program) - 1):
        errorStack.append('halt command not the last command, line : ' + str(pc))
    else:
        binaryStack.append('01010' + '00000000000')




main()