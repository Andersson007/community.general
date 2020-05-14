#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: proxysql_replication_hostgroups
author: "Ben Mildren (@bmildren)"
short_description: Manages replication hostgroups using the proxysql admin
                   interface.
description:
   - Each row in mysql_replication_hostgroups represent a pair of
     writer_hostgroup and reader_hostgroup. ProxySQL will monitor the value of
     read_only for all the servers in specified hostgroups, and based on the
     value of read_only will assign the server to the writer or reader
     hostgroups.
options:
  writer_hostgroup:
    description:
      - Id of the writer hostgroup.
    required: True
  reader_hostgroup:
    description:
      - Id of the reader hostgroup.
    required: True
  comment:
    description:
      - Text field that can be used for any purposes defined by the user.
  state:
    description:
      - When C(present) - adds the replication hostgroup, when C(absent) -
        removes the replication hostgroup.
    choices: [ "present", "absent" ]
    default: present
extends_documentation_fragment:
- community.general.proxysql.managing_config
- community.general.proxysql.connectivity

'''

EXAMPLES = '''
---
# This example adds a replication hostgroup, it saves the mysql server config
# to disk, but avoids loading the mysql server config to runtime (this might be
# because several replication hostgroup are being added and the user wants to
# push the config to runtime in a single batch using the
# M(proxysql_manage_config) module).  It uses supplied credentials to connect
# to the proxysql admin interface.

- proxysql_replication_hostgroups:
    login_user: 'admin'
    login_password: 'admin'
    writer_hostgroup: 1
    reader_hostgroup: 2
    state: present
    load_to_runtime: False

# This example removes a replication hostgroup, saves the mysql server config
# to disk, and dynamically loads the mysql server config to runtime.  It uses
# credentials in a supplied config file to connect to the proxysql admin
# interface.

- proxysql_replication_hostgroups:
    config_file: '~/proxysql.cnf'
    writer_hostgroup: 3
    reader_hostgroup: 4
    state: absent
'''

RETURN = '''
stdout:
    description: The replication hostgroup modified or removed from proxysql
    returned: On create/update will return the newly modified group, on delete
              it will return the deleted record.
    type: dict
    "sample": {
        "changed": true,
        "msg": "Added server to mysql_hosts",
        "repl_group": {
            "comment": "",
            "reader_hostgroup": "1",
            "writer_hostgroup": "2"
        },
        "state": "present"
    }
'''

