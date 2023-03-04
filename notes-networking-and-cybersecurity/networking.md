# Network

* Relay a request to a local interface to a remote one: `socat TCP4-LISTEN:4321 TCP4:localhost:4321`

## Bridge

* List all ethernet bridges: `brctl show`.

* Change the interfaces linked by a bridge: edit `/etc/network/interfaces`
(If the bridge is used by other services, such as `hostapd`, need to change
their configurations correspondingly, e.g., `/etc/hostapd/hostapd.conf`)

