import sys
import matplotlib.pyplot as plt
import math
from binary_fractions import Binary

cycleCount = 0
clocks = []
memAddr = []
MEM = [0] * 256
programCounter = 0
halted = False
RF = [0] * 11 #0,1,2,3,4,5,6,v,l,g,e
Exponents = [0] * 7
flagOp = False
floating = [0] * 7
def initialize(memory):
	listy = sys.stdin.read().split("\n")
	listy = list(filter(None, listy))
	count = 0
	for x in listy:
		memory[count] = x
		count = count + 1
	return len(listy)

programLength = initialize(MEM)

def getData(memory, PC):
	return memory[programCounter]

def execute(instruction):
	opcode = instruction[0:5]
	notOpcode = instruction[5:]
	global cycleCount
	clocks.append(cycleCount)
	memAddr.append(programCounter)
	match opcode:
		case '00000':
			Fadd(notOpcode)
		case '00001':
			Fsub(notOpcode)
		case '00010':
			MovFImm(notOpcode)
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
			hlt()
	cycleCount = cycleCount + 1

def integerToBinary16bit(inty):
	return '{0:016b}'.format(inty) 


def integerToBinary8bit(inty):
	return '{0:08b}'.format(inty) 


def binaryToInteger(bin):
	return int(bin, 2)
def getVariable(addr):
	return MEM[addr + programLength]
def exptoBinary(val):
    try:
        return '{0:03b}'.format(val)
    except:
        return '{0:03b}'.format(int(val[1:])) 

def ftoBinary(val):
    val = float(val[1:])
    m,e = math.frexp(val)
    s = '00000000'
    b = str(Binary(m))[4:]
    if(len(b) == 0):
    	b = '00000'
    if(len(b) == 1):
        b = b + '0000'
    if(len(b) == 2):
        b = b + '000'
    if(len(b) == 3):
        b = b + '00'
    if(len(b) == 4):
        b = b + '0'
    s = s + exptoBinary(e) + b
    return s

def Fadd(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter, flagOp
	temp = RF[r2] + RF[r1]
	if(temp > 2**16):
		flagOp = True
		RF[-4] = 1
	else:
		RF[r3] = temp
		floating[r3] = 1
	programCounter = programCounter + 1


def Fsub(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter, flagOp
	if(RF[r2] > RF[r1]):
		RF[r3] = 0
		RF[-4] = 1
		flagOp = True
	else:
		RF[r3] = RF[r2] + RF[r1]
		floating[r3] = 1
	programCounter = programCounter + 1

def add(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter, flagOp
	temp = RF[r2] + RF[r1]
	if(temp > 2**16):
		flagOp = True
		RF[-4] = 1
	else:
		RF[r3] = temp
	programCounter = programCounter + 1

def sub(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter, flagOp
	if(RF[r2] > RF[r1]):
		RF[r3] = 0
		RF[-4] = 1
		flagOp = True
	else:
		RF[r3] = RF[r2] + RF[r1]
	programCounter = programCounter + 1

def movI(instruction):
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[3:11])
	global RF, programCounter
	RF[r1] = imm
	programCounter = programCounter + 1;
	floating[r1] = 0

def MovFImm(instruction):
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[3:11])
	global RF, programCounter
	RF[r1] = imm
	floating[r1] = 1
	programCounter = programCounter + 1;

def movR(instruction):
	r1 = binaryToInteger(instruction[5:8])
	r2 = binaryToInteger(instruction[8:11])
	global RF, programCounter
	if(r1 == 7):
		temp = binaryToInteger(str(RF[-4]) + str(RF[-3]) + str(RF[-2]) + str(RF[-1]))
		RF[r2] = temp
	else:
		RF[r2] = RF[r1]
	programCounter = programCounter + 1
	floating[r2] = 0

def load(instruction):
	r1 = binaryToInteger(instruction[0:3])
	addr = binaryToInteger(instruction[3:11])
	global MEM, RF, programCounter
	RF[r1] = MEM[addr]
	programCounter = programCounter + 1
	clocks.append(cycleCount)
	memAddr.append(addr)
	floating[r1] = 0

def store(instruction):
	r1 = binaryToInteger(instruction[0:3])
	addr = binaryToInteger(instruction[3:11])
	global MEM, RF, programCounter
	MEM[addr] = RF[r1] 
	programCounter = programCounter + 1
	clocks.append(cycleCount)
	memAddr.append(addr)

def mul(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter, flagOp
	x = RF[r2] * RF[r1]
	if(x > 2**16):
		RF[-4] = 1
		flagOp = True
	else:
		RF[r3] = x
	programCounter = programCounter + 1

def div(instruction):
	r1 = binaryToInteger(instruction[5:8])
	r2 = binaryToInteger(instruction[8:11])
	global RF, programCounter
	RF[0] = int(RF[r1]/RF[r2])
	RF[1] = RF[r1] - (RF[r2]*RF[0])
	programCounter = programCounter + 1

def rightS(instruction):
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[3:11])
	global RF, programCounter
	RF[r1] = RF[r1] / (2 ** imm)
	programCounter = programCounter + 1;


def leftS(instruction):
	r1 = binaryToInteger(instruction[0:3])
	imm = binaryToInteger(instruction[3:11])
	global RF
	RF[r1] = RF[r1] * (2 ** imm)
	programCounter = programCounter + 1;

def exor(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter
	RF[r3] = RF[r2] ^ RF[r1]
	programCounter = programCounter + 1


def ore(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter
	RF[r3] = RF[r2] | RF[r1]
	programCounter = programCounter + 1

def andy(instruction):
	r1 = binaryToInteger(instruction[2:5])
	r2 = binaryToInteger(instruction[5:8])
	r3 = binaryToInteger(instruction[8:11])
	global RF, programCounter
	RF[r3] = RF[r2] & RF[r1]
	programCounter = programCounter + 1

def invert(instruction):
	r1 = binaryToInteger(instruction[5:8])
	r2 = binaryToInteger(instruction[8:11])
	global RF, programCounter
	RF[r2] = ~RF[r1]
	programCounter = programCounter + 1

def cmp(instruction):
	r1 = binaryToInteger(instruction[5:8])
	r2 = binaryToInteger(instruction[8:11])
	global RF, programCounter, flagOp
	if(RF[r1] == RF[r2]):
		RF[-1] = 1
	if(RF[r1] > RF[r2]):
		RF[-2] = 1
	if(RF[r1] < RF[r2]):
		RF[-3] = 1
	flagOp = True
	programCounter = programCounter + 1

def unconJmp(instruction):
	global programCounter
	addr = binaryToInteger(instruction[3:11])
	programCounter = addr


def lessJmp(instruction):
	global programCounter
	addr = binaryToInteger(instruction[3:11])
	if(RF[-3] ==1):
		programCounter = addr
	else:
		programCounter = programCounter + 1

def greaterJmp(instruction):
	global programCounter
	addr = binaryToInteger(instruction[3:11])
	if(RF[-2] == 1):
		programCounter = addr
	else:
		programCounter = programCounter + 1

def equalJmp(instruction):
	global programCounter
	addr = binaryToInteger(instruction[3:11])
	if(RF[-1] ==1):
		programCounter = addr
	else:
		programCounter = programCounter + 1

def hlt():
	global halted
	halted = True

def dumpPC(pc):
	print(integerToBinary8bit(pc), end = " ")

def dumpRF(rf):
	counter = 0
	for x in rf[0:7]:
		if(floating[counter] == 1):
			print(ftoBinary(x), end=" ")
		else:
			print(integerToBinary16bit(x), end =" ")
	print("000000000000" + str(rf[-4]) + str(rf[-3]) + str(rf[-2]) + str(rf[-1]))

def dumpMEM(memory):
	for x in memory[0:programLength]:
		print(x)
	for x in memory[programLength:]:
		print(integerToBinary16bit(x))
		

while(not halted):
	oldFlags = RF[-4:]
	oldPC = programCounter
	instruction = getData(MEM, programCounter)
	execute(instruction)
	if(flagOp == False):
		RF[-4] = 0
		RF[-3] = 0
		RF[-2] = 0
		RF[-1] = 0
	flagOp = False
	dumpPC(oldPC)
	dumpRF(RF)

dumpMEM(MEM)
plt.scatter(clocks, memAddr)
plt.show()