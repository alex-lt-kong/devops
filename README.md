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

* `virsh edit [VMName]`
* Revise the VM's XML definition as follows on host
```
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
      <source dir='/path'/>
      <target dir='mount_tag'/>
    </filesystem>
    ...
  </devices>
</domain>
```
* Issue on guest: `mount -t virtiofs mount_tag /mnt/mount/path`
* Reference: https://libvirt.org/kbase/virtiofs.html


### Clone an existing VM

* `virt-clone --original [OrigVMName] --name [NewVMName] --auto-clone`
* It takes care of MAC address conflicts, etc.
* It does not change:
  * Hostname in `/etc/hosts` and `/etc/hostname`
  * SSH host keys:
    * Remove existing keys: `rm -v /etc/ssh/ssh_host_*`
    * Re-generate: `dpkg-reconfigure openssh-server`
  * Root password: `passwd`

### Enable/Disable guest auto start

* Enable: `virsh autostart [Guest Name]`
* Disable: `virsh autostart [Guest Name] --disable`

