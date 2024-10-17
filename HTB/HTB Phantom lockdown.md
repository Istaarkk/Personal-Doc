
## Step 1: Extract the ZIP file
- Use the following command to extract the zip file:

    ```bash
    unzip <file.zip>
    ```

## Step 2: Unsquash the root filesystem
- After extraction, you'll find 3 documents including a **rootfs** file (which is squashed).
- Use the following command to unsquash it:

    ```bash
    unsquashfs rootfs
    ```

## Step 3: Search for the flag
- Now that all folders are visible, search recursively using `grep` to find the flag:

    ```bash
    grep -r HTB
    ```

- The flag is: **`HTB{N0w_Y0u_C4n_L0g1n}`**
