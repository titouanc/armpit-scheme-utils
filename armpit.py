#!/usr/bin/env python

from serial import Serial
from os.path import basename
from sys import stdout
import re
import argparse

class Board:
    """Helper class to communicate with the Olimex LPC2214 Armpit scheme board"""

    clean_backspaces = re.compile(r'.\x08')
    clean_spaces = re.compile(r'[\r\n\s\t]+')
    clean_comments = re.compile(r';.*\n')
    find_defines = re.compile(r'\(\s*(?:define|set\!)\s+\(?\s*([^\s\)]+)')
    ENDL = "\r\n"

    def __init__(self, port):
        self.fd = Serial(port, 9600)

    def readline(self):
        """Return 1 line read from the board"""
        res = ""
        while not res.endswith("\r"):
            res += self.fd.read(1)
        return self.clean_backspaces.sub('', res.strip())

    def prompt(self):
        """Wait for the scheme interpreter prompt"""
        while self.fd.read(1) != ">":
            pass

    def check_output(self, output=stdout):
        """
        Wait for the scheme interpreter prompt,
        but print interpreter output in given file
        """
        c = self.fd.read(1)
        while c != ">":
            output.write(c)
            c = self.fd.read(1)
        print >>output

    def run_code(self, code, winsize=64):
        """
        Run given code in the board's scheme interpreter.
        @param code (str) The code to run
        @param winsize (int) How many bytes are sent at once through serial link
        """
        code = self.clean_comments.sub('', code) # Remove comments
        code = self.clean_spaces.sub(' ', code.strip()) # Remove multiple spaces
        cur = 0
        while cur < len(code):
            nxt = min(len(code), cur+winsize)
            self.fd.write(code[cur:nxt])
            while cur < nxt:
                c = self.fd.read(1)
                if c == code[cur]:
                    cur += 1
        self.fd.write(self.ENDL)

    def files(self):
        """Return the list of files stored on the board"""
        self.run_code("(files)")
        line = self.readline().strip()
        while not line.startswith("("):
            line = self.readline().strip()
        return map(lambda x: x.strip('"'), line.strip('()').split())

    def erase(self):
        """Erase all files on the board"""
        self.run_code("(erase)")

    def upload(self, name, code):
        """
        Upload a file to the board
        @param name (str) The name of the file to save
        @param code (str) The code that will be contained in this file.
        """
        return self.run_code("""
            (let ((port (open-output-file \"%s\")))
                (write '(begin %s) port)
                (close-output-port port))""" % (name, code))

    def upload_file(self, filename):
        """
        Upload a file from the host filesystem to the board
        @param filename (str) The location of the file to upload on the filesystem
        @note The file name will be the basename of the file on the filsesytem
        """
        return self.upload(basename(filename), open(filename).read())

    def interactive_repl(self):
        """Open an interactive REPL to the board, connected to stdin and stdout"""
        import readline
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        print "Interactive mode. Exit with CTRL+D or `exit`."
        print "Please press the RESET button if the '>' doesn't show up."

        self.run_code("")
        self.prompt()
        completable = set([
            "define", "let", "set!", "lambda", "exit", "set-input-pin!", 
            "set-output-pin!", "set-pin!", "is-pin-set?", "fill-rectangle!",
            "load", "erase"
        ])
        class Completer(object):
            match = []
            @classmethod
            def complete(self, text, state):
                if state == 0:
                    self.match = filter(lambda x: x.startswith(text), completable)
                try:
                    return self.match[state]
                except IndexError as err:
                    return None
        readline.set_completer(Completer.complete)
        readline.set_completer_delims(" ()")

        while True:
            try:
                scheme = raw_input("> ").strip()
                while scheme.count('(') != scheme.count(')'):
                    scheme += raw_input("...> ").strip()
                if scheme == "exit":
                    break
                if scheme:
                    self.run_code(scheme)
                    self.check_output()
                    match = self.find_defines.search(scheme)
                    if match:
                        completable.add(match.group(1))
            except KeyboardInterrupt:
                print
            except EOFError:
                break
        print

if __name__ == "__main__":
    optparser = argparse.ArgumentParser(
        description="Small utility for Olimex LPC2214 running ARMpit Scheme"
    )
    optparser.add_argument(
        '-p', '--port', type=str,
        action='store', dest='serial_port', default="/dev/ttyUSB0",
        help="Serial port to use (/dev/ttyUSB0)"
    )
    optparser.add_argument(
        '-u', '--upload', type=str,
        action='store', dest='upload', default=None,
        help="Upload this file to the board (will be basenamed)"
    )
    optparser.add_argument(
        '-l', '--list',
        action='store_true', dest='list', default=False,
        help="List files currently on board"
    )
    optparser.add_argument(
        '-r', '--erase',
        action='store_true', dest='erase', default=False,
        help="Erase files on board"
    )
    optparser.add_argument(
        '-e', '--execute-command', type=str,
        action='store', dest='command', default=None,
        help="Execute command on board and print results on stdout"
    )
    optparser.add_argument(
        '-f', '--execute-file', type=str,
        action='store', dest='file', default=None,
        help="Execute named file on board and print results on stdout"
    )
    optparser.add_argument(
        '-y', '--upload-exec',
        action='store_true', dest='upload_exec', default=False,
        help="Execute file right after uploading"
    )
    optparser.add_argument(
        '-i', '--interactive',
        action='store_true', dest='interactive', default=False,
        help="Open an interactive REPL to the board"
    )

    OPTIONS = optparser.parse_args()
    board = Board(OPTIONS.serial_port)

    if OPTIONS.erase:
        board.erase()
        board.prompt()
        print "Files erased from board"

    if OPTIONS.upload:
        board.upload_file(OPTIONS.upload)
        board.prompt()
        print "Uploaded", OPTIONS.upload

    if OPTIONS.list:
        print "Files on board:"
        for f in board.files():
            print "-", f

    if OPTIONS.upload and OPTIONS.upload_exec:
        OPTIONS.file = OPTIONS.upload

    if OPTIONS.file:
        board.run_code('(load "%s")' % (OPTIONS.file))
        board.check_output()

    if OPTIONS.command:
        board.run_code(OPTIONS.command)
        board.check_output()

    if OPTIONS.interactive:
        board.interactive_repl()