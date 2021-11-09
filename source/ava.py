#   ------------------------------------------------------   #
#                   ___  ____    ____  ___                   #
#                  /   \ \   \  /   / /   \                  #
#                 /  ^  \ \   \/   / /  ^  \                 #
#                /  /_\  \ \      / /  /_\  \                #
#               /  _____  \ \    / /  _____  \               #
#              /__/     \__\ \__/ /__/     \__\              #
#   ------------------------------------------------------   #
#       The main Atomic Virtual Analyser, AVA, program       #
#   ------------------------------------------------------   #
#            Writen from [insert paper reference]            #
#                     Copyright (c) 2021                     #
#   ------------------------------------------------------   #
#           Written by Ava Dean, Oxford, Nov. 2021           #
#   ------------------------------------------------------   #
#                                                            #
#              __..--''``---....___   _..._    __            #
#    /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /   #
#   ///_.-' _..--.'_    \                    `( ) ) // //    #
#   / (_..-' // (< _     ;_..__               ; `' / ///     #
#    / // // //  `-._,_)' // / ``--...____..-' /// / //      #
#                                                            #
#       This is Ava's catty, Smudge, not Schrödinger's       #
#                                                            #
#   ------------------------------------------------------   #


# Python modules.
from sys import argv

# AVA modules.
from model import Model
from program import setupProgram
from settings import readSettings


def main():
    # Call the preamble to process the arguments. If we don't exit then it will return the supplied system prefix.
    systemPrefix = preamble()

    # So now we've got here, we set up the main program based off the system prefix and add the first trace.
    prog = setupProgram(name=systemPrefix, initialTrace='main')

    # If we've gotten here, then we want a normal run and we have found an appropriate input file, let's process it.
    sttngs = readSettings(prog.stdIn)

    # Now we have settings from the input file, let's set up the model. This will create the system and its parameters.
    mdl = Model(settings=sttngs)

    # Do lots of other things...

    # And finally remove from the trace stracking.
    prog.exit('main')

    # And we're done!
    prog.stop(code=0)


def preamble():
    # Do we have access to any argument information at all?
    if len(argv) == 0:
        print('Fatal error, cannot access any argument information')
        exit(100)

    # Sort out the arguments, with file name removed, first.
    arguments = set([arg.strip() for arg in argv[1:] if arg.strip()])

    # Check if we have any arguments.
    needHelp = True if len(arguments) == 0 else False

    # See if we've asked for a search or info run.
    searchRun = arguments.intersection({'-s', '--search'})
    infoRun = arguments.intersection({'-i', '--info'})

    # Can't ask for both!
    needHelp = True if searchRun and infoRun else needHelp

    # If we aren't doing a search or info run, then we should only have one argument.
    needHelp = True if not searchRun and not infoRun and len(arguments) > 1 else needHelp

    # If we need help then show how to use AVA.
    if needHelp:
        print('Usage: ava <system-prefix>      : runs AVA on file <system-prefix>.inp')
        print('        "   [-s|--search]       : searches for specified keywords and/or blocks')
        print('        "   [-i|--info]         : outputs info for specified keywords and/or blocks')
        exit(0)

    if searchRun:
        searchTerms = arguments.difference({'-s', '--search'})
        searchTerms = {term.strip().lower() for term in searchTerms if term.strip()}

        search(searchTerms)

    if infoRun:
        infoTerms = arguments.difference({'-i', '--info'})
        infoTerms = {term.strip().lower() for term in infoTerms if term.strip()}

        info(infoTerms)

    # If we have got this far then we didn't need help, weren't doing a search run and weren't doing an info run.
    # So now we get the singly supplied argument and return it to main.
    systemPrefix = arguments.pop()

    return systemPrefix


def search(searchTerms: set = None):
    if len(searchTerms) == 0:
        print('Enter keywords or blocks to search for')
        exit(110)

    print('Search not yet implemented')

    exit(111)


def info(infoTerms: set = None):
    if len(infoTerms) == 0:
        print('Enter keywords or blocks to get info about')
        exit(120)

    print('Info not yet implemented')

    exit(121)


if __name__ == '__main__':
    main()
