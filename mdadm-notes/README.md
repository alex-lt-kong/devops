# Mdadm

## Replace a disk

0. Suppose the faulty disk is `/dev/sdb` and the partition in use is `/dev/sdb1`.

0. Check the disk's SMART info: `smartctl -a /dev/sdb`. This is VERY IMPORTANT that we need to note the information
down--when we physically replace the disk, this information is key to locate the physical device.

0. Check the array's status: `mdadm --detail /dev/md0`.

0. Mark a disk as failed: `mdadm --manage /dev/md0 --fail /dev/sdb1`.

0. Check the array's status again: `mdadm --detail /dev/md0`.

0. Remove the disk by mdadm: `mdadm --manage /dev/md0 --remove /dev/sdb1`.

0. Check the array's status again: `mdadm --detail /dev/md0`.

0. Physically replace the disk.

0. Copy the partition table from another health disk to the new disk: `sfdisk -d /dev/sda | sfdisk /dev/sdb`

0. Check if the new disk has the correct partition table: `lsblk`

0. Create mirror with new disk: `mdadm --manage /dev/md0 --add /dev/sdb1`