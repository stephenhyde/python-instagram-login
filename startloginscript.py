#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from loginscript import LoginScript

login = LoginScript(sys.argv[1], sys.argv[2])

result = login.login()
print result
