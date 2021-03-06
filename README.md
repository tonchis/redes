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

##TGF from .pcap files
TGF stands for Trivial Graphf Format and is a simple plain text format for describing graphs.
Once exported functional data from Wireshark into a .pcap file,  you could create a .tgf file with graph information ready to be plot.
1-Open a shell and move to the tp1 directory. 
2- Run the following command 'python tgfpcap.py pcapfile > outputfile.tgf count' where 'pcapfile'' stands for the pcap file you want to operate with and 'outputfile' refers to the file you want to save the output to. If count is positive the the first 'count' packages will be read. A negative 'count' will read all packages. Programs like Yed are able to open and operate with .tgf files. 

## graph.py
Uses Graphviz `.dot` file format to draw a graph from an ARP only `.pcap` file.

The following options are available:

* `-f` or `--file` is the path to the `.pcap` file.
* `-o` or `--output` is the path to the output `.dot` file.
* `-c` or `--count` use the first `count` packets in the capture file only.
* `-w` or `--weight` draws an edge if there was at least `weight` ARP requests between two nodes.
* `--ip` to see the activity for that `ip` only.

Example:

```bash
$ ./tp1/graph.py -f path/to/file.pcap -o "tmp/out.dot" -c 10000 -w 100 -ip "192.168.0.1"
```

