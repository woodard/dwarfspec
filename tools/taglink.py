# Copyright 2012 DWARF Debugging Information Format Committee
#
# All DW_TAG_* entries not in {} are turned into \livelink.

import sys
import anylink

if __name__ == '__main__':
  anylink.read_file_args(["DW_TAG_"])
  


