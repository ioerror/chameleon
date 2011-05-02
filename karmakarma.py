#!/usr/bin/python
#
# chameleon - chameleon helps ammend modify edit list enumerate ordered names
#
#

import ctypes
import ctypes.util
import time
import sys
libc = ctypes.CDLL(ctypes.util.find_library("c"))

class chameleon:
    """Set a custom process name for a program"""
    def __init__(self, new_name=None):
        ################################################
        # import names from /usr/include/linux/prctl.h #
        ################################################
        self.PR_SET_NAME=15
        self.PR_GET_NAME=16
        self.max_size=1608 # This is alignment related and probably wrong
        self.Py_GetArgcArgv = ctypes.pythonapi.Py_GetArgcArgv
        self.argv_ptr = ctypes.POINTER(ctypes.c_char_p)
        self.Py_GetArgcArgv.restype = None
        self.Py_GetArgcArgv.argtypes = [ctypes.POINTER(ctypes.c_int),
                                        ctypes.POINTER(self.argv_ptr)]
        if not new_name:
            self.set_name("chameleon")
        else:
            self.set_name(new_name)
        if sys.platform == "linux2": # What other platforms use prctl?
            self.get_prctl_name()
        #print str(self.get_arg_name())
        #print str(self.get_prctl_name())

    def set_name(self, new_name):
        self.set_arg_name(new_name)
        if sys.platform == "linux2": # What other platforms use prctl?
            self.set_prctl_name(new_name)

    def set_arg_name(self, new_name):
        self.argc = ctypes.c_int(0)
        self.argv = self.argv_ptr()
        self.Py_GetArgcArgv(self.argc, ctypes.pointer(self.argv))
        size = len(new_name)
        if size >= self.max_size:
          size = self.max_size
        ctypes.memset(self.argv.contents, 0, (size + 1)) # We're terminated
        ctypes.memmove(self.argv.contents, new_name, size)

    def get_arg_name(self):
        self.argc = ctypes.c_int(0)
        self.argv = self.argv_ptr()
        self.Py_GetArgcArgv(self.argc, ctypes.pointer(self.argv))
        size = len(str(self.argv.contents.value))
        current_name = ctypes.create_string_buffer((size + 1))
        ctypes.memmove(current_name, self.argv.contents, size)
        return str(current_name.value)

    # These appear to be Linux specific - other platform specific stuff should
    # go below here - This is a max of 15 chars long on Linux...
    def set_prctl_name(self, new_name):
        name = ctypes.create_string_buffer(len(new_name)+1)
        name.value = new_name
        libc.prctl(self.PR_SET_NAME, ctypes.byref(name), 0, 0, 0)

    def get_prctl_name(self):
        current_name = ctypes.create_string_buffer(256)
        libc.prctl(self.PR_GET_NAME, ctypes.byref(current_name), 0, 0, 0)
        return str(current_name.value)

if __name__ == "__main__":
  print "chameleon usage:"
  print "import karmakarma"
  print "karmakarma.chameleon('/usr/lib/openssh/sftp-server')"
