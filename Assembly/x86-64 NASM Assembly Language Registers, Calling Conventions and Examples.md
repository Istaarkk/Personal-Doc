### 1. **Registers in x86-64**

In the **x86-64** architecture, there are **16 general-purpose** registers, each 64 bits:

- **RAX**: Main accumulator, often used for arithmetic operations or to return a value (like `return` in C).
- **RBX**: Base register, often preserved.
- **RCX**: Counter register, used for loops (for example with `loop`).
- **RDX**: Data register, used for I/O operations or to pass a second argument in function calls.
- **RSI**: Source index, used for string operations or to pass the first argument in function calls.
- **RDI**: Destination index, used for string operations or to pass the second argument in function calls.
- **RBP**: Base pointer, points to the beginning of the current function's stack.
- **RSP**: Stack pointer, points to the top of the stack, typically used for stack-related operations.
- **R8** to **R15**: Additional general-purpose registers.

There are also smaller versions of the registers for 32-bit, 16-bit, and 8-bit:

- **RAX** → **EAX** (32 bits) → **AX** (16 bits) → **AL** (8 bits)

### 2. **Calling Convention: SysV ABI for Linux**

In **x86-64**, the SysV ABI calling convention is used to pass arguments during function calls.

- The first **six arguments** are passed in the following registers, from left to right:
    
    - 1st argument → **RDI**
    - 2nd argument → **RSI**
    - 3rd argument → **RDX**
    - 4th argument → **RCX**
    - 5th argument → **R8**
    - 6th argument → **R9**
- Return values are stored in **RAX**.
    
- Additional arguments are passed via the stack.
    
- The **RSP** register must be aligned to **16 bytes** before any function call.
    

### 3. **Examples Comparing C and NASM**

#### Example 1: Adding Two Numbers

##### In C:
```c
int add(int a, int b) {
    return a + b;
}
```
##### In NASM:

```nasm
section .text
    global add    ; Declare the function as public

add:
    mov rax, rdi  ; Copy the first argument (a) into RAX
    add rax, rsi  ; Add the second argument (b) to RAX
    ret           ; Return the result in RAX
```
Explanations:

- In C, the arguments `a` and `b` are passed to the function, and the sum is returned.
- In assembly, `rdi` contains the first argument `a` and `rsi` contains the second argument `b`. We perform the addition and return the result in `rax`.

#### Example 2: `for` Loop

##### In C:
```c
void loop(int n) {
    for (int i = 0; i < n; i++) {
        // do something
    }
}
```
##### In NASM:

```nasm
section .text
    global loop

loop:
    mov rcx, rdi     ; Copy n into RCX (RCX used as the counter)
    xor rax, rax     ; Set i to 0 (using RAX as i)

for_loop:
    cmp rax, rcx     ; Compare i (RAX) with n (RCX)
    jge end_loop     ; If i >= n, jump to end_loop
    ; Do something here

    inc rax          ; i++
    jmp for_loop     ; Repeat the loop

end_loop:
    ret              ; Return

```
Explanations:

- In C, we have a `for` loop that increments a counter `i`.
- In assembly, `rax` is used as the counter `i`, and we use instructions like `cmp` to compare `i` with `n`. The `jmp` instruction is used to jump to labels.

### 4. **Memory and Stack Management**

The **stack** is a LIFO (Last In, First Out) structure. Each function can have its own space on the stack to store local variables. When a function is called, a new stack frame is created.

- **PUSH**: Adds a value to the top of the stack (decrements `rsp`).
- **POP**: Removes a value from the top of the stack (increments `rsp`).

#### Example: Function with a Local Variable

##### In C:

```nasm
void foo() {
    int x = 10;
    // do something with x
}
```
##### In NASM:

```nasm
section .text
    global foo

foo:
    push rbp         ; Save the old RBP
    mov rbp, rsp     ; RBP now points to the current top of the stack

    sub rsp, 8       ; Allocate space for x (8 bytes)
    mov qword [rbp-8], 10  ; Initialize x with the value 10

    ; Do something with x

    mov rsp, rbp     ; Restore the stack
    pop rbp          ; Restore the old RBP
    ret

```
Explanations:
- In C, the local variable `x` is automatically managed by the compiler.
- In assembly, we must manually allocate space on the stack for `x`. Here, we allocate 8 bytes by decrementing `rsp`, then we store the value `10` in that space.

### 5. **System Calls in x86-64 Linux**

To perform a system call in assembly (like reading a file, printing to the screen, etc.), we use the `syscall` instruction.

- System calls are identified by a **number**, which is passed in **RAX**.
- Parameters are passed in the following registers: **RDI**, **RSI**, **RDX**, **R10**, **R8**, **R9**.

#### Example: System Call to Write to Standard Output

##### In NASM:

```nasm
section .data
    msg db "Hello, world!", 0xA   ; Message to display
    len equ $ - msg                ; Length of the message

section .text
    global _start

_start:
    ; System call write (number 1)
    mov rax, 1        ; System call number (write)
    mov rdi, 1        ; File descriptor (1 for stdout)
    mov rsi, msg      ; Address of the message
    mov rdx, len      ; Length of the message
    syscall           ; Perform the system call

    ; System call exit (number 60)
    mov rax, 60       ; System call number (exit)
    xor rdi, rdi      ; Return code (0)
    syscall           ; Exit

```

Explanations:
- This example writes the message "Hello, world!" to standard output (`stdout`).
- The `write` system call uses file descriptor 1 to indicate `stdout`, the address of the message is passed in `rsi`, and the length of the message in `rdx`.

### **6. Quiz Questions**

Which register is used to store the return value of a function?

	**Answer:** RAX

Which register is used to store the system call number in x86-64?

	**Answer:** RAX

What is an opcode?

	**Answer:** The binary code representing the operation to be performed.

What is the ISA of a processor?

	**Answer:** The set of instructions the processor can execute.

What is the purpose of the RSP register?

	**Answer:** It points to the top of the stack.

What is the effect of a JMP instruction?

	**Answer:** Jumps to a new address unconditionally.

What does ZF stand for?

	**Answer:** Zero Flag

Which component executes the instructions of a program?

	**Answer:** The processor (CPU)

What does RISC stand for?

	**Answer:** Reduced Instruction Set Computer

What does `mov rax, [rbx]` do?

	**Answer:** Loads the value at the address pointed to by `rbx` into `rax`.

Which section contains uninitialized data?

	**Answer:** `.bss` section

Where is the remainder stored when using the DIV instruction?

	**Answer:** RDX

Which instruction is used to call a function?

	**Answer:** `call`

How does a function return to the calling instruction?

	**Answer:** Using the `ret` instruction.

How are arguments passed to functions in x86-64?

	**Answer:** The first four arguments are passed in the registers RDI, RSI, RDX, and RCX; subsequent arguments are passed on the stack.