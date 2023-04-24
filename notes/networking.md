# Network

* Forward an TCP request to a local interface to a remote one: `socat TCP4-LISTEN:4321,fork TCP4:<remote-addr>:4321`

## Apache SSL-enabled reversed proxy

* Enable necessarily modules: `a2enmod proxy_http`, `a2enmod ssl`

* Create a conf file: `/etc/apache2/sites-enabled/reverse-proxy-ssl.conf`:

```
<VirtualHost *:443>

    ServerName server.lan

    ProxyPreserveHost On

    ProxyPass           /                http://127.0.0.1:444/
    ProxyPassReverse    /                http://127.0.0.1:444/

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    SSLEngine on

    SSLCertificateFile      /etc/letsencrypt/<fullchain/cert>.pem
    SSLCertificateKeyFile   /etc/letsencrypt/privkey.pem

</VirtualHost>
```

* Enable the site: `a2ensite reverse-proxy-ssl`

## Bridge

* List all ethernet bridges: `brctl show`.

* Create a bridge:

  * There are multiple ways to create a bridge and the most straightforward
  way appears to be editing `/etc/network/interfaces`.
  1. Let's say you have an NIC `eno0` that can access the Internet and
  your `/etc/network/interfaces` is:

      ```
      auto eno0
      iface eno0 inet dhcp
      ```

  1. We change it to:

      ```
      #auto eno0
      #iface eno0 inet dhcp

      auto br0
      iface br0 inet dhcp
          bridge_ports eno0
          bridge_stp off # If we only have a single bridge, should turn it off
      ```

  * There are a few more options you can set, can find more details
  [here](https://wiki.ubuntu.com/KvmWithBridge)
