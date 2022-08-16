# Raspberry Pi's GPIO

## Useful links

* GPIO pin definitions: https://pinout.xyz
* Low-level details: https://elinux.org/RPi_GPIO_Code_Samples#Direct_register_access

## Enable 1-Wire temperature sensors

* A lot of online doc says that we simply append `dtoverlay=w1-gpio` to the end
of `/boot/config.txt`.

* This appears to be not enough, we need to appen something like
`dtoverlay=w1-gpio,gpiopin=3,pullup=on` where gpiopin is in BCM mode.

* DS18B20 temperature sensors are used most of the time and they only works with
BCM pins 2 and 3 because only these two pins have 1.8 kohms resistors pull-upt
o 3.3v and this resistor is needed by the DS18B20 sensor.

* If there is more than one 1-wire sensor, we can add another line with `gpiopin`
set to a new pin.

* `reboot`.

* `modprobe w1-gpio` and `modprobe w1-therm`