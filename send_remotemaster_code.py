#!/usr/bin/env python3

# see also
#  Python pip package for Broadlink RM3/RM4: https://github.com/mjg59/python-broadlink
#  Broadlink protocol: https://github.com/mjg59/python-broadlink/blob/master/protocol.md
#  IR JP1 RC Configuration Tool : https://sourceforge.net/projects/controlremote/
#     This tool can be used to export .girr files from an existing config. You can also use it to find find hidden codes.
#  IR LowLevel Signal Tool : http://www.harctoolbox.org/IrScrutinizer.html
#     This tool can be used to learn and analyze codes
#  IR Lib : http://www.harctoolbox.org/IrpTransmogrifier.html, 
#  IR Lib (replaced by IrpTransmogrifier, part of RemoteMaster) : https://sourceforge.net/p/controlremote/code/HEAD/tree/trunk/decodeir/

#### constant definitions - adapt to your needs #########################################################################################################

ip_address = '192.168.1.71' # replace with you device ip address or leave empty to use auto discovery (takes longer)

# recorded from Broadlink
# Denon Receiver Power Toggle
packet_power = b'&\x00\xaa\x00\t\x1a\x08=\x08\x1a\t\x1a\x08\x1a\t<\t\x1a\x08\x1a\t\x1a\x08\x1a\t\x1a\t<\x08=\t\x19\t\x1a\x08\x00\x06\x0c\x08\x1a\t<\t\x1a\x08\x1a\t\x1a\x08\x1a\t<\t<\t<\t<\t<\t\x1a\x08\x1a\t<\t<\t\x00\x05\x81\t\x19\t<\t\x1a\x08\x1a\t\x1a\x08=\x08\x1a\t\x1a\x08\x1a\t\x1a\x08\x1a\t<\t<\t\x1a\x08\x1a\t\x00\x06\x0b\x08\x1a\t<\t\x1a\x08\x1a\t\x1a\x08\x1a\t<\t<\t<\t<\t=\x08\x1a\x08\x1a\t<\t<\t\x00\x05\x81\t\x19\t=\x08\x1a\t\x1a\x08\x1a\t<\t\x1a\x08\x1a\t\x1a\x08\x1a\t\x1a\x08=\x08=\x08\x1a\t\x1a\x08\x00\r\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# From Denon .girr file; power_on needs to be sent multiple times to work
girr_modulation_freq = 38
girr_denon_power_main_zone = "+264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264  -792 +264 -792 +264 -792 +264 -792 +264 -792  +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -43560 +264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264  -792 +264 -1848 +264 -1848 +264 -1848 +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -43560"
girr_denon_power_off       = "+264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264  -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -43560 +264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264  -792 +264 -1848 +264 -1848 +264 -1848 +264  -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -43560"
girr_denon_power_on        = "+264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264  -792 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -43560 +264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264  -792 +264 -1848 +264 -1848 +264 -1848 +264 -1848 +264  -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -43560"


#### main() function - adapt to your needs, e.g. choose the IR code you want  #########################################################################################################

import broadlink
import re

def main():
  #print(broadlink_to_girr_raw(packet_power))
  #print("packet_power_off={0}".format(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_off)))
  #print("packet_power_on={0}".format(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_on)))
  #print("packet_power_main_zone={0}".format(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_main_zone)))

  if(len(ip_address) > 0):
    device = broadlink.hello(ip_address)
  else:
    devices = broadlink.discover()
    device = devices[0]
    print("Using first found device {0}".format(device))

  device.auth() # when this fails, you need to disable "Lock Device" in the RM3/RM4 device settings

  #device.send_data(packet_power)
  #device.send_data(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_off))
  device.send_data(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_on))
  #device.send_data(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_main_zone))


#### Conversion functions - no need to modify #########################################################################################################

# from girr raw data to Broadlink packet format (suitable for https://github.com/mjg59/python-broadlink device.send_data()
girr_re = re.compile(r'\s*[-+](\d+)\s*')
def girr_raw_to_broadlink(modulation_freq_khz, girr_raw):
  result = girr_re.split(girr_raw)
  outdata=b''
  for x in result:
    if(x != ''):
      scaled = int(int(x) * 269 / 8192 + 0.5)
      if(scaled >= 256):
        outdata+=(scaled & 0xffff).to_bytes(3, 'big')
      else:
        outdata+=(scaled).to_bytes(1, 'big')

  outheader=(modulation_freq_khz).to_bytes(1, 'big')
  outheader+=((len(outdata) + 4) & 0xffff).to_bytes(2, 'big')
  outheader+=(0).to_bytes(1, 'big')
  return outheader + outdata


# from Broadcom recording to girr raw data in microseconds
def broadlink_to_girr_raw(broadlink_packet):
  l = len(broadlink_packet)
  out=""
  if(l >= 4):
    modulation_freq_khz = int(broadlink_packet[0])
    out += "# Modulation Frequency: {0} kHz\n".format(modulation_freq_khz)
    packet_len = int(broadlink_packet[2]) + (int(broadlink_packet[1]) << 8) # TODO: it is unclear how numbers over 255 are stored!
    out += "# Packet length: {0}\n".format(packet_len)
    #out += "# unknown: {0}\n".format(int(broadlink_packet[3]))

  sign="+"
  i = 4;
  while i < l:
    x = broadlink_packet[i]
    if(x == 0):
      if((l - i) > 2):
        x=broadlink_packet[i+1] * 256 + broadlink_packet[i+2]
        i+=2
      #else:
      #  print("Error: encoding error at offset {0}".format(i))

    out += "{0}{1} ".format(sign, int(x * 8192 / 269 + 0.5))
    if sign=="+":
      sign="-"
    else:
      sign="+"
    i+=1
  return out


main()
