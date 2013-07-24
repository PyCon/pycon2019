# This just exists to have something to use as a default settings
# that will try to use local_settings.py and give a useful error
# message if not found.

import sys

try:
    from local_settings import *
except ImportError:
    print("ERROR: A local_settings.py file is required but was not found.")
    print("You can copy local_settings.py-example to local_settings.py "
          "and edit it according to the comments.")
    sys.exit(1)
