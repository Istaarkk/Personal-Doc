# Arch Linux Installation Guide

## 1. Qemu VM Setup:
Create the virtual disk image (20 GB in this example):
```bash
qemu-img create -f qcow2 <image_name> 20G
```

Boot the Arch Linux ISO using Qemu:
```bash
qemu-system-x86_64 -enable-kvm -m 1024 -boot d -cdrom <archlinux.iso> -hda <image_name>
```
(Optional for UEFI boot) Add UEFI firmware file (OVMF.fd) to the Qemu command:
```bash
-drive if=pflash,format=raw,file=./OVMF.fd
```

## 2. VirtualBox VM Setup:
Enable EFI mode in VirtualBox (GUI):
```
settings -> system -> motherboard -> enable EFI
```

## 3. Network Setup in the VM:
Check network interfaces:
```bash
ip link
ip a
ping archlinux.org
```
Request DHCP lease (if necessary):
```bash
dhclient
```

## 4. Partition the Disk:
1. List disks and create GPT partition table:
```bash
fdisk /dev/sda
```
   Inside `fdisk`:
```
g # Create GPT partition table
```

2. Create EFI partition (/dev/sda1, 512 MB):
```bash
n
+512M
```

3. Create Linux filesystem partition (/dev/sda2, remaining space):
```bash
n
```

4. Change the partition type for /dev/sda1 to EFI:
```bash
t
1
1 # EFI System
```

5. Write and quit:
```bash
w
```

## 5. Encrypt and Set Up LVM on /dev/sda2:
- Encrypt /dev/sda2 with LUKS:
```bash
cryptsetup luksFormat /dev/sda2
```

- Open the encrypted partition as cryptlvm:
```bash
cryptsetup open /dev/sda2 cryptlvm
```

- Create the LVM physical volume:
```bash
pvcreate /dev/mapper/cryptlvm
```

- Create a volume group vg0:
```bash
vgcreate vg0 /dev/mapper/cryptlvm
```

- Create logical volumes:
  - Root (10 GB):
  ```bash
  lvcreate -L 10G vg0 -n root
  ```
  - Home (remaining space hence do it in the last part after the swap):
  ```bash
  lvcreate -l 100%FREE vg0 -n home
  ```
  - Swap (2 GB):
  ```bash
  lvcreate -L 2G vg0 -n swap
  ```

## 6. Format the Partitions:
- Format EFI partition /dev/sda1 as FAT32:
```bash
mkfs.fat -F32 /dev/sda1
```

- Format root (vg0-root) and home (vg0-home) as btrfs:
```bash
mkfs.btrfs /dev/vg0/root
mkfs.btrfs /dev/vg0/home
```

- Initialize swap on vg0-swap:
```bash
mkswap /dev/vg0/swap
swapon /dev/vg0/swap
```

## 7. Mount the Partitions:
- Mount the root partition:
```bash
mount /dev/vg0/root /mnt
```

- Create and mount the home directory:
```bash
mkdir /mnt/home
mount /dev/vg0/home /mnt/home
```

- Mount the EFI partition:
```bash
mkdir /mnt/boot
mount /dev/sda1 /mnt/boot
```

## 8. Bootstrap the Base System:
- Install the base system:
```bash
pacstrap -K /mnt base linux linux-firmware btrfs-progs lvm2
```

- Generate fstab:
```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

- Chroot into the new system:
```bash
arch-chroot /mnt
```

## 9. System Configuration:
- Set the timezone to Paris:
```bash
ln -sf /usr/share/zoneinfo/Europe/Paris /etc/localtime
hwclock --systohc
```

- Set the locale to en_US.UTF-8:
```bash
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

- Set the hostname:
```bash
echo "arch2600" > /etc/hostname
```

- Enable systemd networking:
```bash
systemctl enable systemd-networkd
systemctl enable systemd-resolved
```

- Set root password:
```bash
passwd
```

## 10. Initramfs Configuration:
- Edit /etc/mkinitcpio.conf:
  - Replace udev with systemd in the hooks section.
  - Add lvm2, sd-encrypt, sd-vconsole, and btrfs hooks:
```bash
HOOKS=(base systemd autodetect keyboard sd-vconsole modconf block sd-encrypt lvm2 filesystems btrfs)
```

- Rebuild the initramfs:
```bash
mkinitcpio -p linux
```

## 11. Bootloader Setup:
- Install systemd-boot:
```bash
bootctl install
```

- Create the boot entry in /boot/loader/entries/arch.conf with the following content:
```
title Arch Linux
linux /vmlinuz-linux
initrd /initramfs-linux.img
options rd.luks.name=<UUID>=cryptlvm root=/dev/vg0/root rw
```

- Get the UUID for /dev/sda2:
```bash
blkid /dev/sda2
```

## 12. Final Steps:
- Exit the chroot:
```bash
exit
```

- Unmount all partitions:
```bash
umount -R /mnt
```

- Reboot the system:
```bash
reboot
```
