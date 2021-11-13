#   ------------------------------------------------------   #
#                    -*- P R O G R A M -*-                   #
#   ------------------------------------------------------   #
#        This module contains the main global program        #
#     variable and routines relating to files; input and     #
#                output; and error handling.                 #
#   ------------------------------------------------------   #
#            Writen from [insert paper reference]            #
#                     Copyright (c) 2021                     #
#   ------------------------------------------------------   #
#         Module author: Ava Dean, Oxford, Nov. 2021         #
#   ------------------------------------------------------   #


from pathlib import Path


class Program:
    def __init__(self, name: str = None):
        # Name of the calculation is the prefix of the system supplied.
        self.name = name

        # Set up the stack.
        self.stack = []

        # Log what files are open.
        self.openFiles = []

        # Get error file first.
        self.stdErrName = self.getErrorFile()
        # Now we have an error file, we don't need any hard exits.

        # Get input file name
        self.stdInName = f'{self.name}.inp'

        # If it doesn't exist, then abort.
        if not fileExists(self.stdInName):
            self.abort(f'Cannot find input file, {self.stdInName}')

        ## Otherwise, open the file.
        #self.stdIn = self.openFile(file=stdIn, mode='rt')

        # Get standard output file.
        self.stdOut = self.openFile(file=f'{self.name}.out', mode='at')

    def openFile(self, file: str = None, mode: str = 'a'):
        openFile = open(file=file, mode=mode)

        self.openFiles.append(openFile)

        return openFile

    def closeFiles(self, *files):
        for file in files:
            if file not in self.openFiles:
                self.abort(f'Cannot close file {file} as it is not open')

            file.close()

            self.openFiles.remove(file)

    def getErrorFile(self):
        for n in range(1000):
            fileName = f'{self.name}-{n}.err'

            if not fileExists(fileName):
                return fileName

        print('Fatal error, cannot create error file')
        exit(101)

    def abort(self, msg: str = '', code: int = 1):
        # Create a string of the trace stack.
        traceStack = '\n  '.join(self.stack)

        # And zero it to prevent recursion.
        self.stack = []

        # Then write the error message and stack to the error file.
        with open(file=self.stdErrName, mode='at') as stdErr:
            stdErr.write(f'{msg}\nTrace stack:\n  {traceStack}')

        # And stop!
        self.stop(code=code)

    def stop(self, code: int = 0):
        if len(self.stack) != 0:
            self.abort('Trace stack not empty on stop', code=2)

        # Close any open files.
        self.closeFiles(*self.openFiles)

        # And finally exit.
        exit(code)

    def enter(self, item: str = None):
        self.stack.append(item)

    def leave(self, item: str = None):
        lastItem = self.stack.pop()

        if lastItem != item:
            self.stack.append(lastItem)
            self.abort(f'Trace stack error: tried to remove {item} but found {lastItem}')


def fileExists(file: str = None):
    return Path(file).is_file()


def getFileLines(file: str = None, prog: Program = None):
    prog.enter('getFileLines')

    if not fileExists(file):
        prog.abort(f'Cannot find file {file} when reading settings')

    with open(file) as openFile:
        lines = openFile.read().splitlines()

    prog.leave('getFileLines')

    return lines
