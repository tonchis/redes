#Teoría de las comunicaciones

For academic purposes

##env Setup

Run `source .env/bin/activate` in the console before running the `iPython` console.

##iPython Setup

To start testing the methods included in the helpers file, each time the `iPython` console is started, these commands should be run:

```
import sys
sys.path.append("tp1")
sys.path.append("tmp")
import helpers
import scapy.all
```
##Other interesting stuff
About the difference between `import somemodule` and `from somemodule import *`

>If you import `somemodule` the contained globals will be available via `somemodule.someglobal`. If you `from somemodule import *` ALL its globals (or those listed in `__all__` if it exists) will be made globals, i.e. you can access them using `someglobal` without the module name in front of it.

>Using `from module import *` is discouraged as it clutters the global scope and if you import stuff from multiple modules you are likely to get conflicts and overwrite existing classes/functions.

##Exporting functional data from Wireshark
In Wireshark, use the `arp.opcode == 1 && !arp.isgratuitous` filter (arp.opcode corresponds to the ARP data and !arp.isgratuitous leaves out gratuitous requests).
Once the filter is applied, you have to export (not `save as`) by going to `File/Export Specified Packets`. In that window, after you chose the filename and directory, you have to select the `All packets` Packet Range to the left, and then chose the `Displayed` tab, to leave out those that don't match the filter. Then just click the `Save` button.
