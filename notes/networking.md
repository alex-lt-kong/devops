# Network

* Relay a request to a local interface to a remote one: `socat TCP4-LISTEN:4321 TCP4:localhost:4321`

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

* Change the interfaces linked by a bridge: edit `/etc/network/interfaces`
(If the bridge is used by other services, such as `hostapd`, need to change
their configurations correspondingly, e.g., `/etc/hostapd/hostapd.conf`)

