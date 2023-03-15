* Check GPU status:  `nvidia-smi`.

* If Nvidia GPU-related components (driver, cuda, nvcc, etc) are installed 
via a `.list` file in `sources.list.d/`, upgrading the base OS could confuse
package manager. Old `.list` file may need to be manually removed to make it
work again.

* Remove Nvidia's artificial limit on the performance of consumer-grade GPUs: https://github.com/keylase/nvidia-patch

