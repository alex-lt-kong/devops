# smart-notifier

## Usage

Install `smartmontools`: `apt install smartmontools`

Clone this project to a local place, such as `/usr/local/bin/smart-notifier`

Add the following line to `/etc/smartd.conf`:

```
DEVICESCAN -a -s (S/../.././20|L/../../6/21) -m root -M test -M exec /usr/local/bin/smart-notifier/sn.sh
```
