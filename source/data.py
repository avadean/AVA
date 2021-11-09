#   ------------------------------------------------------   #
#                       -*- D A T A -*-                      #
#   ------------------------------------------------------   #
#     This module contains a large range of data used in     #
#      calculations. This includes values for constants,     #
#     values for atomic properties, handling of variables    #
#           in the code, amongst many other things.          #
#   ------------------------------------------------------   #
#            Writen from [insert paper reference]            #
#                     Copyright (c) 2021                     #
#   ------------------------------------------------------   #
#         Module author: Ava Dean, Oxford, Nov. 2021         #
#   ------------------------------------------------------   #


from numpy import array


def stringToValue(value: str = None):
    value = value.strip()

    if value.lower() in ['t', 'true']:
        return True

    elif value.lower() in ['f', 'false']:
        return False

    elif isInt(value):
        return int(float(value))

    elif isFloat(value):
        return float(value)

    elif isVectorInt(value):
        return array(value.split(), dtype=int)

    elif isVectorFloat(value):
        return array(value.split(), dtype=float)

    else:
        return value


def isInt(*xList):
    for x_i in xList:
        try:
            a = float(x_i)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            if a != b:
                return False

    return True


def isFloat(*xList):
    for x_i in xList:
        try:
            float(x_i)
        except (TypeError, ValueError):
            return False

    return True


def isVectorInt(vector: str = None):
    return True if all(isInt(part) for part in vector.split()) else False


def isVectorFloat(vector: str = None):
    return True if all(isFloat(part) for part in vector.split()) else False
