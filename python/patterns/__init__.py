# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder

import os
import importlib
__all__ = [
    importlib.import_module('.%s' % filename, __package__)
    for filename in [
            os.path.splitext(f)[0]
            for f in os.listdir(os.path.dirname(__file__))
            if f.endswith('.py') and not f.startswith('_')
    ]
]
del os, importlib
