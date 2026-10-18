# SR32 - (SIMPLE RISC) 32 #
## WORK IN PROGRESS ##
 Much of this project is heavily in WIP however most of the basics are ratified however not officially. 

## Description ##

This is a large project of a homebrew computer design. It includes the ISA specification, assembler and other things planned such as HDL.

This is a large project, split over multiple languages. Currently c++ is used for the emulator, python for the assembler and md for the documentation.

Here is the paths to the different folders and files with rough descriptions.

| Path | Description |
|---|---|
| `Documentation/` | All documentation and reference material. |
| `Documentation/SR32 ISA specification.md` | The ISA specification - defines the required behaviour for a compliant SR32 CPU. |
| `Assembler/` | A basic Python assembler that assembles SR32 assembly into raw binary. |
| `Emulators/` | A C++ emulator for an SR32-compliant CPU, including 64KB ROM, 64KB RAM, and a memory-mapped output. |
| `HDL/` | Placeholder for a future HDL implementation. |

### License ###
This project is produced under the GNU General Public License v3.0.