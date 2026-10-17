#include <cstdint>
#include <iostream>
#include "cpu.h"
#include<cmath>

#include <unordered_map>



       bool CPU::readCSRS(uint16_t csr, uint32_t& data) {
           auto it = csrs.find(csr);

           if (it == csrs.end()) {
               exception(1, csr);
               return false;
           }

           data = it->second;
           return true;
       }

       bool CPU::writeCSRS(uint16_t csr, uint32_t data) {    // Implement proper permissions
           auto it = csrs.find(csr);

           if (it == csrs.end()) {
               exception(1, csr);
               return false;
           }

           it->second = data;
           return true;
       }







       uint32_t CPU::signExtend(uint32_t data, int widthIn) {
           uint32_t mask = (1u << widthIn) - 1;
           data &= mask;

           if (data & (1u << (widthIn - 1)))
               data |= ~mask;

           return data;
       }

       void CPU::exception(uint8_t cause, uint32_t value) {
           uint32_t tempData = 0;
           uint32_t exceptionPC = programCounter;
           if (readCSRS(0x400, tempData))
           {
               programCounter = tempData + cause * 4;
           }

           writeCSRS(0x401, cause);
           writeCSRS(0x402, value);
           writeCSRS(0x700, exceptionPC);
       }

       uint32_t CPU::readRegister(int reg) {
           if (reg == 0)
               return 0;

           else if (reg == 31)
               return programCounter;

           return registers[reg];
       }

       void CPU::writeRegister(uint8_t reg, uint32_t data) {
           if (reg >= 1 && reg <= 30) {
               registers[reg] = data;
           }
           else if (reg == 31) {
               programCounter = data & 0xfffffffc;
           }
       }

       void CPU::fetch() {
           instructionReg = readMemory(programCounter, 4);
       }

       uint32_t CPU::alu(uint32_t inputA, uint32_t inputB, int operation) {
           switch (operation) {
           case 0:
               return inputA + inputB;
           case 1:
               return inputA - inputB;
           case 2:
               return inputA & inputB;
           case 3:
               return inputA | inputB;
           case 4:
               return inputA ^ inputB;
           case 5:
               return inputA << (inputB & 0x1f);
           case 6:
               return inputA >> (inputB & 0x1f);
           case 7:
               return static_cast <uint32_t> (static_cast <int32_t> (inputA) >> (inputB & 0x1f));
           default:
               return 0;
           }
       }

       void CPU::execute() {
           int opcode = instructionReg & 0x3f;
           int
               function = (instructionReg >> 6) & 0x7;
           int rd = (instructionReg >> 9) & 0x1f;
           int rs1 = (instructionReg >> 14) & 0x1f;
           int rs2 = (instructionReg >> 19) & 0x1f;
           uint32_t immediate13 = (instructionReg >> 19);
           uint32_t immediate16 = (instructionReg >> 16);
           pcChanged = false;
           exceptionTaken = false;
           switch (opcode) {
           case 0x00: // nop
               break;
           case 0x01: // alu
               writeRegister(rd, alu(readRegister(rs1), readRegister(rs2), function));
               if (rd == 31) {
                   pcChanged = true;
               }
               break;
           case 0x02: // alui
               writeRegister(rd, alu(readRegister(rs1), immediate13, function));
               if (rd == 31) {
                   pcChanged = true;
               }
               break;
           case 0x03: // ldr
           {
               uint32_t data = 0;
               switch (function) {
               case 0:
                   data = readMemory(readRegister(rs1) + signExtend(immediate13, 13), 4);
                   break;
               case 1:
                   data = readMemory(readRegister(rs1) + signExtend(immediate13, 13), 2);
                   break;
               case 2:
                   data = readMemory(readRegister(rs1) + signExtend(immediate13, 13), 1);
                   break;
               case 3:
                   data = (readMemory(readRegister(rs1) + signExtend(immediate13, 13), 2) << 16);
                   break;
               case 4:
                   data = signExtend(readMemory(readRegister(rs1) + signExtend(immediate13, 13), 2), 16);
                   break;
               case 5:
                   data = signExtend(readMemory(readRegister(rs1) + signExtend(immediate13, 13), 1), 8);
                   break;
               default:
                   exception(1, instructionReg);
                   pcChanged = true;
                   exceptionTaken = true;
                   break;
               }
               if (not exceptionTaken) {
                   writeRegister(rd, data);
               }
               if (rd == 31) {
                   pcChanged = true;
               }
               break;
           }
           case 0x04: // ldi
           {
               uint32_t data = 0;
               switch (function) {
               case 0:
                   data = immediate16;
                   break;
               case 1:
                   data = immediate16 << 16;
                   break;
               case 2:
                   data = signExtend(immediate16, 16);
                   break;
               case 3:
                   data = (readRegister(rs1) & 0xffff) | (immediate16 << 16);
                   break;
               case 4:
                   data = (readRegister(rs1) & 0xffff0000) | immediate16;
                   break;
               default:
                   exception(1, instructionReg);
                   exceptionTaken = true;
                   pcChanged = true;
                   break;
               }
               if (not exceptionTaken) {
                   writeRegister(rd, data);
               }
               break;
           }
           case 0x05: // str
           {
               uint32_t data = 0;
               switch (function) {
               case 0:
                   writeMemory(readRegister(rs1) + immediate13, readRegister(rd), 4);
                   break;
               case 1:
                   writeMemory(readRegister(rs1) + immediate13, readRegister(rd) & 0xffff, 2);
                   break;
               case 2:
                   writeMemory(readRegister(rs1) + immediate13, readRegister(rd) & 0xff, 1);
                   break;
               default:
                   exception(1, instructionReg);
                   exceptionTaken = true;
                   pcChanged = true;
                   break;
               }
               break;
           }
           case 0x06: // set
               switch (function) {
               case 0:
                   if (readRegister(rs1) == readRegister(rs2)) {
                       writeRegister(rd, 1);
                   }
                   else {
                       writeRegister(rd, 0);
                   }
                   break;
               case 1:
                   if (readRegister(rs1) != readRegister(rs2)) {
                       writeRegister(rd, 1);
                   }
                   else {
                       writeRegister(rd, 0);
                   }
                   break;
               case 2:
                   if (static_cast<int32_t>(readRegister(rd)) < static_cast<int32_t>(readRegister(rs1))) {
                       writeRegister(rd, 1);
                   }
                   else {
                       writeRegister(rd, 0);
                   }
                   break;
               case 3:
                   if (static_cast<int32_t>(readRegister(rd)) >= static_cast<int32_t>(readRegister(rs1))) {
                       writeRegister(rd, 1);
                   }
                   else {
                       writeRegister(rd, 0);
                   }
                   break;
               case 4:
                   if (readRegister(rd) < readRegister(rs1)) {
                       writeRegister(rd, 1);
                   }
                   else {
                       writeRegister(rd, 0);
                   }
                   break;
               case 5:
                   if (readRegister(rd) >= readRegister(rs1)) {
                       writeRegister(rd, 1);
                   }
                   else {
                       writeRegister(rd, 0);
                   }
                   break;
               default:
                   exception(1, instructionReg);
                   pcChanged = true;
                   exceptionTaken = true;
                   break;
               }
               if (rd == 31) {
                   pcChanged = true;
               }
               break;
           case 0x07: // bra
               switch (function) {
               case 0:
                   if (readRegister(rd) == readRegister(rs1)) {
                       programCounter += signExtend(immediate13, 13);
                       pcChanged = true;
                   }
                   break;
               case 1:
                   if (readRegister(rd) != readRegister(rs1)) {
                       programCounter += signExtend(immediate13, 13);
                       pcChanged = true;
                   }
                   break;
               case 2:
                   if (static_cast<int32_t>(readRegister(rd)) < static_cast<int32_t>(readRegister(rs1))) {
                       programCounter += signExtend(immediate13, 13);
                       pcChanged = true;
                   }
                   break;
               case 3:
                   if (static_cast<int32_t>(readRegister(rd)) >= static_cast<int32_t>(readRegister(rs1))) {
                       programCounter += signExtend(immediate13, 13);
                       pcChanged = true;
                   }
                   break;
               case 4:
                   if (readRegister(rd) < readRegister(rs1)) {
                       programCounter += signExtend(immediate13, 13);
                       pcChanged = true;
                   }
                   break;
               case 5:
                   if (readRegister(rd) >= readRegister(rs1)) {
                       programCounter += signExtend(immediate13, 13);
                       pcChanged = true;
                   }
                   break;
               default:
                   exception(1, instructionReg);
                   exceptionTaken = true;
                   pcChanged = true;
                   break;
               }
               break;
           case 0x08: // read csr
           case 0x09: // write csr

           default:
               exception(1, instructionReg);
               exceptionTaken = true;
               pcChanged = true;
               break;

           }
           if (not pcChanged) {
               programCounter += 4;
           }
       }

void CPU::clockCycle() {
    switch (state) {
    case 0:
        fetch();
        state = 1;
        break;
    case 1:
        execute();
        state = 0;
        break;
    }
}