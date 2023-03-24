# smart-notifier

Send email notifications when a SMART warning is detected by smartmontools

## Usage

Install `smartmontools`: `apt install smartmontools`

Clone this project to a local place, such as `/usr/local/bin/devops`

Add the following line to `/etc/smartd.conf`:

```
DEVICESCAN -a -s (S/../.././20|L/../../6/21) -m root -M test -M exec /usr/local/bin/devops/smart-alert/sn.sh
```

## Verification

Restart the smartd service `systemctl restart smartd` and then you should receive test emails.

## Regular check

* Add `/usr/sbin/service smartd restart` to crontab.
* Each time `smartd` restarts, a test email will be sent.
