import re
from twisted.internet.protocol import DatagramProtocol

class listener(DatagramProtocol):
    def datagramReceived(self, datagram, address):

        parameter_names = {
            "Down Mhz": "downlink_frequency",
            "Down Mode": "downlink_mode",
            "Up MHz": "uplink_frequency",
            "Up Mode": "uplink_mode",
            "Azimuth": "azimuth",
            "Elevation": "elevation",
            "SatName": "name"
        }

        satellite_update = {}
        macdoppler_message_raw = re.findall(r'\[(.*)\]',str(datagram))

        if(macdoppler_message_raw[0][0:16] == "Sat Radio Report"):
            macdoppler_message = macdoppler_message_raw[0][17:]
            message_type = "frequency_mode_tone"

        if (macdoppler_message_raw[0][0:17] == "AzEl Rotor Report"):
            macdoppler_message = macdoppler_message_raw[0][18:]
            message_type = "azimuth_elevation"

        macdoppler_message_list = macdoppler_message.split(", ")

        for item in macdoppler_message_list:
            macdoppler_message_list[macdoppler_message_list.index(item)] = item.split(":")

        satellite_update["type"] = message_type
        satellite_update.update(dict(macdoppler_message_list))

        satellite_update = {parameter_names.get(k, k): v for k, v in satellite_update.items()}
        print(satellite_update)