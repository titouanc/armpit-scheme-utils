A small utility to communicate with an LPC-2214 Olimex board running ArmPit
scheme. 

This is [the board](http://prog.vub.ac.be/~cderoove/project/armpit_scheme.pdf)
used for the [SICP course](http://soft.vub.ac.be/soft/content/structure-and-interpretation-computer-programs-taught-english)
project at VUB.

    $ ./armpit.py -h
    usage: armpit.py [-h] [-p SERIAL_PORT] [-u UPLOAD] [-l] [-r] [-e EXECUTE]

    Small utility for Olimex LPC2214 running ARMpit Scheme

    optional arguments:
      -h, --help            show this help message and exit
      -p SERIAL_PORT, --port SERIAL_PORT
                            Serial port to use (/dev/ttyUSB0)
      -u UPLOAD, --upload UPLOAD
                            Upload this file to the board (will be basenamed)
      -l, --list            List files currently on board
      -r, --erase           Erase files on board
      -e EXECUTE, --execute EXECUTE
                            Execute command on board and print results on stdout
                            