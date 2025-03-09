# SR882toMQTT

This script connect to SR882, retrieve most valuable data, and publish them via MQTT.
It should be the same structure as SR1128, SR1168, sr1188
Vendor name could be Ultisolar

## Some history
After numerous tries to discover how to request my no-name solar boiler controller, I finally found out the original software, which contains all the informations about register used.
Unfortunately, the protocol used doesn't seems to be modbus (CRC error in response), so I reverse engineered the software to obtain the query sent.

Thanks to : RogMoe from HomeAssistant community forum, for sharing the precious original software (https://community.home-assistant.io/t/ultisolar-evacuated-tubes-controller/733595/6)
