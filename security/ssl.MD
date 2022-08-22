# SSL

* View a certificate: `openssl s_client -showcerts -connect <domain.name:443>`

* A simple way to verify if an SSL certificate is issued by a CA trusted by the current system:
`curl https://<domain.name> --verbose 2>&1 | grep "SSL certificate"`

* How to know if my certificate is in PEM format? If you can read its content by `openssl x509 -in cert.crt -text`,
it is in PEM format.