# Public Key Infrastructure

* View a certificate: `openssl s_client -showcerts -connect <domain.name:443>`

* A simple way to verify if an SSL certificate is issued by a CA trusted by the current system:
`curl https://<domain.name> --verbose 2>&1 | grep "SSL certificate"`

* How to know if my certificate is in PEM format? If you can read its content by `openssl x509 -in cert.crt -text`,
it is in PEM format.

## SSH keys

* Create new:
  * RSA: `ssh-keygen`
  * Ed25519: `ssh-keygen -t ed25519` (a not-NIST/non-NSA algorithm)

* Convert openssh format to Putty's ppk format:
  * Install putty: `apt install putty-tools`
  * Convert: `puttygen ~/.ssh/id_ed25519 -o ~/.ssh/id_ed25519.ppk`

## Generate a self-signed SSL certificate

* `openssl req -newkey rsa:4096 -x509 -sha512 -days 365 -nodes -out my-cert.crt -keyout my-cert.key`


## Add/Remove trusted CAs

* To add: `cp trusted-ca.crt /usr/local/share/ca-certificates/trusted-ca.crt`
and then `update-ca-certificates`
* To remove: `rm /usr/local/share/ca-certificates/trusted-ca.crt` and then
`update-ca-certificates --fresh`
* Expected result: `1 added`
  ```
  Updating certificates in /etc/ssl/certs...
  1 added, 0 removed; done.
  Running hooks in /etc/ca-certificates/update.d...
  done.
  ```
  * Note that as of 2022, many broswers, including Chrome and Firefox, maintain its own list of trusted CAs. To make
    a self-generated CA trusted, one needs to do it separately--usually via the browser's GUI.

## Apache SSL `.conf` for Let's Encrpyt certificates

* This is closely related to the "Apache SSL-enabled reversed proxy" in
[this networking note](./networking.md). Let's Encrypt generates
a few different files, which ones should be used by Apache to follow the
best practice?

```
SSLCertificateFile      /etc/letsencrypt/live/<domain_name>/fullchain.pem
SSLCertificateKeyFile   /etc/letsencrypt/live/<domain_name>/privkey.pem
```

* [Reference](https://community.letsencrypt.org/t/recommended-apache-config/58294)