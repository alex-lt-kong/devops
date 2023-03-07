* Check GPU status:  `nvidia-smi`.

* Remove Nvidia's artificial limit on the performance of consumer-grade GPUs: https://github.com/keylase/nvidia-patch

* to make the GPU passthrough work, you need to set KVM guest's schema to xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0' and then add the following section to the <domain> section:
```xml
  <qemu:commandline>
    <qemu:arg value='-cpu'/>
    <qemu:arg value='host,hv_time,kvm=off,hv_vendor_id=null'/>
  </qemu:commandline>
```