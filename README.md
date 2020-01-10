# DummyRDM #
DummyRDM is a tool for testing various controllers within an RDM network. Transport is provided via E1.33 RDMNet, Art-Net, and LLRP

[![Documentation Status](https://readthedocs.org/projects/dummyrdm/badge/?version=latest)](https://dummyrdm.readthedocs.io/en/latest/?badge=latest)

## Motivation ##
I created this tool while developing LXNetTools as a means of creating a flexible framework for testing new device features in a fully controllable and customisable manner. 

## About the project ##
For ease of prototyping new features and portability, DummyRDM has been written in Python3, and tested on Mac OSX and Ubuntu (Windows pending). There's still a lot I need to tidy up while adding new features at the same time though it's functional, and over time I'm slowly getting rid of some ugly, repetitive code and making it more readable. 

## Docs and usage ##
Simply running `python3 main.py` from the root of the project should start up a basic test "node" with a 12 port, Artnet V4 node, a single RDM device with a randomly generated UID/CID, and LLRP/E1.33 responders. At present, most of the API has **some** documentation, even if it isn't perfect yet, but this is something I'm trying to tidy up. 
For example:  
```python
devicestore[1] = rdmdevice.rdmdevice()
devicestore[1].start()
artnetengne.registerdevice(1, 1)
```
Will add a new device to the devicestore, start the thread for the LLRP responder, and register it with the Art-net engine at port 1


## Credits ##
Standards used in the development of this include E1.20 Remote Device Management, and E1.37-x extension PIDS, and E1.33 RDMNet, both available for download from [The ESTA TSP documents page](https://tsp.esta.org/tsp/documents/published_docs.php)

This application makes use of Art-Net™ Designed by and Copyright Artistic Licence Holdings Ltd. [Read the Art-Net 4 standard here](https://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf)


## License ##
This application is released under an MIT license, see the license file for more details