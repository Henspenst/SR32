# SR32 Specification
- [SR32 Specification](#sr32-specification)
  - [1 Introduction](#1-introduction)
    - [1.0 Overview](#10-overview)
    - [1.1 Normative Language](#11-normative-language)
    - [1.2 Reservations and Illegal instructions](#12-reservations-and-illegal-instructions)
  - [2 Architecture](#2-architecture)
    - [2.1 Data Model](#21-data-model)
    - [2.2 Integer Representation](#22-integer-representation)
    - [2.3 Registers](#23-registers)
    - [2.4 Program Counter](#24-program-counter)
    - [2.5 ALU](#25-alu)
    - [2.6 Control and Status Registers](#26-control-and-status-registers)
  - [3 Instruction Set](#3-instruction-set)
    - [3.1 Instruction Formats](#31-instruction-formats)
      - [Format A](#format-a)
      - [Format B](#format-b)
      - [Format C](#format-c)
      - [Format D](#format-d)
    - [3.2 Instructions](#32-instructions)
      - [0x00 NOP](#0x00-nop)
      - [0x01 ALU](#0x01-alu)
      - [0x02 ALUI](#0x02-alui)
      - [0x03 LDR](#0x03-ldr)
      - [0x04 LDI](#0x04-ldi)
      - [0x05 STR](#0x05-str)
      - [0x06 SET](#0x06-set)
      - [0x07 BRA](#0x07-bra)
  - [4 Extensions](#4-extensions)

## 1 Introduction

### 1.0 Overview

This document defines the architecture and required behaviour of a compatible
SR32 processor.

A compatible implementation MUST conform to all requirements marked as
mandatory by this specification.

Where this specification does not define a behaviour, an implementation MAY
choose its own behaviour. Such implementation-defined behaviour MUST NOT
contradict any requirement of this specification.

### 1.1 Normative Language

The following terms have specific meanings when used in this specification:

| Term | Meaning |
|------|---------|
| **WORD** | A 32 bit value. |
| **HALF WORD** | A 16 bit value. |
| **BYTE** | An 8 bit value. |
| **MUST** | The requirement is mandatory. A compatible implementation MUST satisfy it. |
| **MUST NOT** | The requirement is prohibited. A compatible implementation MUST NOT do it. |
| **SHOULD** | The requirement is recommended. An implementation MAY deviate from it when there is an implementation-specific reason to deviate. |
| **SHOULD NOT** | The behaviour is discouraged. An implementation may still use it when there is a valid reason. |
| **MAY** | The behaviour is optional. An implementation may choose whether or not to support it. |
| **PC** | The program counter, implemented as r31. |
| **Rd** | The 5-bit register field occupying bits 9–13, when present. Its meaning is defined by the individual instruction. |
| **Rs1** | The 5-bit register field occupying bits 14–18, when present. Its meaning is defined by the individual instruction. |
| **Rs2** | The 5-bit register field occupying bits 19–23, when present. Its meaning is defined by the individual instruction. |
| **CSR(s)** | Control and status register(s) |

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are
normative and are used to define compatibility requirements.

### 1.2 Reservations and Illegal instructions

The isa specification has a number of reserved spaces in the opcode field and function field.
If an instruction not supported by the specific isa implementation is attempted to executed the cpu MUST halt or execute a trap.

## 2 Architecture

### 2.1 Data Model

The processor MUST use a 32-bit data width and a 32-bit address width.

- A byte MUST consist of 8 bits.
- A half word MUST consist of 16 bits.
- If a half word is described as "upper", it refers to bits 16–31 of a word.
- If a half word is described as "lower", it refers to bits 0–15 of a word.

The processor MUST use big-endian byte ordering. For a multi-byte value,
the most significant byte MUST be stored at the lowest memory address.

For example, the 32-bit value `0x12345678` stored at address `0x00001000`
MUST be represented as:

| Address | Value |
|---------|-------|
| `0x00001000` | `0x12` |
| `0x00001001` | `0x34` |
| `0x00001002` | `0x56` |
| `0x00001003` | `0x78` |

The processor MUST use byte addressing. Each memory address refers to exactly
one byte of memory.

The architectural data width and address width MUST NOT be interpreted as
requirements for the physical memory interface. An implementation MAY use a
different internal or external memory bus width, provided that the behaviour
visible to software conforms to this specification.

### 2.2 Integer Representation

Register values have no given signness, each instruction and variant chose to interpret data as signed or unsigned.

A two's complement integer has a value range from -2<sup>N−1</sup> to 2<sup>N−1</sup>−1.
The most significant bit is a sign bit that indicates whether the value is negative. The negative of a value can be obtained by inverting all the bits then adding 1. This is what sign extended refers to.

Integer arithmetic MUST wrap on overflow modulo 2<sup>32</sup>. Exceptions, traps or cpu halts MUST not be generated.


### 2.3 Registers

The processor MUST provide 32 programmer-visible registers:

- `r0` MUST always contain the value `0`.
- Reads from `r0` MUST return `0`.
- Writes to `r0` MUST NOT change its value.
- `r1`–`r30` MUST be general-purpose registers with no other architecturally defined functions.
- `r31` MUST be the program counter, therefore any reads from r31 return the address of the current instruction.

The specification does not require any additional programmer-visible registers.

An implementation MAY use internal registers such as an instruction register,
memory address register, or memory data register.

***Implementation note***

Additional internal registers do not form part of the programmer-visible
architecture and therefore do not affect compatibility.

### 2.4 Program Counter

`r31` is the program counter.
At the beginning of instruction execution r31 MUST contain the address of the instruction being executed.
All source operands MUST be read before the destination register is written.
The program counter MUST be incremented by 4 at the end of each execute step unless:
- The instruction executed wrote to r31.
- The instruction was a branch instruction which took the branch.

Writing a value to `r31` changes the program counter to that value.
The next fetch operation MUST be executed at the resulting value in r31.

If a value is written to r31 the least 2 significant bits MUST be cleared and set to 0;
Therefore program counter address MUST be divisible by 4.

An instruction which writes to `r31` MUST follow the program-counter behaviour
defined by this section.



### 2.5 ALU

The processor MUST support the following ALU operations:

| Function | Operation |
|----------|-----------|
| `0` | Add |
| `1` | Subtract |
| `2` | Boolean AND |
| `3` | Boolean OR |
| `4` | Boolean XOR |
| `5` | Logical shift left |
| `6` | Logical shift right |
| `7` | Arithmetic shift right |

The specification defines the required operations and their results. It does
not require a particular internal ALU implementation.

- Addition and subtraction MUST wrap around when an overflow occurs modulo 2<sup>32</sup>.
- For shift operations, only bits 0–4 of the shift operand are used.
- Bits 5–31 of the shift operand MUST be ignored.
- Arithmetic shift right MUST replicate the sign bit.

***Implementation note***

An implementation MAY map the 3-bit function field directly to the ALU
operation because the function values correspond directly to the operations
defined above.


### 2.6 Control and Status Registers

Control and Status Registers (CSR's) are OPTIONAL.
An implementation may chose to instead halt if an illegal instruction is detected.
An implementation that does support CSR's MUST conform fully to this section.

*Note: currently this section is a placeholder.*

// Placeholder.

## 3 Instruction Set

### 3.1 Instruction Formats

All instructions are 32 bits wide.

Bits 0–5 contain the opcode for every instruction.

The processor defines four instruction formats. The interpretation of the
remaining bits depends on the instruction format.

The exact interpretation of each field is defined by the individual
instruction format below. The processor MUST follow these formats.

#### Format A

| Bits | Field | Width |
|------|-------|------:|
| 0–5 | Opcode | 6 |
| 6–8 | Function | 3 |
| 9–13 | `Rd` | 5 |
| 14–18 | `Rs1` | 5 |
| 19–23 | `Rs2` | 5 |
| 24–31 | Reserved | 8 |

#### Format B

| Bits | Field | Width |
|------|-------|------:|
| 0–5 | Opcode | 6 |
| 6–8 | Function | 3 |
| 9–13 | `Rd` | 5 |
| 14–18 | `Rs1` | 5 |
| 19–31 | Immediate | 13 |


#### Format C

| Bits | Field | Width |
|------|-------|------:|
| 0–5 | Opcode | 6 |
| 6–31 | Reserved | 26 |

#### Format D

| Bits | Field | Width |
|------|-------|------:|
| 0–5 | Opcode | 6 |
| 6–8 | Function | 3 |
| 9–13 | `Rd` | 5 |
| 14–15 | Reserved | 2 |
| 16–31 | Immediate | 16 |

### 3.2 Instructions

The base instruction set contains 8 instructions.

The base instruction set uses opcode values `0x00`–`0x07`. The remaining
opcode values are reserved for future extensions.

Unless otherwise specified, immediate fields MUST be sign extended
to 32 bits using two's complement representation before use.

Individual instructions MAY define a different interpretation of their
immediate field.


#### 0x00 NOP

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| No operation | `NOP` | `0x00` | C| N/A |

The `NOP` instruction MUST have no architecturally visible effect other
than the normal progression of the program counter.

#### 0x01 ALU

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Arithmetic / Logic | `ALU` | `0x01` | A | `Rd = Rs1 op Rs2` |

The `ALU` instruction uses the 3-bit Function field in bits `6`–`8` to
select the operation defined in Section 2.5.

The processor MUST implement all eight operations defined in Section 2.5.

The result of the selected operation MUST be written to `Rd`.

#### 0x02 ALUI

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Arithmetic / Logic Immediate | `ALUI` | `0x02` | B | `Rd = Rs1 op Immediate` |

The 13-bit Immediate field MUST be sign-extended to 32 bits before being
used by the `ALUI` instruction.

The `ALUI` instruction uses the 3-bit Function field in bits `6`–`8` to
select the operation defined in Section 2.5.

The processor MUST implement all eight operations defined in Section 2.5.

The result of the selected operation MUST be written to `Rd`.

#### 0x03 LDR

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Load | `LDR` | `0x03` | B | `Rd = read(Rs1 + Immediate)` |

The 13-bit Immediate field MUST be sign-extended to 32 bits before being
added to `Rs1`.

The `LDR` instruction uses the 3-bit Function field in bits `6`–`8` to
select the size of data loaded.

| Function | Operation | Pseudocode |
|---------:|-----------|--------|
| `0` | Load word | 16 bit value |
| `1` | Load lower half word | 16 bit value |
| `2` | Load byte | 8 bit value |
| `3` | Load upper half word | (16 bit value << 16) \| (existing value & 0xffff) |
| `4` | Load lower half word sign extend | signextend(16 bit value) |
| `5` | Load byte sign extend| signextend(8 bit value) |
| `6` | Reserved |  |
| `7` | Reserved |  |

#### 0x04 LDI

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Load Immediate | `LDI` | `0x04` | D | `Rd = immediate` |


The `LDI` instruction uses the 3-bit Function field in bits `6`–`8` to
select the size of data loaded.

| Function | Operation | Pseudocode |
|---------:|-----------|-----------|
| `0` | Load lower half word | Rd = immediate |
| `1` | Load upper half word | Rd = immediate << 16 |
| `2` | Load lower sign extended | Rd = signextend(immediate) |
| `3` | Load upper (keep data) | Rd = (Rd & 0xffff) \| immediate << 16 |
| `4` | Load lower (keep data) | Rd = (Rd & 0xffff0000) \| (immediate) |
| `5` | Reserved |
| `6` | Reserved |
| `7` | Reserved |

#### 0x05 STR

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Store | `STR` | `0x05` | B | `memory[Rs1 + immediate] = Rd` |


The `STR` instruction uses the 3-bit Function field in bits `6`–`8` to
select the size of data stored.

| Function | Operation |
|---------:|-----------|
| `0` | Store word |
| `1` | Store half word |
| `2` | Store byte |
| `3` | Reserved |
| `4` | Reserved |
| `5` | Reserved |
| `6` | Reserved |
| `7` | Reserved |

#### 0x06 SET

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Set | `SET` | `0x06` | A | `Rd = 1 if Rs1 cond Rs2 else 0` |


The `SET` instruction uses the 3-bit Function field in bits `6`–`8` to
select the condition.

| Function | Operation |
|---------:|-----------|
| `0` | Equal |
| `1` | Not Equal |
| `2` | Less than signed |
| `3` | Greater or equal signed |
| `4` | Less than unsigned |
| `5` | Greater or equal unsigned |
| `6` | Reserved |
| `7` | Reserved |

#### 0x07 BRA

| Name | Mnemonic | Opcode | Format | Pseudocode |
|------|----------|-------:|:------:|------------|
| Branch | `BRA` | `0x07` | B | `pc = pc + immediate if Rd cond Rs1` |


The `BRA` instruction uses the 3-bit Function field in bits `6`–`8` to
select the condition to do the branch check.

***Note***
For the purposes of this instruction Rd is not the destination register, instead the first of the 2 comparison registers, rs1 being the second.

| Function | Operation |
|---------:|-----------|
| `0` | Equal |
| `1` | Not Equal |
| `2` | Less than signed |
| `3` | Greater or equal signed |
| `4` | Less than unsigned |
| `5` | Greater or equal unsigned |
| `6` | Reserved |
| `7` | Reserved |

## 4 Extensions

// Placeholder