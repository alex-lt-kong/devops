# Raspberry Pi

## Headless OS install with SSH enabled

- Write image to sd card: `dd if=/home/mamsds/Downloads/2022-04-04-raspios-bullseye-arm64-lite.img/2022-04-04-raspios-bullseye-arm64-lite.img of=/dev/sda bs=4M conv=fsync`.

- Enable `ssh`:

  - Locate the boot partition:

  ```
  # lsblk
  NAME                          MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
  sda                             8:0    1  59.5G  0 disk
  ├─sda1                          8:1    1   256M  0 part
  └─sda2                          8:2    1   1.6G  0 part
  ...
  ```

  - `mount` the partition to an arbitrary directory: `mount /dev/sda1 /tmp/sdcard-boot`.
  - Create an empty `ssh` file: `touch /tmp/sdcard-boot/ssh`.

- Default login
  - In the past, Raspberry Pi OS used `pi` as default user and `raspberry` as default password.
  - This is no longer the case since 2022 according to [this post](https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/)
  - Generate a password hash with: `echo 'mypassword' | openssl passwd -6 -stdin`
  - Save `<username>:<hashed password>` to `/tmp/sdcard-boot/userconf`

## Disable swap device

- We can disable swap device to prolong the lifespan of SD card used by Raspberry Pi.
- Turn it off: `swapoff -a`.
- If we stop here, the swap space will be spawned again after reboot!
- Remove the program that re-creates it: `apt remove dphys-swapfile`.

## Disable auto login

- Remove the corresponding line in: `/etc/systemd/system/getty@tty1.service.d/autologin.conf`.

## Disable screensaver

- https://forums.raspberrypi.com/viewtopic.php?f=91&t=57552
