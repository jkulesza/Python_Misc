Notebook_Creator
================

This Python script is used to create 8.5 x 11 (standard US Letter size) paper
with various features (name, date, page number, grids, etc) that could be used
as scratch paper or bound within a notebook.

In order to run this, you need to have additional packages available based on these lines:

```
from pyx import *
import numpy as np
import subprocess * import re
import datetime
```

In terms of non-standard packages, ```Pyx``` and ```Numpy``` are the ones you are not likely to have. Once they are installed, you can generate a test notebook as follows:

```
Python 2.7.8 (default, Jul  8 2014, 07:53:47) 
[GCC 4.2.1 Compatible Apple LLVM 5.1 (clang-503.0.40)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from Make_Notebook import *
>>> Make_Notebook()
Operating on Page 1
Operating on Page 2
Operating on Page 3
Operating on Page 4
Operating on Page 5
Operating on Page 6
Operating on Page 7
Operating on Page 8
Operating on Page 9
Operating on Page 10
>>> quit() 
```
