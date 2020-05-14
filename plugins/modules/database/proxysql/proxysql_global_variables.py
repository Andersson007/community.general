#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: proxysql_global_variables
author: "Ben Mildren (@bmildren)"
short_description: Gets or sets the proxysql global variables.
description:
   - The M(proxysql_global_variables) module gets or sets the proxysql global
     variables.
options:
  variable:
    description:
      - Defines which variable should be returned, or if I(value) is specified
        which variable should be updated.
    required: True
  value:
    description:
      - Defines a value the variable specified using I(variable) should be set
        to.
extends_documentation_fragment:
- community.general.proxysql.managing_config
- community.general.proxysql.connectivity

'''

EXAMPLES = '''
---
# This example sets the value of a variable, saves the mysql admin variables
# config to disk, and dynamically loads the mysql admin variables config to
# runtime. It uses supplied credentials to connect to the proxysql admin
# interface.

- proxysql_global_variables:
    login_user: 'admin'
    login_password: 'admin'
    variable: 'mysql-max_connections'
    value: 4096

# This example gets the value of a variable.  It uses credentials in a
# supplied config file to connect to the proxysql admin interface.

- proxysql_global_variables:
    config_file: '~/proxysql.cnf'
    variable: 'mysql-default_query_delay'
'''

RETURN = '''
stdout:
    description: Returns the mysql variable supplied with it's associated value.
    returned: Returns the current variable and value, or the newly set value
              for the variable supplied..
    type: dict
    "sample": {
        "changed": false,
        "msg": "The variable is already been set to the supplied value",
        "var": {
            "variable_name": "mysql-poll_timeout",
            "variable_value": "3000"
        }
    }
'''

