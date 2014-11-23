# ArmPit scheme utils

A small utility to communicate with an LPC-2214 Olimex board running ArmPit
scheme. 

This is [the board](http://prog.vub.ac.be/~cderoove/project/armpit_scheme.pdf)
used for the [SICP course](http://soft.vub.ac.be/soft/content/structure-and-interpretation-computer-programs-taught-english)
project at VUB.

Requires pyserial (`pip install pyserial` or `apt-get install python-serial`)

## Usage

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
      -f FILE, --execute-file FILE
                        Execute named file on board and print results on
                        stdout
      -y, --upload-exec     Execute file right after uploading

## Examples

    # List files
    $ ./armpit.py -l
    Files on board:
    - lib

    # Execute a scheme snippet on board
    $ ./armpit.py -e '(display "Hello world")'
    Hello world

    # Upload a file ...
    $ ./armpit.py -u screen.scm 
    Uploaded screen.scm

    # ... then load it
    $ ./armpit.py -f screen.scm 

    # Upload and load a file
    $ ./armpit.py -yu blink.scm 
    Uploaded blink.scm

    $ ./armpit.py -r
    Files erased from board

