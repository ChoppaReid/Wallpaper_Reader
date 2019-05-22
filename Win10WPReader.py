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

print("BOOHOO:","Var: ",WP1,"\n	\nVar2: ",WP2)

"""

Hmm this is messy!
How to extract the file path from the registry subkeys without all the fluff ????
So need to understand how to convert REG Binary into normal string.


190523 0025: Just running first sync after creating GitHub repository for this little project
(it's way too late to be actually doing anything on this right now) :)

"""


# this one comes from: https://marc.info/?l=python-list&m=125087538012528&w=2

def __get_data(root_key, key, value):
    """This method gets the data from the given key and value under the root
    key.

    Args:
      root_key (str): The root key as abbreviated string.
                      Valid values: [hklm, hkcr, hkcu, hku, hkpd, hkcc].
      key (str): The subkey starting from the root key.
              e.g.: SYSTEM\CurrentControlSet\Services\Tcpip\Parameters
      value (str): The value to query.

    Returns:
      Str. It returns the retrieved data, or an empty string if data could not be retrieved.
    """
    data = ''
    try:
      hkey = winreg.OpenKey(root_key, key, 0, winreg.KEY_READ)
      data, regtype = winreg.QueryValueEx(hkey, value)
      print("MAR:", data, regtype)
      winreg.CloseKey(hkey)
    except WindowsError as e:
      logging.error('Error occurred getting registry data: {0}'.format(e))
    return data 

mygarb1 = __get_data(winreg.HKEY_CURRENT_USER,r'Control Panel\Desktop','TranscodedImageCache_000')
mygarb2 = __get_data(winreg.HKEY_CURRENT_USER,r'Control Panel\Desktop','TranscodedImageCache_001')
print("Here it is\n\t",mygarb1,"\n\t",mygarb2)

from winreg import *

hreg = ConnectRegistry(None, HKEY_CURRENT_USER)
hkey = OpenKey(hreg, 'Control Panel\Desktop')
accent_color_menu = QueryValueEx(hkey, 'TranscodedImageCache_000')[0]
CloseKey(hkey)
print("XX\n",accent_color_menu)

aKey = OpenKey(hreg, 'Control Panel\Desktop')
for i in range(1024):
    try:
        asubkey_name=EnumKey(aKey,i)
        asubkey=OpenKey(aKey,asubkey_name)
        val=QueryValueEx(asubkey, "DisplayName")
        print("BBB",val)
    except EnvironmentError:
        print("OOPS")
        break

