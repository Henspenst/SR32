import argparse
import sys
from dataclasses import dataclass

@dataclass
class sourceLocation:
    filename: str
    line: int
    column: int

@dataclass
class token:
    type: str
    text: str
    location: sourceLocation

@dataclass
class statement:
    kind: str
    name: str | None
    operands: list
    location: sourceLocation
    length: int = 0




aliases = {
    # ALU
    "add":  {"output": [["alu",  "f0", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sub":  {"output": [["alu",  "f1", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "and":  {"output": [["alu",  "f2", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "or":   {"output": [["alu",  "f3", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "xor":  {"output": [["alu",  "f4", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sll":  {"output": [["alu",  "f5", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "slr":  {"output": [["alu",  "f6", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sar":  {"output": [["alu",  "f7", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},

    # ALUI
    "addi": {"output": [["alui", "f0", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "subi": {"output": [["alui", "f1", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "andi": {"output": [["alui", "f2", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "ori":  {"output": [["alui", "f3", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "xori": {"output": [["alui", "f4", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "slli": {"output": [["alui", "f5", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "slri": {"output": [["alui", "f6", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},
    "sari": {"output": [["alui", "f7", "$rd", "$rs", "$imm"]], "input": ["rd", "rs", "imm"], "inputTypes": ["register", "register", "imm13"]},

    # Move
    "mov":  {"output": [["alu", "f0", "$rd", "$rs", "r0"]], "input": ["rd", "rs"], "inputTypes": ["register", "register"]},

    # Load
    "load":      {"output": [["ldr", "f0", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "loadhalf":  {"output": [["ldr", "f1", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "loadbyte":  {"output": [["ldr", "f2", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "loadupper": {"output": [["ldr", "f3", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "loadshalf": {"output": [["ldr", "f4", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "loadsbyte": {"output": [["ldr", "f5", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},

    # Store
    "store":     {"output": [["str", "f0", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "storehalf": {"output": [["str", "f1", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},
    "storebyte": {"output": [["str", "f2", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"]},

    # Immediate load
    "loadimm":      {"output": [["ldi", "f0", "$rd", "$imm"]], "input": ["rd", "imm"], "inputTypes": ["register", "imm16"]},
    "loadimmupper": {"output": [["ldi", "f1", "$rd", "$imm"]], "input": ["rd", "imm"], "inputTypes": ["register", "imm16"]},
    "loadimmsigned": {"output": [["ldi", "f2", "$rd", "$imm"]], "input": ["rd", "imm"], "inputTypes": ["register", "simm16"]},
    "loadimmupperkeep": {"output": [["ldi", "f3", "$rd", "$imm"]], "input": ["rd", "imm"], "inputTypes": ["register", "imm16"]},
    "loadimmlowerkeep": {"output": [["ldi", "f4", "$rd", "$imm"]], "input": ["rd", "imm"], "inputTypes": ["register", "imm16"]},
    "loadword": {"output": [["ldi", "f1", "$rd", "$immh"], ["ldi", "f4", "$rd", "$imml"]], "input": ["rd", "immh", "imml"], "inputTypes": ["register", "imm16", "imm16"]},

    # Comparisons
    "seq":  {"output": [["set", "f0", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sne":  {"output": [["set", "f1", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "slt":  {"output": [["set", "f2", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sge":  {"output": [["set", "f3", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sltu": {"output": [["set", "f4", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},
    "sgeu": {"output": [["set", "f5", "$rd", "$rs1", "$rs2"]], "input": ["rd", "rs1", "rs2"], "inputTypes": ["register", "register", "register"]},

    # Branches
    "beq":  {"output": [["bra", "f0", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"], "relative": True},
    "bneq":  {"output": [["bra", "f1", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"], "relative": True},
    "blt":  {"output": [["bra", "f2", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"], "relative": True},
    "bge":  {"output": [["bra", "f3", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"], "relative": True},
    "bltu": {"output": [["bra", "f4", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"], "relative": True},
    "bgeu": {"output": [["bra", "f5", "$rd", "$rs", "$offset"]], "input": ["rd", "rs", "offset"], "inputTypes": ["register", "register", "imm13"], "relative": True},
}

registerAliases = {
    # Special
    "zero": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "fp": 4,

    # Arguments / return values
    "a0": 5,
    "a1": 6,
    "a2": 7,
    "a3": 8,
    "a4": 9,
    "a5": 10,
    "a6": 11,
    "a7": 12,

    # Temporaries
    "t0": 13,
    "t1": 14,
    "t2": 15,
    "t3": 16,
    "t4": 17,
    "t5": 18,
    "t6": 19,
    "t7": 20,
    "t8": 21,

    # Saved registers
    "s0": 22,
    "s1": 23,
    "s2": 24,
    "s3": 25,
    "s4": 26,
    "s5": 27,
    "s6": 28,
    "s7": 29,
    "s8": 30,

    # Program counter
    "pc": 31,

    "r0": 0,
    "r1": 1,
    "r2": 2,
    "r3": 3,
    "r4": 4,
    "r5": 5,
    "r6": 6,
    "r7": 7,
    "r8": 8,
    "r9": 9,
    "r10": 10,
    "r11": 11,
    "r12": 12,
    "r13": 13,
    "r14": 14,
    "r15": 15,
    "r16": 16,
    "r17": 17,
    "r18": 18,
    "r19": 19,
    "r20": 20,
    "r21": 21,
    "r22": 22,
    "r23": 23,
    "r24": 24,
    "r25": 25,
    "r26": 26,
    "r27": 27,
    "r28": 28,
    "r29": 29,
    "r30": 30,
    "r31": 31

}

instructions = {"nop": {"opcode": 0, "args": []},
                "alu": {"opcode": 1, "args": ["function", "register", "register", "register"]},
                "alui": {"opcode": 2, "args": ["function", "register", "register", "imm13"]},
                "ldr": {"opcode": 3, "args": ["function", "register", "register", "imm13"]},
                "ldi": {"opcode": 4, "args": ["function", "register", "imm16"]},
                "str": {"opcode": 5, "args": ["function", "register", "register", "imm13"]},
                "set": {"opcode": 6, "args": ["function", "register", "register", "register"]},
                "bra": {"opcode": 7, "args": ["function", "register", "register", "imm13"], "relative": True}
                }

def main():
    parser = argparse.ArgumentParser(description="SR32 assembler")
    parser.add_argument("input", help="Path to the .asm input file")
    parser.add_argument("output", help="Path to the .bin output file")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        print(f"Error: Could not read '{args.input}': {e}", file=sys.stderr)
        sys.exit(1)

    tokens = tokenize(source, args.input)
    #for temp in tokens:
    #    print(temp.type + ", " + temp.text)
    # print(tokens)
    tokens = tokenParser(tokens)
    tokens = solveLabels(tokens)
    tokens = solveAliases(tokens)
    output = genBinaryDict(tokens)
    output = genByteArray(output)
    try:
        with open(args.output, "wb") as outputFile:
            outputFile.write(output)
    except OSError as e:
        print(f"Error: Could not write'{args.output}': {e}", file=sys.stderr)

def removeComments(line):
    output = ""
    inComment = False
    for char in line:
        if char == "#":
            inComment = not inComment
        else:
            if not inComment:
                output += char
    return output

def checkWord(word):
    word = word.strip()
    if word in aliases:
        return("alias")
    elif word.endswith(":"):
        return("labelDef")
    elif word.startswith("/"):
        return("labelUse")
    elif word.startswith("r") and word[1:].isdigit():
        return("register")
    elif word in instructions:
        return("instruction")
    else:
        return("value")

def tokenSplit(line):
    word = ""
    output = []
    wordStart = 0
    for i, char in enumerate(line):
        if i == len(line) - 1:
            word += char
            output.append((word, checkWord(word), wordStart))
            wordStart = i + 2
        elif char == " " or char == "\t":
            output.append((word, checkWord(word), wordStart))
            word = ""
            wordStart = i + 2
        else:
            word += char
    output2 = []
    for word in output:
        if word[0].strip() != "":
            output2.append(word)
    return output2

def tokenize(source, filename):
    tokens = []

    for lineNumber, line in enumerate(source.splitlines(), start=1):
        code = removeComments(line)
        lineTokens = tokenSplit(code)

        if lineTokens:
            tokens.extend([
                token(
                    type=tokenType,
                    text=tokenText,
                    location=sourceLocation(
                        filename, lineNumber, column
                    )
                )
                for tokenText, tokenType, column in lineTokens
            ])

    return tokens

def convertValue(string):
    string = string.strip()
    return int(string, 0)

def checkValidity(token, position, instruction):
    if instruction.type == "alias":
        expected = aliases[token.text]["inputTypes"][position]
    elif instruction.type == "instruction":
        expected = instructions[token.text]["inputTypes"][position]

    if token.type == "value":
        if expected == "imm13":
            value = convertValue(token.text)
            if -4096 <= value < 4096:
                return ("true")
            else:
                return ("value incorrect")
        elif expected == "simm16":
            value = convertValue(token.text)
            if -32768 <= value < 32768:
                return("true")
            else:
                return("value incorrect")
    elif token.type == "register":
        if token.type == "register":
            value = int(token.text[1:])
            if 0 <= value <= 31:
                return("true")
            else:
                return("register incorrect")
        else:
            return("unexpected token type")
    elif token.type == "labelUse":
        if token.type == "simm16":
            return("true")
        elif token.type == "imm13":
            return("true")
        else:
            return("unexpected token type")

def tokenParser(tokens): # Needs to return a list of statements
    def isStatementStart(t):
        return t.type in {
            "labelDef",
            "instruction",
            "alias"
        }
    output = []
    i = 0
    operands = []
    while i < len(tokens):
        currentToken = tokens[i]

        if currentToken.type == "labelDef":
            output.append(
                statement(
                    kind="labelDef",
                    name=currentToken.text,
                    operands=[],
                    location=currentToken.location))
            i += 1
            operands = []
            continue

        elif currentToken.type == "alias":
            definition = aliases[currentToken.text]
            kind = "alias"
            expectedLen = len(definition["inputTypes"])
        elif currentToken.type == "instruction":
            definition = instructions[currentToken.text]
            kind = "instruction"
            expectedLen = len(definition["args"])
        else:
            pass    # IMPLEMENT error
        i += 1

        while len(operands) < expectedLen and i < len(tokens):
            nextToken = tokens[i]
            if isStatementStart(nextToken):
                break
            operands.append(nextToken)
            i += 1
        length = 0
        if kind == "instruction":
            length = 4
        elif kind == "alias":
            length = len(aliases[currentToken.text]["output"]) * 4
        output.append(
            statement(
                kind=kind,
                name=currentToken.text,
                operands=operands,
                location=currentToken.location,
                length=length
            ))
        operands = []
    return output

def solveLabels(statements):
    output = []
    labels = {}
    secondPass = []
    programCounter = 0
    for statement in statements:
        if statement.kind == "labelDef":
            if statement.name not in labels:
                labels[statement.name[:-1]] = programCounter
            else:
                pass # IMPLEMENT error
        else:
            secondPass.append(statement)
            programCounter += statement.length
    programCounter = 0
    for statement in secondPass:
        for operand in statement.operands:
            if operand.type == "labelUse":
                if statement.kind == "instruction":
                    relative = instructions[statement.name].get("relative", False)
                elif statement.kind == "alias":
                    relative = aliases[statement.name].get("relative", False)
                else:
                    relative = False

                if relative:
                    operand.text = str(labels[operand.text[1:]] - programCounter)
                else:
                    operand.text = str(labels[operand.text[1:]])

                operand.type = "value"
        output.append(statement)
        programCounter += statement.length
    return output

def solveAliases(statements):
    output = []
    for tempStatement in statements:
        if tempStatement.kind == "alias":
            if tempStatement.name not in aliases:
                pass # IMPLEMENT error
            else:
                for instruction in aliases[tempStatement.name]["output"]:
                    nextInstruction = statement(
                        kind="instruction",
                        name=instruction[0],
                        operands=[],
                        location=tempStatement.location,
                        length=4
                    )
                    for operand in instruction:
                        if operand[:1] == "$":
                            nextInstruction.operands.append(
                                tempStatement.operands[
                                    aliases[tempStatement.name]["input"].index(operand[1:])]
                            )
                        else:
                            if operand[:1] == "f":
                                nextInstruction.operands.append(token(
                                    type="function",
                                    text=operand,
                                    location=tempStatement.location
                                ))
                            elif operand in registerAliases:
                                nextInstruction.operands.append(token(
                                    type="register",
                                    text=operand,
                                    location=tempStatement.location
                                ))
                    output.append(nextInstruction)
        else:
            output.append(tempStatement)
    return output

def genBinaryDict(statements):
    output = {}
    currentAddress = 0
    for tempStatement in statements:
        line = 0
        currentShift = 6
        line += instructions[tempStatement.name]["opcode"]
        for i, operandType in enumerate(instructions[tempStatement.name]["args"]):
            operand = tempStatement.operands[i]
            if operandType == "function":
                line += int(operand.text[1:]) << currentShift
                currentShift += 3
            elif operandType == "register":
                line += registerAliases[operand.text] << currentShift
                currentShift += 5
            elif operandType == "imm13":
                value = int(operand.text) & 0x1FFF
                line |= value << currentShift
                currentShift += 13
            elif operandType == "imm16":
                line += int(operand.text) << currentShift + 2
                currentShift += 18
            else:
                pass    # IMPLEMENT error
        output[currentAddress] = (line >> 24) & 0xff
        output[currentAddress + 1] = (line >> 16) & 0xff
        output[currentAddress + 2] = (line >> 8) & 0xff
        output[currentAddress + 3] = line & 0xff
        currentAddress += 4
    return(output)

def genByteArray(data):
    startAddress = min(data)
    endAddress = max(data)
    output = bytearray(endAddress - startAddress + 1)
    for address, value in data.items():
        output[address - startAddress] = value
    return bytes(output)

if __name__ == "__main__":
    main()