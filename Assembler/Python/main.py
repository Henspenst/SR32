instructions = """

loadimm r1  104
store r1 r0 -1

loadimm r1  101
store r1 r0 -1

loadimm r1  108
store r1 r0 -1

loadimm r1  108
store r1 r0 -1

loadimm r1  111
store r1 r0 -1
"""

aliases = {
    # ALU
    "add":  {"output": [["alu",  "f0", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sub":  {"output": [["alu",  "f1", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "and":  {"output": [["alu",  "f2", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "or":   {"output": [["alu",  "f3", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "xor":  {"output": [["alu",  "f4", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sll":  {"output": [["alu",  "f5", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "slr":  {"output": [["alu",  "f6", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sar":  {"output": [["alu",  "f7", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},

    # ALUI
    "addi": {"output": [["alui", "f0", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "subi": {"output": [["alui", "f1", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "andi": {"output": [["alui", "f2", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "ori":  {"output": [["alui", "f3", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "xori": {"output": [["alui", "f4", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "slli": {"output": [["alui", "f5", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "slri": {"output": [["alui", "f6", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},
    "sari": {"output": [["alui", "f7", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"]},

    # Move
    "mov":  {"output": [["alu", "f0", "$rd", "$rs", "r0"]], "input": ["rd", "rs"]},

    # Load
    "load":      {"output": [["ldr", "f0", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "loadhalf":  {"output": [["ldr", "f1", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "loadbyte":  {"output": [["ldr", "f2", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "loadupper": {"output": [["ldr", "f3", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "loadshalf": {"output": [["ldr", "f4", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "loadsbyte": {"output": [["ldr", "f5", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},

    # Store
    "store":     {"output": [["str", "f0", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "storehalf": {"output": [["str", "f1", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "storebyte": {"output": [["str", "f2", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},

    # Immediate load
    "loadimm":      {"output": [["ldi", "f0", "$rd", "$imm"]], "input": ["rd", "imm"]},
    "loadimmupper": {"output": [["ldi", "f1", "$rd", "$imm"]], "input": ["rd", "imm"]},
    "loadimmsigned": {"output": [["ldi", "f2", "$rd", "$imm"]], "input": ["rd", "imm"]},
    "loadimmupperkeep": {"output": [["ldi", "f3", "$rd", "$imm"]], "input": ["rd", "imm"]},
    "loadimmlowerkeep": {"output": [["ldi", "f4", "$rd", "$imm"]], "input": ["rd", "imm"]},
    "loadword": {"output": [["ldi", "f0", "$rd", "$imml"], ["ldi", "f4", "$rd", "$immh"]], "input": ["rd", "immh", "imml"]},

    # Comparisons
    "seq":  {"output": [["set", "f0", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sne":  {"output": [["set", "f1", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "slt":  {"output": [["set", "f2", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sge":  {"output": [["set", "f3", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sltu": {"output": [["set", "f4", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},
    "sgeu": {"output": [["set", "f5", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"]},

    # Branches
    "beq":  {"output": [["bra", "f0", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "bneq":  {"output": [["bra", "f1", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "blt":  {"output": [["bra", "f2", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "bge":  {"output": [["bra", "f3", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "bltu": {"output": [["bra", "f4", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
    "bgeu": {"output": [["bra", "f5", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"]},
}

formats = {"nop": [],
           "alu": ["function", "reg", "reg", "reg", "reserved8"],
           "alui": ["function", "reg", "reg", "immediate13"],
           "ldr": ["function", "reg", "reg", "immediate13"],
           "ldi": ["function", "reg", "reserved2", "immediate16"],
           "str": ["function", "reg", "reg", "immediate13"],
           "set": ["function", "reg", "reg", "reg", "reserved8"],
           "bra": ["function", "reg", "reg", "immediate13"]}

instructionID = {"nop": 0,
                "alu": 1,
                "alui": 2,
                "ldr": 3,
                "ldi": 4,
                "str": 5,
                "set": 6,
                "bra": 7,}

def signBinary(number, bits):
    minimum = -(2 ** (bits - 1))
    maximum = (2 ** (bits - 1)) - 1

    if number < minimum or number > maximum:
        raise ValueError("Number is outside signed range")

    if number < 0:
        number = (2 ** bits) + number

    return bin(number)[2:].zfill(bits)

def tokeniser(instructions):
    tokens = []
    for line in instructions.splitlines():
        line = line.split("#", 1)[0].strip().lower() # Splitting and removing comments
        if line:
            tokens.append(line.split()) # Removing empty lines
    return tokens


def instructioniser(tokens): # Replaces pseudo instructions like ADD for their explicit versions.
    output = []
    for line in tokens:
        mneumonic = line[0]
        if mneumonic not in aliases:
            output.append(line)
        else:
            alias = aliases[mneumonic]
            arguments = line[1:]
            parameters = {}
            for i in range(len(alias["input"])):
                parameters[alias["input"][i]] = arguments[i]

            for instruction in alias["output"]:
                newLine = []

                for token in instruction:
                    if token[:1] == "$":
                        parameter = token[1:]
                        newLine.append(parameters[parameter])
                    else:
                        newLine.append(token)
                output.append(newLine)
    return output

def labeller(tokens):
    labels = {}
    programCounter = 0
    newLines = []
    for line in tokens:
        newLine = []
        for token in line:
            if token.endswith(":"):
                label = token[:-1]
                if label in labels:
                    raise ValueError("Duplicate labels: " + label)
                labels[label] = programCounter
            else:
                newLine.append(token)
        if newLine:
            newLines.append(newLine)
            programCounter += 4

    output = []
    programCounter = 0
    for line in newLines:
        newLine = []
        for token in line:
            if token.startswith("/"):
                label = token[1:]
                if label not in labels:
                    raise ValueError("Label not defined: " + label)
                offset = labels[label] - programCounter
                newLine.append(offset)
            else:
                newLine.append(token)
        output.append(newLine)
        programCounter += 4
    return output


def binary(tokens):
    output = {}
    programCounter = 0
    for line in tokens:
        lineBinary = ""
        parameters = []
        parameters.append(bin(int(instructionID[line[0]]))[2:].zfill(6))

        arg_index = 1
        for tokenType in formats[line[0]]:
            if tokenType == "function":
                func_val = int(line[arg_index][1:])
                if func_val > 7 or func_val < 0:
                    raise ValueError("Function is out of range: " + " ".join(line))
                parameters.append(bin(func_val)[2:].zfill(3))
                arg_index += 1
            elif tokenType == "reg":
                register = int(line[arg_index][1:])
                if register < 0 or register > 31:
                    raise ValueError("Register out of range: " + " ".join(line))
                parameters.append(bin(register)[2:].zfill(5))
                arg_index += 1
            elif tokenType == "immediate13":
                value = int(line[arg_index])
                parameters.append(signBinary(value, 13))
                arg_index += 1
            elif tokenType == "immediate16":
                value = int(line[arg_index])
                parameters.append(signBinary(value, 16))
                arg_index += 1
            elif tokenType == "reserved2":
                parameters.append("00")
            elif tokenType == "reserved8":
                parameters.append("00000000")

        for parameter in reversed(parameters):
            lineBinary += parameter

        output[programCounter] = lineBinary.zfill(32)
        programCounter += 4
    return output

def writeFile(binary):
    pass


tokens = tokeniser(instructions)
tokens = instructioniser(tokens)
tokens = labeller(tokens)
print(tokens)
binary = binary(tokens)
print(binary)