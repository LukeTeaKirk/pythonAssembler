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
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[4:12])
	global RF
	RF[r1] = imm
	programCounter = programCounter + 1;



def movF(instruction):
    if(not checkRegBounds(r1, 'R0', 'R0') and r2 == 'FLAGS'):
        binaryStack.append('1001100000' + regtoBinary(r1) + '111')

def movR(instruction):
	r1 = binaryToInteger(instruction[6:9])
	r2 = binaryToInteger(instruction[10:13])
	global RF
	RF[r2] = RF[r1]
	programCounter = programCounter + 1

def load(instruction):
	r1 = binaryToInteger(instruction[0:3])
	addr = binaryToInteger(instruction[4:12])
	global MEM, RF
	RF[r1] = MEM[addr]
	programCounter = programCounter + 1

def str(instruction):
	r1 = binaryToInteger(instruction[0:3])
	addr = binaryToInteger(instruction[4:12])
	global MEM, RF
	MEM[addr] = RF[r1] 
	programCounter = programCounter + 1

def mul(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[6:9])
	r3 = binaryToInteger(instruction[10:13])
	global RF
	x = RF[r2] * RF[r1]
	if(x > 2^16):
		RF[-4] = 1
	else:
		RF[r3] = x
	programCounter = programCounter + 1

def div(instruction):
	r1 = binaryToInteger(instruction[6:9])
	r2 = binaryToInteger(instruction[10:13])
	global RF
	RF[0] = int(RF[r1]/RF[r2])
	RF[1] = RF[r1] - (RF[r2]*RF[0])
	programCounter = programCounter + 1

def rightS(instruction):
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[4:12])
	global RF
	RF[r1] = RF[r1] / (2 ** imm)
	programCounter = programCounter + 1;


def leftS(instruction):
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[4:12])
	global RF
	RF[r1] = RF[r1] * (2 ** imm)
	programCounter = programCounter + 1;

def exor(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[6:9])
	r3 = binaryToInteger(instruction[10:13])
	global RF
	RF[r3] = RF[r2] ^ RF[r1]
	programCounter = programCounter + 1


def ore(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[6:9])
	r3 = binaryToInteger(instruction[10:13])
	global RF
	RF[r3] = RF[r2] | RF[r1]
	programCounter = programCounter + 1

def andy(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[6:9])
	r3 = binaryToInteger(instruction[10:13])
	global RF
	RF[r3] = RF[r2] & RF[r1]
	programCounter = programCounter + 1

def invert(instruction):
	r1 = binaryToInteger(instruction[6:9])
	r2 = binaryToInteger(instruction[10:13])
	global RF
	RF[r2] = ~RF[r1]
	programCounter = programCounter + 1

def cmp(instruction):
	r1 = binaryToInteger(instruction[6:9])
	r2 = binaryToInteger(instruction[10:13])
	global RF
	if(RF[r1] == RF[R2]):
		RF[-1] = 1
	if(RF[r1] > RF[R2]):
		RF[-2] = 1
	if(RF[r1] < RF[R2]):
		RF[-3] = 1
	programCounter = programCounter + 1

def unconJmp(instruction):
	addr = binaryToInteger(instruction[4:12])
	programCounter = addr


def lessJmp(instruction):
	addr = binaryToInteger(instruction[4:12])
	if(RF[-3] ==1):
		programCounter = addr
	else:
		programCounter = programCounter + 1

def greaterJmp(instruction):
	addr = binaryToInteger(instruction[4:12])
	if(RF[-2] == 1):
		programCounter = addr
	else:
		programCounter = programCounter + 1

def equalJmp(instruction):
	addr = binaryToInteger(instruction[4:12])
	if(RF[-1] ==1):
		programCounter = addr
	else:
		programCounter = programCounter + 1

def hlt():
	global halted
	halted = True
	
while(not halted):
	instruction = getData(memory, programCounter)
	execute(instruction)
	dump(programCounter)
	dump(RF)
