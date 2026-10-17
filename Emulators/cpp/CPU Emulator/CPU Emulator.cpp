// CPU Emulator.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "cpu.h"

#include <iostream>

uint32_t ram[65536] = {};
uint32_t rom[65536] = {};

int main()
{
    std::cout << "Hello World!\n";
}

uint32_t readMemory(uint32_t address, uint32_t size) {
    if ((address & (1u << 16)) == 0)
    {
        return(rom[address & 0xffff]);
    }
    else
    {
        return(ram[address & 0xffff]);
    }
}

void writeMemory(uint32_t address, uint32_t data, uint32_t size) {
    if (address == 0xffffffff) {
        std::cout.put(static_cast<char>(data & 0xFF));
    }
    else if ((address & (1u << 16)) == 0)
    {
        rom[address & 0xffff] = data;
    }
    else
    {
        ram[address & 0xffff] = data;
    }
    return;
}
