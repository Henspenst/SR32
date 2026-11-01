// CPU Emulator.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "cpu.h"
#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;

uint8_t ram[65536] = {};
uint8_t rom[65536] = {};

int main()
{
    ifstream romFile(R"(filepath.bin)", ios::binary | ios::ate);
    ifstream::pos_type pos = romFile.tellg();

    romFile.seekg(0, ios::beg);
    romFile.read(reinterpret_cast<char*>(rom), pos);

    CPU cpu;
    for (int i = 0; i < 100; i++)
    {
        cpu.clockCycle();
    }
    romFile.close();
    return 0;
}

uint32_t readMemory(uint32_t address, uint32_t size) {
    uint32_t outBuffer = 0;
    for (int i = 0; i < size; i++)
    {
        if (((address + i) & (1u << 16)) == 0)
        {
            outBuffer = (outBuffer << 8) | rom[(address & 0xffff) + i];
        }
        else
        {
            outBuffer = (outBuffer << 8) | ram[(address & 0xffff) + i];
        }
    }
    return (outBuffer); 
}

void writeMemory(uint32_t address, uint32_t data, uint32_t size) {
    if (address == 0xffffffff) {
        std::cout.put(static_cast<char>(data & 0xFF));
    }
    else {
        for (int i = 0; i < size; i++)
        {
            if ((address & (1u << 16)) != 0)
            {
                ram[(address & 0xffff) + i] = (data >> (((size - 1) - i) * 8)) & 0xff;
            }
        }
    }
    return;
}
