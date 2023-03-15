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

### Network bridge

* List all members of a bridge: `brctl show`

### Shared directory

* `virsh edit <VMName>`
* Revise the VM's XML definition as follows on host
```xml
<domain>
  ...
  <memoryBacking>
    <source type='memfd'/>
    <access mode='shared'/>
  </memoryBacking>
  ...
  <devices>
    ...
    <filesystem type='mount' accessmode='passthrough'>
      <driver type='virtiofs'/>
      <source dir='<path_on_host>'/>
      <target dir='<mount_tag_for_guest>'/>
    </filesystem>
    ...
  </devices>
</domain>
```
* Issue on guest: `mount -t virtiofs <mount_tag_for_guest> <path_on_guest>`
* Reference: https://libvirt.org/kbase/virtiofs.html

### Attach USB device to guest

* Check the address of the USB device to be attached:

```shell
~# lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 003: ID 05a3:9230 ARC International Camera
```

* If we want to add the second item to guest,
add the following `<hostdev />` section under the `<devices />` section of
VM's XML definition:
```XML
  <hostdev mode='subsystem' type='usb' managed='yes'>
    <source>
      <vendor id='0x05a3'/>
      <product id='0x9230'/>
      <address bus='1' device='3'/>
    </source>
  </hostdev>
```
  * Note that `<address bus='1' device='3'/>` is only needed if two USB devices
  share the same vendorId and productId; otherwise we can ignore the `<address />` 
  section inside `<source />`.

* After adding the above section amd save the XML definition, KVM will generate
one extra `<address />` section under the `<hostdev />` section:
```XML
<hostdev mode='subsystem' type='usb' managed='yes'>
  <source>
    <vendor id='0x05a3'/>
    <product id='0x9230'/>
    <address bus='1' device='3'/>
  </source>
  <address type='usb' bus='0' port='6'/>
</hostdev>
```
  * Usually we can safely ignore that.

### Clone an existing VM

* `virt-clone --original <OrigVMName> --name <NewVMName> --auto-clone`
* It takes care of MAC address conflicts, etc.
* It does not change:
  * Hostname in `/etc/hosts` and `/etc/hostname`
  * SSH host keys:
    * Remove existing keys: `rm -v /etc/ssh/ssh_host_*`
    * Re-generate: `dpkg-reconfigure openssh-server`
  * Root password: `passwd`

### Auto start management

* Enable: `virsh autostart <VMName>`
* Disable: `virsh autostart <VMName> --disable`
* List all guests which will be be auto-started: `virsh list --all --autostart`
* List all guests which will NOT be auto-started: `virsh list --all --no-autostart`


### Expand guest VM's disk size as well as partitions on it

* List partitions inside guest: `df -h`
* Install necessary package on host: `apt install libguestfs-tools`
* Increase disk size on host: `qemu-img resize vm.qcow2 +20G`
* Backup original qcow file on host: `cp vm.qcow2 vm-orig.qcow2`
* Expand partition on host: `virt-resize -expand /dev/sda1 vm-orig.qcow2 vm.qcow2`
  * The path of partition, `/dev/sda1` is the one we get from step one, `df -h`
  * If the path is `/dev/vda1` inside guest machine, change it to `/dev/sda1`
* Boot into guest, if everything okay, remove backup disk file `rm vm-orig.qcow2`

### Nvidia GPU passthrough
* to make the GPU passthrough work, you need to set KVM guest's schema to
xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0' and then add the
following section to the <domain> section:
```xml
  <qemu:commandline>
    <qemu:arg value='-cpu'/>
    <qemu:arg value='host,hv_time,kvm=off,hv_vendor_id=null'/>
  </qemu:commandline>
```

### Miscellaneous
* Rename a guest: `virsh domrename <OldVMName> <NewVMName>`