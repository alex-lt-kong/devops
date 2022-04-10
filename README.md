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

* SSH portforwarding for secure VNC: `ssh root@host -L 5901:localhost:5901`

* Expert mode is usually recommended for more flexibility.