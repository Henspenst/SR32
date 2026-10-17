#pragma once

#include <cstdint>
#include <unordered_map>

uint32_t readMemory(uint32_t address, uint32_t size);
void writeMemory(uint32_t address, uint32_t data, uint32_t size);

class CPU
{
private:
    std::unordered_map < int,
        uint32_t > csrs = {
            {
                0x401,
                0x0000
            }, // Trap cause
            {
                0x402,
                0x0000
            }, // Trap value
            {
                0x700,
                0x0000
            }, // Trap program counter
            {
                0x400,
                0x300
            }, // Trap vector
    };
    uint32_t registers[32] = {};
    uint32_t instructionReg = 0;
    uint32_t programCounter = 0;

    bool pcChanged = false;
    bool exceptionTaken = false;

    int state = 0;

    uint32_t signExtend(uint32_t data, int widthIn);

    void exception(uint8_t cause, uint32_t value);

    uint32_t readRegister(int reg);
    void writeRegister(uint8_t reg, uint32_t data);

    bool readCSRS(uint16_t csr, uint32_t& data);
    bool writeCSRS(uint16_t csr, uint32_t data);

    void fetch();
    void execute();

    uint32_t alu(
        uint32_t inputA,
        uint32_t inputB,
        int operation
    );

public:
    CPU();

    void clockCycle();

    uint32_t getPC() const;
    uint32_t getRegister(uint8_t reg) const;
};