# This script is used for debugging.
# By importing this scripts, you can run your python project as usual. But when your program encounters some problem, the python
# process would come into the pdb debugging mode so that you don't need to restart and debug your code.

import sys

class ExceptionHook:
    instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            from IPython.core import ultratb
            self.instance = ultratb.FormattedTB(mode='Plain',
                 color_scheme='Linux', call_pdb=1)
        return self.instance(*args, **kwargs)

sys.excepthook = ExceptionHook()

