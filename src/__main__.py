import sys

import termuxgui.oo as tgo
from activity import PackageActivity

try:
    with tgo.Connection() as c:
        c.launch(PackageActivity)
        c.event_loop()
except KeyboardInterrupt:
    print()
    sys.exit(1)