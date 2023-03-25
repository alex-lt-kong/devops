# Nvidia GPU

* For GPU passthrough, refer to [this note](./kvm.md)

* Selecting operating system--should we keep using Debian or switch to Ubuntu?
  * Nvidia provides supports for Debian and Ubuntu (as they are very similar
  anyway), if we only want to do video encoding/decoding, both OSes should
  offer very similar experience.
  * However, TensorFlow's documentation mainly uses Ubuntu, if we choose
  Debian, it might still work, but more tweaking could be needed.

* Check GPU status:  `nvidia-smi`.

* If Nvidia GPU-related components (driver, cuda, nvcc, etc) are installed 
via a `.list` file in `sources.list.d/`, upgrading the base OS could confuse
package manager. Old `.list` file may need to be manually removed to make it
work again.

* Remove Nvidia's artificial limit on the performance of consumer-grade GPUs: https://github.com/keylase/nvidia-patch

