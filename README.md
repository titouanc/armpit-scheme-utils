# ArmPit scheme utils

A small utility to communicate with an LPC-H2214 Olimex board running ArmPit
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

    # Remove files
    $ ./armpit.py -r
    Files erased from board

    # Interactive REPL
    $ ./armpit.py -i
    Interactive mode. Exit with CTRL+D or `exit`.
    > (define (range min max) (if (= min max) '() (cons min (range (+ 1 min) max))))
    
    > (range 0 100)
    (0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29
    30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56
    57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83
    84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99)
    > (apply + (map (lambda (x) (* x x)) (range 0 1000)))
    332833500 
    > exit
