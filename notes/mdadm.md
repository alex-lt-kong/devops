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

0. Create a partition on the new disk for RAID to use, we may take one of the 
below approaches:

    0. If size of the new disk is the same as an old disk, and an old disk's
    partition table looks satisfactory, we can copy the partition table from
    an old disk to the new disk: `sfdisk -d /dev/sda | sfdisk /dev/sdb`

    0. Or we may just create a new partition like usual, with `fdisk` etc.

    * Note that a RAID array can directly use the entire disk, without using
    a partition, this may cause issue. For example, say both the old and new
    disk are 2TB in size, but the old disk has `2 * 1024 ^ 3` = `2147483648`
    bytes while the new disk has `2 * 1000^3` = `2000000000` bytes. If we
    use the entire old hard disk, the new hard disk may not be large enough for
    the RAID array! Therefore, when we get a new hard disk, we might want to
    create a partition on top of it, and make that partition a bit smaller,
    just in case in the future there will be a slightly smaller hard disk
    with the same nominal capacity.

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