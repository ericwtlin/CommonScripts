# -*- coding: utf-8 -*-
"""


Authors:    Wutao Lin
Date:       17/10/23 下午4:19
"""

def copy_file(source_path, dest_path):
    """copy file
    Args:
        source_path:
        dest_path:
    Returns:

    """
    open(dest_path, 'wb').write(open(source_path, 'rb').read())