import sys

MEM = [0] * 512
programLength = initialize(MEM)
programCounter = 0
halted = False
RF = [0] * 11 #0,1,2,3,4,5,6,v,l,g,e

def initialize(memory):
	listy = sys.stdin.read().split("\n")
	count = 0
    for x in listy:
    	memory[count] = x
    return len(listy)

def getData(memory, PC):
	return memory[programCounter]

def execute(instruction):
	opcode = instruction[0:5]
	notOpcode = instruction[5:]
	match opcode:
		case '10000':
			add(notOpcode)
		case '10001':
			sub(notOpcode)
		case '10010':
			movI(notOpcode)
		case '10011':
			movR(notOpcode)
		case '10100':
			load(notOpcode)
		case '10101':
			store(notOpcode)
		case '10110':
			mul(notOpcode)
		case '10111':
			div(notOpcode)
		case '11000':
			rightS(notOpcode)
		case '11001':
			leftS(notOpcode)
		case '11010':
			exor(notOpcode)
		case '11011':
			ore(notOpcode)
		case '11100':
			andy(notOpcode)
		case '11101':
			invert(notOpcode)
		case '11110':
			cmp(notOpcode)
		case '11111':
			unconJmp(notOpcode)
		case '01100':
			lessJmp(notOpcode)
		case '01101':
			greaterJmp(notOpcode)
		case '01111':
			equalJmp(notOpcode)
		case '01010':
			hlt(notOpcode)

def dump(memory):
	for x in memory:
		print(x)

def integerToBinary(inty):
	return 

def binaryToInteger(bin):
	return int(bin, 2)

def getVariable(addr):
	return MEM[addr + programLength]

def add(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[6:9])
	r3 = binaryToInteger(instruction[10:13])
	global RF
	RF[r3] = RF[r2] + RF[r1]
	programCounter = programCounter + 1

def sub(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[6:9])
	r3 = binaryToInteger(instruction[10:13])
	global RF
	if(RF[r2] > RF[r1]):
		RF[r3] = 0
		RF[-4] = 1
	else:
		RF[r3] = RF[r2] + RF[r1]
	programCounter = programCounter + 1

def movI(instruction):
	

def movF(instruction):
    if(not checkRegBounds(r1, 'R0', 'R0') and r2 == 'FLAGS'):
        binaryStack.append('1001100000' + regtoBinary(r1) + '111')

def movR(instruction):
    if(not checkRegBounds(r1, r2, 'R0')):
        binaryStack.append('1001100000' + regtoBinary(r1) + regtoBinary(r2))

def load(r1, vari):
    a = checkRegBounds(r1,'R0','R0')
    b = checkVar(vari)
    if(not a and not b):
        binaryStack.append('10100' + regtoBinary(r1) + immtoBinary(variableStack.get(vari)))

def str(r1, vari):
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
        binaryStack.append('10111' + '00000' + regtoBinary(r1) + regtoBinary(r2))

def cmp(r1,r2):
    if(not checkRegBounds(r1,r2,'R0')):
        binaryStack.append('10111' + '00000' + regtoBinary(r1) + regtoBinary(r2))

def unconJmp(label):
    if(not checkLabel(label)):
        binaryStack.append('11111' + '000' + immtoBinary(labelStack.get(label)[0]))

def lessJmp(addr):
    if(not checkLabel(addr)):
        binaryStack.append('01100' + '000' + immtoBinary(labelStack.get(label)[0]))

def greaterJmp(addr):
    if(not checkLabel(addr)):
        binaryStack.append('01101' + '000' + immtoBinary(labelStack.get(label)[0]))

def equalJmp(addr):
    if(not checkLabel(addr)):
        binaryStack.append('01111' + '000' + immtoBinary(labelStack.get(label)[0]))

def hlt():
    if(programCounter != len(program) - 1):
        errorStack.append('halt command not the last command, line Number: ' + (programCounter + 1).__str__() + "\n" + "Line: " + program[programCounter])
    else:
        binaryStack.append('01010' + '00000000000')

while(not halted):
	instruction = getData(memory, programCounter)
	execute(instruction)
	dump(programCounter)
	dump(RF)
