#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: router

short_description: This is the Cumulus Linux router module

version_added: "1.0.0"

description: This is a Cumulus Linux module to interact with the router object.

options:
    filters:
        description: Filters used while fetching information about router
        type: dict
        suboptions:
            rev:
                description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration
                             branches, such as startup and applied. This could be a branch name, tag name or specific commit.
                required: false
                type: str
                default: applied
            omit:
                description: Drop any JSON properties matched by an omit pattern from the response.
                required: false
                type: list
                elements: str
            include:
                description: Only include JSON properties matched by an include pattern in the response.
                required: false
                type: list
                elements: str
    data:
        description: Provided configuration
        type: dict
        suboptions:
            bgp:
                description: BGP global configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
                    autonomous_system:
                        description: ASN for all VRFs, if a single AS is in use. If "none", then ASN must be set for every VRF. This is the default.
                        required: false
                        type: int
                    graceful_restart:
                        description: BGP Graceful restart global configuration.
                        type: dict
                        required: false
                        suboptions:
                            mode:
                                description: Role of router during graceful restart.
                                             helper-only, router is in helper role.
                                             full, router is in both helper and restarter role.
                                             off, GR is disabled for the router
                                type: str
                                required: false
                                choices:
                                    - 'full'
                                    - 'off'
                                    - 'helper-only'
                    router_id:
                        description: BGP router-id for all VRFs, if a common one is used. If "none", then router-id must be set for every VRF.
                                     This is the default.
                        required: false
                        type: str
            ospf:
                description: OSPF global configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
                    timers:
                        description: Timers.
                        required: false
                        type: dict
                        suboptions:
                            spf:
                                description: SPF timers.
                                required: false
                                type: dict
                                suboptions:
                                    delay:
                                        description: Delay (msec) from first change received till SPF calculation.
                                        required: false
                                        type: int
                                    holdtime:
                                        description: Initial hold time (msec) between consecutive SPF calculations.
                                        required: false
                                        type: int
                                    max_holdtime:
                                        description: Maximum hold time (msec) between consecutive SPF calculations.
                                        required: false
                                        type: int
            policy:
                description: A router policy
                type: dict
                required: false
                suboptions:
                    prefix_list:
                        description: prefix lists to be used in routing policies
                        type: list
                        required: false
                        elements: dict
                        suboptions:
                            id:
                                description: id of the prefix list
                                type: str
                                required: false
                            type:
                                description: type of prefixes
                                type: str
                                choices:
                                    - ipv4
                                    - ipv6
                                required: false
                            rule:
                                description: rules for the prefix list
                                type: list
                                required: false
                                elements: dict
                                suboptions:
                                    id:
                                        description: numerical id for the rule (rules are applied in order)
                                        type: int
                                        required: false
                                    match:
                                        description: prefix for the rule
                                        type: list
                                        required: false
                                        elements: dict
                                        suboptions:
                                            id:
                                                description: ipv4 or ipv6 prefix
                                                type: str
                                                required: false
                                            max_prefix_len:
                                                description: prefix length to be used for encapsulating smaller prefixes in rules
                                                type: int
                                                required: false
                                            min_prefix_len:
                                                description: prefix length to be used for encapsulating larger prefixes in rules
                                                type: int
                                                required: false
                                    action:
                                        description: action to take on the rule
                                        type: str
                                        choices:
                                            - permit
                                            - deny
                                        required: false
                    route_map:
                        description: route map to be used for filtering routes
                        type: list
                        required: false
                        elements: dict
                        suboptions:
                            id:
                                description: route-map id
                                type: str
                                required: false
                            rule:
                                description: rules to apply
                                type: list
                                required: false
                                elements: dict
                                suboptions:
                                    id:
                                        description: number of the rule (rules are applied in order)
                                        type: int
                                        required: false
                                    action:
                                        description: action to take
                                        type: list
                                        required: false
                                        elements: dict
                                        suboptions:
                                            id:
                                                description: Route Map set
                                                type: str
                                                required: false
                                                choices:
                                                    - deny
                                                    - permit
                                    match:
                                        description: what to match
                                        type: dict
                                        required: false
                                        suboptions:
                                            type:
                                                description: match type
                                                type: str
                                                required: false
                                                choices:
                                                    - ipv4
                                                    - ipv6
                                            ip_prefix_list:
                                                description: ip prefix list to use
                                                type: str
                                                required: false
            vrr:
                description: VRR global configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
            pim:
                description: PIM global configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
                    timers:
                        description: Timers.
                        required: false
                        type: dict
                        suboptions:
                            keep_alive:
                                description: Timeout value for S,G stream, in seconds.
                                required: false
                                type: int
            adaptive_routing:
                description: Adaptive routing global configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
                    profile:
                        description: Adaptive routing global profile configuration.
                        required: false
                        type: str
                        choices:
                            - 'profile-1'
                            - 'profile-2'
                            - 'profile-custom'
                    link_utilization_threshold:
                        description: Turn on or off Link utilization threshold on all interfaces.
                                     This feature is off by default.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
    revid:
        description: Revision ID to query/to apply config to.
        required: false
        type: str
    state:
        description: Defines the action to be taken.
        required: true
        type: str
        choices:
            - gathered
            - deleted
            - merged
    force:
        description: When true, replies "yes" to NVUE prompts.
        required: false
        default: false
        type: bool
    wait:
        description: How long to poll for "merged/deleted" operation results.
        required: false
        default: 0
        type: int

author:
    - Nvidia NBU Team (@nvidia-nbu)
    - Krishna Vasudevan (@krisvasudevan)
'''

EXAMPLES = r'''
# Pass in a message
- name: Display all the router config in the environment
  nvidia.nvue.router:
    state: gathered
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types


def main():
    # define supported filters for the endpoint
    # since router object doesn't support querying the operational state, we will default to applied state
    filter_spec = dict(
        rev=dict(type='str', required=False, default='applied'),
        omit=dict(type='list', required=False, elements='str'),
        include=dict(type='list', required=False, elements='str')
    )

    # define the router spec - used for creation/modification
    router_spec = dict(
        bgp=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off']),
            autonomous_system=dict(type='int', required=False),
            graceful_restart=dict(type='dict', required=False, options=dict(
                mode=dict(type='str', required=False, choices=['full', 'off', 'helper-only'])
            )),
            router_id=dict(type='str', required=False)
        )),
        ospf=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off']),
            timers=dict(type='dict', required=False, options=dict(
                spf=dict(type='dict', required=False, options=dict(
                    delay=dict(type='int', required=False),
                    holdtime=dict(type='int', required=False),
                    max_holdtime=dict(type='int', required=False)
                )))
            ))),
        vrr=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off'])
        )),
        pim=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off']),
            timers=dict(type='dict', required=False, options=dict(
                keep_alive=dict(type='int', required=False)
            ))
        )),
        adaptive_routing=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off']),
            profile=dict(type='str', required=False, choices=['profile-1', 'profile-2', 'profile-custom']),
            link_utilization_threshold=dict(type='str', required=False, choices=['on', 'off'])
        )),
        policy=dict(type='dict', required=False, options=dict(
            prefix_list=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                type=dict(type='str', required=False, choices=['ipv4', 'ipv6']),
                rule=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='int', required=False),
                    match=dict(type='list', required=False, elements='dict', options=dict(
                        id=dict(type='str', required=False),
                        max_prefix_len=dict(type='int', required=False),
                        min_prefix_len=dict(type='int', required=False)
                    )),
                    action=dict(type='str', required=False, choices=['permit', 'deny'])
                ))
            )),
            route_map=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                rule=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='int', required=False),
                    action=dict(type='list', required=False, elements='dict', options=dict(
                        id=dict(type='str', required=False, choices=['permit', 'deny'])
                    )),
                    match=dict(type='dict', required=False, options=dict(
                        type=dict(type='str', required=False, choices=['ipv4', 'ipv6']),
                        ip_prefix_list=dict(type='str', required=False))
                    )
                ))
            ))
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=["gathered", "deleted", "merged"]),
        revid=dict(type='str', required=False),
        data=dict(type='dict', required=False, options=router_spec),
        filters=dict(type='dict', required=False, options=filter_spec)
    )

    required_if = [
        ["state", "merged", ["data"]],
    ]
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        required_if=required_if,
        supports_check_mode=True
    )

    path = "router"
    if module.params["state"] == "gathered":
        operation = "get"
    else:
        operation = "set"
    data = module.params["data"]
    force = module.params["force"]
    wait = module.params["wait"]
    revid = module.params["revid"]

    if isinstance(data, string_types):
        data = json.loads(data)

    warnings = list()
    result = {"changed": False, "warnings": warnings}

    running = None
    commit = not module.check_mode

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    connection = Connection(module._socket_path)
    response = connection.send_request(data, path, operation, force=force, wait=wait, revid=revid)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()
