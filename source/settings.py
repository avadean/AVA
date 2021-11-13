#   ------------------------------------------------------   #
#                   -*- S E T T I N G S -*-                  #
#   ------------------------------------------------------   #
#     This module contains all information in regards to     #
#       the settings of the calculation. This includes       #
#      keywords and blocks, and also processing of input     #
#                           files.                           #
#   ------------------------------------------------------   #
#            Writen from [insert paper reference]            #
#                     Copyright (c) 2021                     #
#   ------------------------------------------------------   #
#         Module author: Ava Dean, Oxford, Nov. 2021         #
#   ------------------------------------------------------   #


from data import stringToValue
from program import getFileLines


settingTypes = {}


def setting(key: str = None, prog=None, **kwargs):
    prog.enter('setting')

    key = key.strip().lower()

    settingObject = settingTypes.get(key, None)

    if settingObject is None:
        prog.abort(f'Key {key} does not correspond to setting')

    newSetting = settingObject(key=key, **kwargs)

    prog.leave('setting')

    return newSetting


def readSettings(fileName: str = None, prog=None):
    prog.enter('readSettings')

    lines = getFileLines(file=fileName, prog=prog)

    lines = [line.strip() for line in lines if line.strip()]

    lines = [line for line in lines if not line.startswith('#') and not line.startswith('!')]

    settingKey = ''
    settingKeyOther = ''
    inBlock = False
    blockLines = []

    settings = []

    for line in lines:

        # Check for comments.
        for commentChar in ('#', '!'):
            comment = line.find(commentChar)

            # Remove it if need be.
            if comment != -1:
                line = line[:comment].strip()

        if inBlock:
            # Don't lower() line before as we may want capitalisation.
            if line.lower().startswith('%'):

                # Get rid of the '%' - don't need capitalisation now
                line = line[1:].strip().lower()

                # Check that there is only one string.
                settingKeys = line.split()
                if len(settingKeys) == 1:
                    settingKeyOther = settingKeys[0]
                else:
                    prog.abort(f'Error in block in line \'{line}\' of file {fileName}')

                if settingKey != settingKeyOther:
                    prog.abort(f'Entered block {settingKey} but found endblock {settingKeyOther}')

                arguments = {'lines': blockLines}

                newSetting = setting(key=settingKey, prog=prog, **arguments)

                settings.append(newSetting)

                # We have now exited a block.
                inBlock = False
                blockLines = []
            else:
                blockLines.append(line)

        else:
            # Don't lower() line before as we may want capitalisation if it is not a block.
            if line.lower().startswith('%'):

                # Get rid of the '%' - don't need capitalisation now
                line = line[1:].strip().lower()

                # We have now entered a block.
                inBlock = True
                blockLines = []

                # Check that there is only one string.
                settingKeys = line.split()
                if len(settingKeys) == 1:
                    settingKey = settingKeys[0]
                else:
                    prog.abort(f'Error in block in line \'{line}\' of file {fileName}')

            else:
                # If we're here then we have a keyword.

                parts = line.split()
                parts = [part.strip() for part in parts if part.strip() not in (':', '=')]

                if len(parts) == 1:
                    # e.g. symmetry_generate
                    key = parts[0].lower()
                    value = True

                    arguments = {'value': value}

                elif len(parts) == 2:
                    key = parts[0].lower()
                    value = stringToValue(parts[1])

                    arguments = {'value': value}

                elif len(parts) == 3:
                    key = parts[0].lower()
                    value = stringToValue(parts[1])
                    unit = parts[2]

                    arguments = {'value': value, 'unit': unit}

                elif len(parts) == 4:
                    # e.g. kpoints_mp_grid : 1.0 1.0 1.0
                    key = parts[0].lower()
                    value = stringToValue(' '.join(parts[1:3]))

                    arguments = {'value': value}

                else:
                    raise ValueError(f'Error in keyword {line} of file {fileName}')

                newSetting = setting(key=key, prog=prog, **arguments)

                settings.append(newSetting)

    prog.leave('readSettings')

    return settings
