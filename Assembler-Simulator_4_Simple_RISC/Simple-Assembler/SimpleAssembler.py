import sys
import math
from binary_fractions import Binary

tempPC = 0
programCounter = 0
notvar = 0
variableStack = {}
ogVarCounter = 0
varCounter = 0 
labelStack = {}
templabelStack = {}
registerStack = [0,0,0,0,0,0]
flagsStack = [0,0,0,0] #EGLV,0123
binaryStack = []
errorStack = []
program = []
isa = ['addf', 'subf', 'movf', 'var', 'add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je', 'hlt']
def main():
    global program, programCounter, notvar, variableStack, varCounter, labelStack, registerStack, flagsStack, binaryStack, errorStack, program, ogVarCounter
    program = takeInput()
    varCounter = len(program) -1
    ogVarCounter = varCounter
    for x in program:
        if(len(x) == 0):
            programCounter = programCounter + 1
        else:
            commands = x.split()
            if(len(commands) > 5):
                errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
            try:
                left = []
                if('FLAGS' in commands):
                    if(len(commands) == 3 and commands[-2] == 'FLAGS' and 'mov' == commands[0]):
                        pass
                    else:                
                        errorStack.append("Invalid usage of Flags register in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)

                if(commands[0][-1] == ':'):
                    label(commands[0][:-1])
                    commands = commands[1:]
                if(commands[0] != "var"):
                    if(notvar == 0):
                        for x in variableStack:
                            variableStack[x] = variableStack[x] - len(variableStack)
                    notvar = 1
                if(commands[0] == 'addf'):
                    if(len(commands) == 4):
                        addf(commands[1], commands[2], commands[3])
                        left = commands[4:]
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
                if(commands[0] == 'subf'):
                    if(len(commands) == 4):
                        subf(commands[1], commands[2], commands[3])
                        left = commands[4:]
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)

                if(commands[0] == 'movf'):
                    if(len(commands) == 3):
                        if('$' in commands[2]):
                            movFI(commands[1], commands[2])
                            left = commands[3:]
                        else:
                            errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)

                if(commands[0] == 'var'):
                    if(len(commands) == 2):
                        var(commands[1])
                        left = commands[2:]
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
                if(commands[0] == 'add'):
                    if(len(commands) == 4):
                        add(commands[1], commands[2], commands[3])
                        left = commands[4:]
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
                if(commands[0] == 'sub'):
                    if(len(commands) == 4):
                        sub(commands[1], commands[2], commands[3])
                        left = commands[4:]
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
                if(commands[0] == 'mov'):
                    if(len(commands) == 3):
                        if('$' in commands[2]):
                            movI(commands[1], commands[2])
                            left = commands[3:]
                        else:
                            if(commands[1] == 'FLAGS'): 
                                movF(commands[1], commands[2])
                                left = commands[3:]
                            elif('FLAGS' not in commands):
                                movR(commands[1], commands[2])
                                left = commands[3:]
                    else:
                        errorStack.append("Unexpected parameters in line number " + (programCounter + 1).__str__() + "\n" + "Line: " + x)
                if(commands[0] == 'ld'):
                    load(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'st'):
                    stri(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'mul'):
                    mul(commands[1], commands[2], commands[3])
                    left = commands[4:]
                if(commands[0] == 'div'):
                    div(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'rs'):
                    rightS(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'ls'):
                    leftS(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'xor'):
                    exor(commands[1], commands[2], commands[3])
                    left = commands[4:]
                if(commands[0] == 'or'):
                    ore(commands[1], commands[2], commands[3])
                    left = commands[4:]
                if(commands[0] == 'and'):
                    andy(commands[1], commands[2], commands[3])
                    left = commands[4:]
                if(commands[0] == 'not'):
                    invert(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'cmp'):
                    cmp(commands[1], commands[2])
                    left = commands[3:]
                if(commands[0] == 'jmp'):
                    unconJmp(commands[1])
                    left = commands[2:]
                if(commands[0] == 'jlt'):
                    lessJmp(commands[1])
                    left = commands[2:]
                if(commands[0] == 'jgt'):
                    greaterJmp(commands[1])
                    left = commands[2:]
                if(commands[0] == 'je'):
                    equalJmp(commands[1])
                    left = commands[2:]
                if(commands[0] == 'hlt'):
                    hlt()   
                if(commands[0] not in isa):
                    errorStack.append("Unrecognized commands in line number: " + (programCounter + 1).__str__()+ "\n" + "Line: " + x)
                if(len(left) != 0):
                    errorStack.append("Unexpected parameters in line number: " + (programCounter + 1).__str__()+ "\n" + "Line: " + x)

            except IndexError:
                errorStack.append("Expected more parameters in line number:  " + (programCounter + 1).__str__()+ "\n" + "Line: " + x)
            except Exception as e:
                print(e)
                errorStack.append("General Syntax error in line number " + (programCounter + 1).__str__()+ "\n" + "Line: " + x)
            programCounter = programCounter + 1
    if(len(errorStack)==0):
        for x in binaryStack[:256]:
            print(x)
    else:
        for x in errorStack:
            print(x)
            print("\n")

def takeInput():
    listy = sys.stdin.read().split("\n")
    listy = list(filter(None, listy))
    return listy

def checkRegBounds(r1, r2, r3):
    flag = 0
    if(not(r1[0] == 'R' and (r2[0] == 'R' or r2 == 'FLAGS') and r3[0] == 'R')):
        errorStack.append("Syntax error, invalid registers, Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        flag = 1
    else:
        r1 = int(r1[1:])
        r2 = int(r2[1:])
        r3 = int(r3[1:])
        if(r1 > 6 or r1 < 0):
            errorStack.append("Register is undefined R" + r1 + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
            flag = 1
        if(r2 > 6 or r2 < 0):
            errorStack.append("Register is undefined R" + r2 + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
            flag = 1
        if(r3 > 6 or r3 < 0):
            errorStack.append("Register is undefined R" + r3 + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
            flag = 1
    return flag

def checkFloatingRange(val):
    val = float(val[1:])
    m,e = math.frexp(val)
    integerVal = int(val)
    flag = 0
    b = str(Binary(m))[4:]
    if(e.bit_length() > 3):
        flag = 1
        errorStack.append("floater is out of range " + val + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
    if(len(b)>5):
        errorStack.append("floater is out of range " + val + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        flag = 1
    return flag

def checkWholeRange(val):
    val = int(val[1:])
    flag = 0
    if(val>255 or val < 0):
        flag = 1
        errorStack.append("lmm is out of range " + val + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
    if(val - int(val) != 0):
        errorStack.append("lmm is not a whole number " + val + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        flag = 1
    return flag

def checkVar(variz):
    flag = 0
    if(variz not in variableStack):
        if(variz in labelStack):
            flag = 1
            errorStack.append("label is misused as a variable " + variz + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        else:
            errorStack.append("variable is undefined " + variz + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
            flag = 1
    return flag

def checkLabel(addr):
    flag = 0
    global tempPC
    for x in program:
        commands = x.split()
        if(commands[0][-1] == ':'):
                templabel(commands[0][:-1])
                commands = commands[1:]
        tempPC = tempPC + 1
    tempPC = 0
    if(addr not in labelStack and addr not in templabelStack):
        if(addr in variableStack):
            flag = 1
            errorStack.append("variable is misused as a label " + addr + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        else:
            errorStack.append("label is undefined " + addr + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        flag = 1
    return flag

def immtoBinary(val):
    try:
        return '{0:08b}'.format(val)
    except:
        return '{0:08b}'.format(int(val[1:])) 

def exptoBinary(val):
    try:
        return '{0:03b}'.format(val)
    except:
        return '{0:03b}'.format(int(val[1:])) 

def ftoBinary(val):
    val = float(val[1:])
    m,e = math.frexp(val)
    s = ''
    b = str(Binary(m))[4:]
    if(len(b) == 1):
        b = b + '0000'
    if(len(b) == 2):
        b = b + '000'
    if(len(b) == 3):
        b = b + '00'
    if(len(b) == 4):
        b = b + '0'

    s = exptoBinary(e) + b
    return s
    
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
        return '110'

def var(name):
    global varCounter, variableStack
    if(notvar == 1):
        errorStack.append("Variables not declared at the beginning, Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        return
    if(name in variableStack):
        errorStack.append("Variables already declared, Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        return
    if(name in labelStack):
        errorStack.append("Variable name already declared as label, Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        return
    varCounter = varCounter + 1
    variableStack[name] = varCounter

def label(name):
    global varCounter, labelStack,ogVarCounter
    if(name in labelStack):
        errorStack.append("Label already declared: " + name + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        return
    if(' ' in name):
        errorStack.append("Label contains space before ':' " + name + " Line Number: " + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
        return
    labelStack[name] = [programCounter - varCounter + ogVarCounter]

def templabel(name):
    global varCounter, templabelStack, ogVarCounter, tempPC
    if(name in labelStack):
        return
    if(' ' in name):
        return
    templabelStack[name] = [tempPC - varCounter + ogVarCounter]



def addf(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('00000' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def subf(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('00001' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def movFI(r1, val):
    b = checkFloatingRange(val)
    if(not checkRegBounds(r1, 'R0', 'R0') and not b):
        binaryStack.append('00010' + regtoBinary(r1) + ftoBinary(val))


def add(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('10000' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def sub(r1,r2,r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('10001' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def movI(r1, val):
    b = checkWholeRange(val)
    if(not checkRegBounds(r1, 'R0', 'R0') and not b):
        binaryStack.append('10010' + regtoBinary(r1) + immtoBinary(val))

def movF(r1,r2):
    if(not checkRegBounds(r2, 'R0', 'R0') and r1 == 'FLAGS'):
        binaryStack.append('1001100000' + regtoBinary(r2) + '111')

def movR(r1,r2):
    if(not checkRegBounds(r1, r2, 'R0')):
        binaryStack.append('1001100000' + regtoBinary(r1) + regtoBinary(r2))

def load(r1, vari):
    a = checkRegBounds(r1,'R0','R0')
    b = checkVar(vari)
    if(not a and not b):
        binaryStack.append('10100' + regtoBinary(r1) + immtoBinary(variableStack.get(vari)))

def stri(r1, vari):
    a = checkRegBounds(r1,'R0','R0')
    b = checkVar(vari)
    if(not a and not b):
        binaryStack.append('10101' + regtoBinary(r1) + immtoBinary(variableStack.get(vari)))

def mul(r1, r2, r3):
    if(not checkRegBounds(r1,r2,r3)):
        binaryStack.append('10110' + '00' + regtoBinary(r1) + regtoBinary(r2) + regtoBinary(r3))

def div(r3, r4):
    if(not checkRegBounds(r3,r4,'R0')):
        binaryStack.append('10111' + '00000' + regtoBinary(r3) + regtoBinary(r4))

def rightS(r1, val):
    a = checkRegBounds(r1,'R0','R0')
    b = checkWholeRange(val)
    if(not checkRegBounds(r1,'R0','R0') and not b):
        binaryStack.append('11000' + regtoBinary(r1) + immtoBinary(val))


def leftS(r1, val):
    b = checkWholeRange(val)
    if(not checkRegBounds(r1,'R0','R0') and not b):
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
        binaryStack.append('11101' + '00000' + regtoBinary(r1) + regtoBinary(r2))

def cmp(r1,r2):
    if(not checkRegBounds(r1,r2,'R0')):
        binaryStack.append('11110' + '00000' + regtoBinary(r1) + regtoBinary(r2))

def unconJmp(label):
    if(not checkLabel(label)):
        temp = ''
        if(label not in labelStack):
            temp = templabelStack.get(label)
        else:
            temp = labelStack.get(label)
        binaryStack.append('11111' + '000' + immtoBinary(temp[0]))

def lessJmp(label):
    if(not checkLabel(label)):
        temp = ''
        if(label not in labelStack):
            temp = templabelStack.get(label)
        else:
            temp = labelStack.get(label)
        binaryStack.append('01100' + '000' + immtoBinary(temp[0]))

def greaterJmp(label):
    if(not checkLabel(label)):
        temp = ''
        if(label not in labelStack):
            temp = templabelStack.get(label)
        else:
            temp = labelStack.get(label)
        binaryStack.append('01101' + '000' + immtoBinary(temp[0]))

def equalJmp(label):
    if(not checkLabel(label)):
        temp = ''
        if(label not in labelStack):
            temp = templabelStack.get(label)
        else:
            temp = labelStack.get(label)
        binaryStack.append('01111' + '000' + immtoBinary(temp[0]))

def hlt():
    if(programCounter != len(program) - 1):
        errorStack.append('halt command not the last command, line Number: ' + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
    else:
        binaryStack.append('01010' + '00000000000')

main()