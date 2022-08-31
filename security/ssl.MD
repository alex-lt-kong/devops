# SSL

* View a certificate: `openssl s_client -showcerts -connect <domain.name:443>`

* A simple way to verify if an SSL certificate is issued by a CA trusted by the current system:
`curl https://<domain.name> --verbose 2>&1 | grep "SSL certificate"`

* How to know if my certificate is in PEM format? If you can read its content by `openssl x509 -in cert.crt -text`,
it is in PEM format.

## Add/Remove trusted CAs

* To add: `cp trusted-ca.crt /usr/local/share/ca-certificates/trusted-ca.crt`
and then `update-ca-certificates`
* To remove: `rm /usr/local/share/ca-certificates/trusted-ca.crt` and then
`update-ca-certificates --fresh`