#!/usr/bin/python

# Copyright: (c) 2022, NVIDIA <nvidia.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
author: Nvidia NBU Team (@nvidia-nbu)
short_description: Use httpapi to run command on NVUE devices
description:
- This connection plugin provides a connection to NVUE over an HTTP(S)-based
  api.
module: api
options:
    operation:
        description: Type of API operation
        required: false
        choices: ["get", "set"]
        default: "get"
        type: str
    force:
        description: When true, replies "yes" to NVUE prompts.
        required: false
        default: false
        type: bool
    wait:
        description: How long to poll for "set" operation results.
        required: false
        default: 0
        type: int
    path:
        description: API path that will be appended to "/nvue_v1"
        required: false
        default: /
        type: str
    filled:
        description: If true, fill in attributes with default values, providing a complete set of attributes.
                     If false, return only the attributes that differ from the defaults.
        required: false
        default: true
        type: bool
    data:
        description: Structured data used with "set" operations.
        default: {}
        required: false
        type: dict
    revid:
        description: Revision ID to query/to apply config to
        required: false
        type: str
"""

EXAMPLES = r"""
# In-line data definition
- name: Example of interpolating variables
  nvidia.nvue.api:
    operation: set
    force: yes
    wait: 15
    data:
      system:
        message:
          "pre-login": "{{ MSG }}"
  vars:
    MSG: WARNING

# Using inventory variables
- name: Example of using host variables
  nvidia.nvue.api:
    operation: set
    force: yes
    wait: 15
    data: "{{ dict(host_variables) }}"
"""

RETURN = r"""
# These are examples of possible return values,
# and in general should use other names for return values.
changed:
  description: whether a configuration was changed
  returned: always
  type: bool
  sample: true
message:
    description: whether a change was applied
    type: dict
    returned: always
    sample:
        "state": "applied"
"""

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types


def main():
    """entry point for module execution"""
    module_args = {
        "operation": {
            "type": "str",
            "choices": ["get", "set"],
            "default": "get",
        },
        "force": {"type": "bool", "required": False, "default": False},
        "wait": {"type": "int", "required": False, "default": 0},
        "path": {"type": "str", "required": False, "default": "/"},
        "filled": {"type": "bool", "required": False, "default": True},
        "data": {"type": "dict", "required": False, "default": {}},
        "revid": {"type": "str", "required": False}
    }

    required_if = [
        ["operation", "set", ["data"]],
    ]

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=required_if,
        supports_check_mode=True,
    )

    path = module.params["path"]
    data = module.params["data"]
    operation = module.params["operation"]
    force = module.params["force"]
    wait = module.params["wait"]
    revid = module.params["revid"]
    filled = module.params["filled"]

    if isinstance(data, string_types):
        data = json.loads(data)

    warnings = list()
    result = {"changed": False, "warnings": warnings}

    running = None
    commit = not module.check_mode

    connection = Connection(module._socket_path)
    response = connection.send_request(data, path, operation, force=force, wait=wait, revid=revid, filled=filled)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)


if __name__ == "__main__":
    main()
