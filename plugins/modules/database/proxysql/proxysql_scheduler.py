#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: proxysql_scheduler
author: "Ben Mildren (@bmildren)"
short_description: Adds or removes schedules from proxysql admin interface.
description:
   - The M(proxysql_scheduler) module adds or removes schedules using the
     proxysql admin interface.
options:
  active:
    description:
      - A schedule with I(active) set to C(False) will be tracked in the
        database, but will be never loaded in the in-memory data structures.
    default: True
    type: bool
  interval_ms:
    description:
      - How often (in millisecond) the job will be started. The minimum value
        for I(interval_ms) is 100 milliseconds.
    default: 10000
  filename:
    description:
      - Full path of the executable to be executed.
    required: True
  arg1:
    description:
      - Argument that can be passed to the job.
  arg2:
    description:
      - Argument that can be passed to the job.
  arg3:
    description:
      - Argument that can be passed to the job.
  arg4:
    description:
      - Argument that can be passed to the job.
  arg5:
    description:
      - Argument that can be passed to the job.
  comment:
    description:
      - Text field that can be used for any purposed defined by the user.
  state:
    description:
      - When C(present) - adds the schedule, when C(absent) - removes the
        schedule.
    choices: [ "present", "absent" ]
    default: present
  force_delete:
    description:
      - By default we avoid deleting more than one schedule in a single batch,
        however if you need this behaviour and you're not concerned about the
        schedules deleted, you can set I(force_delete) to C(True).
    default: False
    type: bool
extends_documentation_fragment:
- community.general.proxysql.managing_config
- community.general.proxysql.connectivity

'''

EXAMPLES = '''
---
# This example adds a schedule, it saves the scheduler config to disk, but
# avoids loading the scheduler config to runtime (this might be because
# several servers are being added and the user wants to push the config to
# runtime in a single batch using the M(proxysql_manage_config) module).  It
# uses supplied credentials to connect to the proxysql admin interface.

- proxysql_scheduler:
    login_user: 'admin'
    login_password: 'admin'
    interval_ms: 1000
    filename: "/opt/maintenance.py"
    state: present
    load_to_runtime: False

# This example removes a schedule, saves the scheduler config to disk, and
# dynamically loads the scheduler config to runtime.  It uses credentials
# in a supplied config file to connect to the proxysql admin interface.

- proxysql_scheduler:
    config_file: '~/proxysql.cnf'
    filename: "/opt/old_script.py"
    state: absent
'''

RETURN = '''
stdout:
    description: The schedule modified or removed from proxysql
    returned: On create/update will return the newly modified schedule, on
              delete it will return the deleted record.
    type: dict
    "sample": {
        "changed": true,
        "filename": "/opt/test.py",
        "msg": "Added schedule to scheduler",
        "schedules": [
            {
                "active": "1",
                "arg1": null,
                "arg2": null,
                "arg3": null,
                "arg4": null,
                "arg5": null,
                "comment": "",
                "filename": "/opt/test.py",
                "id": "1",
                "interval_ms": "10000"
            }
        ],
        "state": "present"
    }
'''

