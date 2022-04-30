# KVM Notes

## Guest Install

* Command
```
virt-install \
--virt-type=kvm \
--name [VMName] \
--ram 512 \
--vcpus=1 \
--virt-type=kvm \
--cdrom=[ISOPath] \
--network=bridge=br0,model=virtio \
--graphics vnc \
--disk path=/var/lib/libvirt/images/vm.qcow2,size=11,bus=virtio,format=qcow2
```

* Map `localhost:5901` to `remote:5901` for secure VNC: `ssh user@host -L 5901:localhost:5901`

* Expert mode is usually recommended for more flexibility:
  * Use root account only.
  * Disable default security update (as it is very sloooow in China).

* Partitioning:
  * delect manual partitioning and add only one root partition.
  * Bootable flag is for MBR partitions only, `off` is okay for modern systems.
  * Swap and EFI paritions are both optional.

* After install:
  * Remember to re-enable security update if it is disabled during installation. A template can be found here: https://wiki.debian.org/SourcesList#Example_sources.list
  * Should we disable VNC? By default it should listen on `127.0.0.1:5900` only, just in case we break SSH, can leave it turned on.

## Management

### Clone an existing VM

* virt-clone --original [OrigVMName] --name [NewVMName] --auto-clone
* It takes care of MAC address, etc.
* It does not change SSH host keys, though:
  * Remove existing keys: `rm -v /etc/ssh/ssh_host_*`
  * Re-generate: `dpkg-reconfigure openssh-server`

### Enable/Disable guest auto start

* Enable: `virsh autostart [Guest Name]`
* Disable: `virsh autostart [Guest Name] --disable`

