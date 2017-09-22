#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from loginscript import LoginScript

login = LoginScript(sys.argv[1], sys.argv[2], sys.argv[3])

result = login.login()
login.logout()

print result
