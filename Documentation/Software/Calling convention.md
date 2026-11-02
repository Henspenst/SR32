| Register |           Use          |  Name | Preservation |
|:--------:|:----------------------:|:-----:|--------------|
|    r0    |          Zero          |  zero | Always zero  |
|    r1    |     Return address     |   ra  | Caller-saved |
|    r2    |      Stack pointer     |   sp  | Callee-saved |
|    r3    |     Global pointer     |   gp  | Callee-saved |
|    r4    |      Frame pointer     |   fp  | Callee-saved |
|  r5-r12  |      Return/ Args      | a0-a7 | Caller saved |
|  r13-r21 | Caller-saved tempories | t0-t8 | Caller-saved |
|  r22-r30 | Callee-saved registers | s0-s8 | Callee-saved |
|    r31   |     ProgramCounter     |   pc  |              |

Callee saved - preserved across calls.
Caller saved - tempoary, not preserved across calls.


the stack pointer holds

downwards growing stack
reads then increments
decrements then writes