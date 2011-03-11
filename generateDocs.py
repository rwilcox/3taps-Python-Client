""" generateDocs.py

    This Python program generates the Python API wrapper documentation from the
    wrapper source files.
"""
import pydoc, glob, os
import shutil
from os.path import isdir
from re import search,sub
from copy import copy 

#############################################################################
 
SRC_DIR = 'threetaps' # Where to find our source modules.
DOC_DIR = 'doc'       # Where to place our documentation files.
pydoc.writing = 1 
 
#############################################################################
 
def buildFileList(base_name):
    """ Recursively generate a list of files and directories to document.
    
        'base_name' is the relative path to add to directories and files.
        Note that we ignore any __init__.py files.
    """
    filelist = [f for f in glob.glob(base_name + '/*')
                if (isdir(f) or search('.py$', f))
                and not search('__init__.py', f)]
    for f in copy(filelist):
        if isdir(f):
            filelist = filelist + buildFileList(f)
    return filelist

#############################################################################

def filenameToDocname(f):
    """ Convert a path name into the PyDoc filename it will turn into.
    
        If the path name ends in a .py, then it is cut off. If there is no
        extension, the name is assumed to be a directory.
    """
    f = sub('/', '.', f)
    if search('.py$', f):
        f = sub('.py$', '.html', f)
    else:
        f = f + '.html'
    return f

#############################################################################

def filenameToPackagename(f):
    """ Convert a path name into the Python dotted-notation package name.
    
        If the name ends in a .py, then cut it off.  If there is no extension,
        the name is assumed to be a directory, and nothing is done other than
        to replace the '/' with '.'
    """
    f = sub('/', '.', f)
    if search('.py$', f):
        f = sub('.py$', '', f)
    return f

#############################################################################

def main():
    """ Generate all pydoc documentation files within our "doc" directory.

        After generation, there will be an index.html file that displays all
        the modules.
    """
    # Remove the existing documentation files, if any.

    if os.path.exists(DOC_DIR):
        shutil.rmtree(DOC_DIR)
    os.mkdir(DOC_DIR)

    # Create the new documentation files.

    filelist = buildFileList(SRC_DIR) + [SRC_DIR]
    for fName in filelist:
        f = filenameToDocname(fName)
        if not glob.glob(DOC_DIR + '/' + fName):
            pydoc.writedoc(filenameToPackagename(fName))
        if glob.glob(fName):
            cmd = 'mv -f ' + f + ' ' + DOC_DIR + '/'
            os.system(cmd)
        else:
            filelist.remove(fName)

    # Finally, rename the top-level file to "index.html" so it can be accessed
    # easily.

    cmd = 'mv ' + DOC_DIR + '/threetaps.html ' + DOC_DIR + '/index.html'
    os.system(cmd)

#############################################################################

if __name__ == "__main__":
    main()

