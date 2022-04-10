# KVM Notes

## Guest Install

* Command
```
virt-install \
--virt-type=kvm \
--name dns \
--ram 512 \
--vcpus=1 \
--virt-type=kvm \
--cdrom=/var/vms/debian-11.3.0-amd64-netinst.iso \
--network=bridge=br0,model=virtio \
--graphics vnc \
--disk path=/var/vms/dns.qcow2,size=11,bus=virtio,format=qcow2
```

* Map `localhost:5901` to `remote:5901` for secure VNC: `ssh user@host -L 5901:localhost:5901`

* Expert mode is usually recommended for more flexibility:
  * Use root account only.
  * Disable default security update (as it is very sloooow in China).

* Partitioning: select manual partitioning and add only one root partition.
Swap and EFI paritions are both optional.

* Remember to reanble security update if it is disabled during installation.
A template can be found here: https://wiki.debian.org/SourcesList#Example_sources.list

## Management

### Enable/Disable guest auto start

* Enable: `virsh autostart [Guest Name]`
* Disable: `virsh autostart [Guest Name] --disable`