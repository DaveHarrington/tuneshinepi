# Tuneshine power-saver

A Pico W that polls a server, and turns the relay on/off depending on the value it receives.

## Setup

Install the [pico-sleep](https://github.com/ghubcoder/micropython-pico-deepsleep?tab=readme-ov-file) uf2 (use the Pico W one).

Using Thonny, upload the py files. Add SSID and password to wifi.conf

## Notes

Battery will shut-off port when too low a current is drawn for a minute or so. Only way to reset the port is to take current to 0.
