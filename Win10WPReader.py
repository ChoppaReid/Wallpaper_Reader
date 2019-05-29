"""

Function code "regkey_value" for this experiment comes from: http://code.activestate.com/recipes/578689-get-a-value-un-windows-registry/

Function code "explore"      for this experiment comes from: https://stackoverflow.com/questions/281888/open-explorer-on-a-file

My GitHub: https://github.com/ChoppaReid
My Website: https://sites.google.com/view/choppas-crypt/home/

Assumptions:
	You're using Windows 10
	You have dual screens (although single screen appears to work also)
	You want to know where the source files for your wallpaper displays are (not just Windows' bastardized copies)
	I'm assuming this will only work on westernized systems, so happy to hear from anyone using other code-pages to see if it actually works.
	
	PS: I use TABS not SPACES

NOTE: 
	This does not OPEN a file!
	It simply takes a file and points to it in windows explorer.

	This is all written in python 3.7.3
"""

import winreg																		#	handles registry stuff (in python-2 it would be _winreg)
import subprocess																	#	used to call file-explorer open-folder/select-file
import os																			#	python 3 OS path handling stuff

"""
The below example is my reg binary reader which gets the wallpaper locations from registry.
The actual explorer file locater is "explore" function below.
"""

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

"""
The below example "explore" can utilize variable input.
Will also correct path definitions when required (unix to windows)
"""

def explore(path):
	# explorer would choke on forward slashes
	FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
	path = os.path.normpath(path)
	if os.path.isdir(path):
		subprocess.run([FILEBROWSER_PATH, path])									#	Only a folder was given, so just open the folder
	elif os.path.isfile(path):
		subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])		#	here is where we tell explorer to select our file
	return

# stripRegCrud simply cleans up a reg binary key.
# removes all NULL values and any pre/post crud in the key value
def stripRegCrud(file):
	crud = ':\\'																	#	Search for a "drive like" representation eg: ":\"
	file = file.replace('\00', '')													#	strip out all NULL chars
	file = (file[(file.find(crud) - 1):(file.find(r"\\"))])							#	Trim out the remaining crud from registry entry
	return file

# example usage - 'latin-1' is the generic "do all" for most "westernized" code-pages (or so I believe)
WP1 = regkey_value(r"HKEY_CURRENT_USER\Control Panel\Desktop", "TranscodedImageCache_000").decode('latin-1')
WP2 = regkey_value(r"HKEY_CURRENT_USER\Control Panel\Desktop", "TranscodedImageCache_001").decode('latin-1')
# Would be better to iterate all sub keys, then work on any matching "Trans....9999" values
# I'll get round to that, eventually!

WP1 = stripRegCrud(WP1)																#	Let's clean up this key value so it's usable
WP2 = stripRegCrud(WP2)

print("\n\tWallpaper 1 is: ",WP1)													#	Just showing user what they're getting
print("\tWallpaper 2 is: ", WP2)

explore(WP1)																		#	Call explore function and highlight requested file
explore(WP2)

"""
The below example is primitive, can only utilize fixed strings.
Hence being moved into a comment (The other example above is FAR superior)
"""
#subprocess.Popen(r'explorer /select,"C:\Users\Mark Reid\Pictures\Wallpapers\44f6e5ak3315cee8aae7334.jpg"')
