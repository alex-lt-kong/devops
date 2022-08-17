# Mdadm

## Replace a disk

0. Suppose the faulty disk is `/dev/sdb` and the partition in use is `/dev/sdb1`.

0. Check the disk's SMART info: `smartctl -a /dev/sdb`. This is VERY IMPORTANT that we need to note the information
down--when we physically replace the disk, this information is key to locate the physical device.

0. Check the array's status: `mdadm --detail /dev/mdX`.

0. Mark a disk as failed: `mdadm --manage /dev/mdX --fail /dev/sdb1`.

0. Check the array's status again: `mdadm --detail /dev/mdX`.

0. Remove the disk by mdadm: `mdadm --manage /dev/mdX --remove /dev/sdb1`.

0. Check the array's status again: `mdadm --detail /dev/mdX`.

0. Physically replace the disk.

0. Copy the partition table from another health disk to the new disk: `sfdisk -d /dev/sda | sfdisk /dev/sdb`

0. Check if the new disk has the correct partition table: `lsblk`

0. Create mirror with new disk: `mdadm --manage /dev/mdX --add /dev/sdb1`


## Verify the integrity of an array

* Using `fsck` doesn't seem to fit: it checks file systems such as ext3/ext4. Since we are using RAID, unless the RAID
totally fails, it is likely that `mdadm` will simply return "everything okay" to `fsck`.

* Start a check offline: `/usr/share/mdadm/checkarray /dev/mdX`.

* Check the status by `cat /proc/mdstat`.

## Stop/start an array

* To stop: `mdadm --stop /dev/mdX`

* To start: `mdadm --assemble --scan`