#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: proxysql_query_rules
author: "Ben Mildren (@bmildren)"
short_description: Modifies query rules using the proxysql admin interface.
description:
   - The M(proxysql_query_rules) module modifies query rules using the
     proxysql admin interface.
options:
  rule_id:
    description:
      - The unique id of the rule. Rules are processed in rule_id order.
  active:
    description:
      - A rule with I(active) set to C(False) will be tracked in the database,
        but will be never loaded in the in-memory data structures.
    type: bool
  username:
    description:
      - Filtering criteria matching username.  If I(username) is non-NULL, a
        query will match only if the connection is made with the correct
        username.
  schemaname:
    description:
      - Filtering criteria matching schemaname. If I(schemaname) is non-NULL, a
        query will match only if the connection uses schemaname as its default
        schema.
  flagIN:
    description:
      - Used in combination with I(flagOUT) and I(apply) to create chains of
        rules.
  client_addr:
    description:
      - Match traffic from a specific source.
  proxy_addr:
    description:
      - Match incoming traffic on a specific local IP.
  proxy_port:
    description:
      - Match incoming traffic on a specific local port.
  digest:
    description:
      - Match queries with a specific digest, as returned by
        stats_mysql_query_digest.digest.
  match_digest:
    description:
      - Regular expression that matches the query digest. The dialect of
        regular expressions used is that of re2 - https://github.com/google/re2
  match_pattern:
    description:
      - Regular expression that matches the query text. The dialect of regular
        expressions used is that of re2 - https://github.com/google/re2
  negate_match_pattern:
    description:
      - If I(negate_match_pattern) is set to C(True), only queries not matching
        the query text will be considered as a match. This acts as a NOT
        operator in front of the regular expression matching against
        match_pattern.
    type: bool
  flagOUT:
    description:
      - Used in combination with I(flagIN) and apply to create chains of rules.
        When set, I(flagOUT) signifies the I(flagIN) to be used in the next
        chain of rules.
  replace_pattern:
    description:
      - This is the pattern with which to replace the matched pattern. Note
        that this is optional, and when omitted, the query processor will only
        cache, route, or set other parameters without rewriting.
  destination_hostgroup:
    description:
      - Route matched queries to this hostgroup. This happens unless there is a
        started transaction and the logged in user has
        I(transaction_persistent) set to C(True) (see M(proxysql_mysql_users)).
  cache_ttl:
    description:
      - The number of milliseconds for which to cache the result of the query.
        Note in ProxySQL 1.1 I(cache_ttl) was in seconds.
  timeout:
    description:
      - The maximum timeout in milliseconds with which the matched or rewritten
        query should be executed. If a query run for longer than the specific
        threshold, the query is automatically killed. If timeout is not
        specified, the global variable mysql-default_query_timeout applies.
  retries:
    description:
      - The maximum number of times a query needs to be re-executed in case of
        detected failure during the execution of the query. If retries is not
        specified, the global variable mysql-query_retries_on_failure applies.
  delay:
    description:
      - Number of milliseconds to delay the execution of the query. This is
        essentially a throttling mechanism and QoS, and allows a way to give
        priority to queries over others. This value is added to the
        mysql-default_query_delay global variable that applies to all queries.
  mirror_flagOUT:
    description:
      - Enables query mirroring. If set I(mirror_flagOUT) can be used to
        evaluates the mirrored query against the specified chain of rules.
  mirror_hostgroup:
    description:
      - Enables query mirroring. If set I(mirror_hostgroup) can be used to
        mirror queries to the same or different hostgroup.
  error_msg:
    description:
      - Query will be blocked, and the specified error_msg will be returned to
        the client.
  log:
    description:
      - Query will be logged.
    type: bool
  apply:
    description:
      - Used in combination with I(flagIN) and I(flagOUT) to create chains of
        rules. Setting apply to True signifies the last rule to be applied.
    type: bool
  comment:
    description:
      - Free form text field, usable for a descriptive comment of the query
        rule.
  state:
    description:
      - When C(present) - adds the rule, when C(absent) - removes the rule.
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
# This example adds a rule to redirect queries from a specific user to another
# hostgroup, it saves the mysql query rule config to disk, but avoids loading
# the mysql query config config to runtime (this might be because several
# rules are being added and the user wants to push the config to runtime in a
# single batch using the M(proxysql_manage_config) module). It uses supplied
# credentials to connect to the proxysql admin interface.

- proxysql_query_rules:
    login_user: admin
    login_password: admin
    username: 'guest_ro'
    match_pattern: "^SELECT.*"
    destination_hostgroup: 1
    active: 1
    retries: 3
    state: present
    load_to_runtime: False

# This example removes all rules that use the username 'guest_ro', saves the
# mysql query rule config to disk, and dynamically loads the mysql query rule
# config to runtime.  It uses credentials in a supplied config file to connect
# to the proxysql admin interface.

- proxysql_query_rules:
    config_file: '~/proxysql.cnf'
    username: 'guest_ro'
    state: absent
    force_delete: true
'''

RETURN = '''
stdout:
    description: The mysql user modified or removed from proxysql
    returned: On create/update will return the newly modified rule, in all
              other cases will return a list of rules that match the supplied
              criteria.
    type: dict
    "sample": {
        "changed": true,
        "msg": "Added rule to mysql_query_rules",
        "rules": [
            {
                "active": "0",
                "apply": "0",
                "cache_ttl": null,
                "client_addr": null,
                "comment": null,
                "delay": null,
                "destination_hostgroup": 1,
                "digest": null,
                "error_msg": null,
                "flagIN": "0",
                "flagOUT": null,
                "log": null,
                "match_digest": null,
                "match_pattern": null,
                "mirror_flagOUT": null,
                "mirror_hostgroup": null,
                "negate_match_pattern": "0",
                "proxy_addr": null,
                "proxy_port": null,
                "reconnect": null,
                "replace_pattern": null,
                "retries": null,
                "rule_id": "1",
                "schemaname": null,
                "timeout": null,
                "username": "guest_ro"
            }
        ],
        "state": "present"
    }
'''

