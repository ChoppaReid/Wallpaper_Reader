"""

Function code "regkey_value" for this experiment comes from: http://code.activestate.com/recipes/578689-get-a-value-un-windows-registry/

My GitHub: https://github.com/ChoppaReid
My Website: https://sites.google.com/view/choppas-crypt/home/

"""


import codecs
import winreg
import binascii

def regkey_value(path, name="", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        start_key = getattr(winreg, path[0])
        return regkey_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    with winreg.OpenKey(start_key, subkey) as handle:
        assert handle
        if path:
            return regkey_value(path, name, handle)
        else:
            desc, i = None, 0
            while not desc or desc[0] != name:
                desc = winreg.EnumValue(handle, i)
                i += 1
            return desc[1]

# example usage
# This can be setup as iterative once I have the basic "extract from registry" functionality sorted out!
WP1 = regkey_value(r"HKEY_CURRENT_USER\Control Panel\Desktop", "TranscodedImageCache_000").decode('latin-1')
WP2 = regkey_value(r"HKEY_CURRENT_USER\Control Panel\Desktop", "TranscodedImageCache_001").decode('latin-1')
# Would be better to setup above code to iterate all sub keys, then work on any matching "Trans....9999" name-formats

print("Var: ",WP1,"`n	`nVar2: ",WP2)

"""

Hmm this is messy!
How to extract the file path from the registry subkeys without all the fluff ????
So need to understand how to convert REG Binary into normal string.

"""