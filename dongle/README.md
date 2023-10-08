To burn a Dongle
---
ref. https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/establish-serial-connection.html
```shell
ls /dev/tty*
# You need to find the new one when you connected eps32
ls /dev/tty*
sudo chmod a+rw /dev/ttyUSB0
python -m esptool -p /dev/ttyUSB0 -b 460800 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 vysor-dongle-esp32.bin
```
For USB-c We will get `/dev/ttyACM0`
```shell
sudo chmod a+rw /dev/ttyACM0 # maybe this line is not necessary
python -m esptool -p /dev/ttyACM0 erase_flash
python -m esptool -p /dev/ttyACM0 write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 vysor-dongle-esp32.bin
```
Unfortunately, The image of vysor is now support to this type.\
[ESP32 type](http://www.ulisp.com/show?3TQF)

### erase memory
**hold on boot button**
```shell
python -m esptool -p /dev/ttyUSB0 --chip esp32 erase_flash
```
ref. https://randomnerdtutorials.com/esp32-erase-flash-memory/
### EN to GND is reset