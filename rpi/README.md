# Raspberry Pi

## Headless OS install with SSH enabled

* Write image to sd card: `dd if=/home/mamsds/Downloads/2022-04-04-raspios-bullseye-arm64-lite.img/2022-04-04-raspios-bullseye-arm64-lite.img of=/dev/sda bs=4M conv=fsync`.

* Enable `ssh`:
  * Locate the boot partition:
  ```
  # lsblk
  NAME                          MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
  sda                             8:0    1  59.5G  0 disk  
  ├─sda1                          8:1    1   256M  0 part  
  └─sda2                          8:2    1   1.6G  0 part 
  ...
  ```
  * `mount` the partition to an arbitrary directory: `mount /dev/sda1 /tmp/sdcard-boot`.
  * Create an empty `ssh` file: `touch /tmp/sdcard-boot/ssh`.


* Default login
  * In the past, Raspberry Pi OS used `pi` as default user and `raspberry` as default password.
  * This is no longer the case since 2022 according to [this post](https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/)
  * Generate a password hash with: `echo 'mypassword' | openssl passwd -6 -stdin`
  * Save `<username>:<hashed password>` to `/tmp/sdcard-boot/userconf`


## Enable with sharing in AP mode

* Finishing all steps using headless SSH is possible but risky, preparing physical keyboard and monitor would make 
the process much safer.

* Install `hostapd` and `dnsmasq`: `apt-get -y install hostapd bridge-utils `.

* Disable them for the time being: `systemctl stop hostapd`.

* Append `denyinterfaces wlan0` and `denyinterfaces eth0` to `/etc/dhcpcd.conf`
to disable dynamic IP allocation to the subject WLAN interface.

* Append the following to `/etc/network/interfaces` to define a new network bridge.
```
# Bridge setup
auto br0
iface br0 inet dhcp
bridge_ports eth0 wlan0
```

* Add the lines to `/etc/hostapd/hostapd.conf`
```
interface=wlan0
bridge=br0
#driver=nl80211
ssid=Hotspot-Name
hw_mode=g
channel=11
wmm_enabled=1
# Wi-Fi Multimedia (WMM) is a Wi-Fi Alliance interoperability certification.
# It provides basic Quality of service (QoS) features to IEEE 802.11 networks.
# In the field of computer networking, quality of service refers to traffic
# prioritization and resource reservation control mechanisms rather than the
# achieved service quality.
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=your_very_complicated_password
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

* Unmask `hostapd`: `systemctl unmask hostapd`.

* Restart and the AP should work

* Just to be sure, after reboot, can issue `brctl show` to check if the network bridge is established as expected.