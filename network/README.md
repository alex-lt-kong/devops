# Network

## Bridge

* List all ethernet bridges: `brctl show`.

* Change the interfaces linked by a bridge: edit `/etc/network/interfaces`
(If the bridge is used by other services, such as `hostapd`, need to change
their configurations correspondingly, e.g., `/etc/hostapd/hostapd.conf`)