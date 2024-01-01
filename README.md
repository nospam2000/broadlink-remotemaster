# broadlink-remotemaster
Send IR commands via Broadlink RM3 / RM4 from RemoteMaster code definitions (IrScrutinizer .girr format)
This repo contains two functions to map from the .girr format used by the mentioned tools to the Broadlink format for an easy exchange.

RemoteMaster and its ecosystem define the IR codes with a high level DSL. It is mainly used to configure the OFA (One For All) IR remote controls.
You can find lots of codes for many devices and there is a great active community in [the JP1 Forum](http://www.hifi-remote.com/forums/)
There are also lots of tools like IrScrutinizer which help customizing your remote control.

[Here](http://www.hifi-remote.com/forums/dload.php?action=file&file_id=13367) you can find a Denon X4000 .rmdu file which can be converted to .girr format using RemoteMaster. You need to create an account to be able to download the file.

## Installation

This tool requires Python 3 and the python package `broadlink`

I'm using [Pipenv](https://pipenv.pypa.io/en/latest/installation.html) to mange my virtual Python environments.
When you don't use it, replace the `pipenv shell` command below with your choice.

Commands to install Python packge dependencies
````bash
git clone https://github.com/nospam2000/broadlink-remotemaster
cd broadlink-remotemaster
pipenv shell
pip3 install -r requirements.txt
````

## Usage

There are two Python conversion functions which convert from the ASCII based .girr format to the binary Broadlink format:
1. girr_raw_to_broadlink(modulation_freq_khz, girr_raw)
2. broadlink_to_girr_raw(broadlink_packet)

The .girr file can be exported from RemoteMaster, here a small excerpt:
````xml
<raw frequency="38000">
  <repeat>+264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -43560 +264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -43560</repeat>
</raw>
````

Here an example how to use it in the Python code:
````python
girr_modulation_freq = 38
girr_denon_power_on  = "+264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264 -1848 +264  -792 +264 -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -1848 +264 -792 +264 -792 +264 -43560 +264 -792 +264 -1848 +264 -792 +264 -792 +264 -792 +264  -792 +264 -1848 +264 -1848 +264 -1848 +264 -1848 +264  -792 +264 -792 +264 -792 +264 -1848 +264 -1848 +264 -43560"
device.send_data(girr_raw_to_broadlink(girr_modulation_freq, girr_denon_power_on))
````

