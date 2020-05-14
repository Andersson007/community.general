#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: proxysql_mysql_users
author: "Ben Mildren (@bmildren)"
short_description: Adds or removes mysql users from proxysql admin interface.
description:
   - The M(proxysql_mysql_users) module adds or removes mysql users using the
     proxysql admin interface.
options:
  username:
    description:
      - Name of the user connecting to the mysqld or ProxySQL instance.
    required: True
  password:
    description:
      - Password of the user connecting to the mysqld or ProxySQL instance.
  active:
    description:
      - A user with I(active) set to C(False) will be tracked in the database,
        but will be never loaded in the in-memory data structures. If omitted
        the proxysql database default for I(active) is C(True).
    type: bool
  use_ssl:
    description:
      - If I(use_ssl) is set to C(True), connections by this user will be made
        using SSL connections. If omitted the proxysql database default for
        I(use_ssl) is C(False).
    type: bool
  default_hostgroup:
    description:
      - If there is no matching rule for the queries sent by this user, the
        traffic it generates is sent to the specified hostgroup.
        If omitted the proxysql database default for I(use_ssl) is 0.
  default_schema:
    description:
      - The schema to which the connection should change to by default.
  transaction_persistent:
    description:
      -  If this is set for the user with which the MySQL client is connecting
         to ProxySQL (thus a "frontend" user), transactions started within a
         hostgroup will remain within that hostgroup regardless of any other
         rules.
         If omitted the proxysql database default for I(transaction_persistent)
         is C(False).
    type: bool
  fast_forward:
    description:
      - If I(fast_forward) is set to C(True), I(fast_forward) will bypass the
        query processing layer (rewriting, caching) and pass through the query
        directly as is to the backend server. If omitted the proxysql database
        default for I(fast_forward) is C(False).
    type: bool
  backend:
    description:
      -  If I(backend) is set to C(True), this (username, password) pair is
         used for authenticating to the ProxySQL instance.
    default: True
    type: bool
  frontend:
    description:
      - If I(frontend) is set to C(True), this (username, password) pair is
        used for authenticating to the mysqld servers against any hostgroup.
    default: True
    type: bool
  max_connections:
    description:
      - The maximum number of connections ProxySQL will open to the backend for
        this user. If omitted the proxysql database default for
        I(max_connections) is 10000.
  state:
    description:
      - When C(present) - adds the user, when C(absent) - removes the user.
    choices: [ "present", "absent" ]
    default: present
extends_documentation_fragment:
- community.general.proxysql.managing_config
- community.general.proxysql.connectivity

'''

EXAMPLES = '''
---
# This example adds a user, it saves the mysql user config to disk, but
# avoids loading the mysql user config to runtime (this might be because
# several users are being added and the user wants to push the config to
# runtime in a single batch using the M(proxysql_manage_config) module).  It
# uses supplied credentials to connect to the proxysql admin interface.

- proxysql_mysql_users:
    login_user: 'admin'
    login_password: 'admin'
    username: 'productiondba'
    state: present
    load_to_runtime: False

# This example removes a user, saves the mysql user config to disk, and
# dynamically loads the mysql user config to runtime.  It uses credentials
# in a supplied config file to connect to the proxysql admin interface.

- proxysql_mysql_users:
    config_file: '~/proxysql.cnf'
    username: 'mysqlboy'
    state: absent
'''

RETURN = '''
stdout:
    description: The mysql user modified or removed from proxysql
    returned: On create/update will return the newly modified user, on delete
              it will return the deleted record.
    type: dict
    sample:
        changed: true
        msg: Added user to mysql_users
        state: present
        user:
            active: 1
            backend: 1
            default_hostgroup: 1
            default_schema: null
            fast_forward: 0
            frontend: 1
            max_connections: 10000
            password: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
            schema_locked: 0
            transaction_persistent: 0
            use_ssl: 0
            username: guest_ro
        username: guest_ro
'''

