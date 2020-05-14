#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: proxysql_backend_servers
author: "Ben Mildren (@bmildren)"
short_description: Adds or removes mysql hosts from proxysql admin interface.
description:
   - The M(proxysql_backend_servers) module adds or removes mysql hosts using
     the proxysql admin interface.
options:
  hostgroup_id:
    description:
      - The hostgroup in which this mysqld instance is included. An instance
        can be part of one or more hostgroups.
    default: 0
  hostname:
    description:
      - The ip address at which the mysqld instance can be contacted.
    required: True
  port:
    description:
      - The port at which the mysqld instance can be contacted.
    default: 3306
  status:
    description:
      - ONLINE - Backend server is fully operational.
        OFFLINE_SOFT - When a server is put into C(OFFLINE_SOFT) mode,
                       connections are kept in use until the current
                       transaction is completed. This allows to gracefully
                       detach a backend.
        OFFLINE_HARD - When a server is put into C(OFFLINE_HARD) mode, the
                       existing connections are dropped, while new incoming
                       connections aren't accepted either.

        If omitted the proxysql database default for I(status) is C(ONLINE).
    choices: [ "ONLINE", "OFFLINE_SOFT", "OFFLINE_HARD"]
  weight:
    description:
      - The bigger the weight of a server relative to other weights, the higher
        the probability of the server being chosen from the hostgroup. If
        omitted the proxysql database default for I(weight) is 1.
  compression:
    description:
      - If the value of I(compression) is greater than 0, new connections to
        that server will use compression. If omitted the proxysql database
        default for I(compression) is 0.
  max_connections:
    description:
      - The maximum number of connections ProxySQL will open to this backend
        server. If omitted the proxysql database default for I(max_connections)
        is 1000.
  max_replication_lag:
    description:
      - If greater than 0, ProxySQL will regularly monitor replication lag. If
        replication lag goes above I(max_replication_lag), proxysql will
        temporarily shun the server until replication catches up. If omitted
        the proxysql database default for I(max_replication_lag) is 0.
  use_ssl:
    description:
      - If I(use_ssl) is set to C(True), connections to this server will be
        made using SSL connections. If omitted the proxysql database default
        for I(use_ssl) is C(False).
    type: bool
  max_latency_ms:
    description:
      - Ping time is monitored regularly. If a host has a ping time greater
        than I(max_latency_ms) it is excluded from the connection pool
        (although the server stays ONLINE). If omitted the proxysql database
        default for I(max_latency_ms) is 0.
  comment:
    description:
      - Text field that can be used for any purposed defined by the user.
        Could be a description of what the host stores, a reminder of when the
        host was added or disabled, or a JSON processed by some checker script.
    default: ''
  state:
    description:
      - When C(present) - adds the host, when C(absent) - removes the host.
    choices: [ "present", "absent" ]
    default: present
extends_documentation_fragment:
- community.general.proxysql.managing_config
- community.general.proxysql.connectivity

'''

EXAMPLES = '''
---
# This example adds a server, it saves the mysql server config to disk, but
# avoids loading the mysql server config to runtime (this might be because
# several servers are being added and the user wants to push the config to
# runtime in a single batch using the M(proxysql_manage_config) module).  It
# uses supplied credentials to connect to the proxysql admin interface.

- proxysql_backend_servers:
    login_user: 'admin'
    login_password: 'admin'
    hostname: 'mysql01'
    state: present
    load_to_runtime: False

# This example removes a server, saves the mysql server config to disk, and
# dynamically loads the mysql server config to runtime.  It uses credentials
# in a supplied config file to connect to the proxysql admin interface.

- proxysql_backend_servers:
    config_file: '~/proxysql.cnf'
    hostname: 'mysql02'
    state: absent
'''

RETURN = '''
stdout:
    description: The mysql host modified or removed from proxysql
    returned: On create/update will return the newly modified host, on delete
              it will return the deleted record.
    type: dict
    "sample": {
        "changed": true,
        "hostname": "192.168.52.1",
        "msg": "Added server to mysql_hosts",
        "server": {
            "comment": "",
            "compression": "0",
            "hostgroup_id": "1",
            "hostname": "192.168.52.1",
            "max_connections": "1000",
            "max_latency_ms": "0",
            "max_replication_lag": "0",
            "port": "3306",
            "status": "ONLINE",
            "use_ssl": "0",
            "weight": "1"
        },
        "state": "present"
    }
'''

