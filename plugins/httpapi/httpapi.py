# Copyright: (c) 2022, NVIDIA <nvidia.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
author: Nvidia NBU Team (@nvidia-nbu)
name: httpapi
short_description: httpapi plugin for NVIDIA's NVUE API
description:
- This connection plugin provides a connection to devices with NVIDIA's NVUE API over HTTP(S)-based
"""

import urllib

import json
import time

from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.ansible.netcommon.plugins.plugin_utils.httpapi_base import HttpApiBase


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)
        self.prefix = "/nvue_v1"
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, data, path, operation, **kwargs):
        if path == "revision/":
            if operation == "new":
                return self.create_revision()
            elif operation == "apply":
                return self.apply_config()
        if operation == "set":
            return self.set_operation(data, path, **kwargs)
        elif operation == "get":
            params = {"rev": "applied"}
            path = f"{self.prefix}/{path}?{urllib.parse.urlencode(params)}"
            return self.get_operation(path)

    def get_operation(self, path):
        response, response_data = self.connection.send(
            path, "", headers=self.headers, method="GET"
        )
        return handle_response(response, response_data)

    def set_operation(self, data, path, **kwargs):
        # If revid is not passed as part of the list of paramaters, create a new revision ID
        self.revisionID = kwargs.get("revid", self.create_revision())
        result = self.patch_revision(path, data)
        if kwargs.get("revid"):
            return result
        else:
            return self.apply_config(**kwargs)

    def create_revision(self):
        path = "/".join([self.prefix, "revision"])

        response, response_data = self.connection.send(
            path, dict(), method="POST", headers=self.headers
        )

        for k in handle_response(response, response_data):
            return k

    def patch_revision(self, path, data):
        params = {"rev": self.revisionID}
        path = f"{self.prefix}/?{urllib.parse.urlencode(params)}"

        response, response_data = self.connection.send(
            path, json.dumps(data), headers=self.headers, method="PATCH"
        )

        return handle_response(response, response_data)

    def apply_config(self, **kwargs):

        force = kwargs.get("force", False)
        wait = kwargs.get("wait", 0)
        path = "/".join([self.prefix, "revision", self.revisionID.replace("/", "%2F")])

        data = {"state": "apply"}
        if force:
            data["auto-prompt"] = {
                "ays": "ays_yes",
                "ignore_fail": "ignore_fail_yes",
            }

        response, response_data = self.connection.send(
            path,
            json.dumps(data),
            headers=self.headers,
            method="PATCH",
        )

        result = handle_response(response, response_data)

        while wait >= 0:
            result = self.get_operation(path)
            if result.get("state") == "applied":
                break
            time.sleep(1)
            wait -= 1

        return result


def handle_response(response, response_data):
    try:
        response_data = json.loads(response_data.read())
    except ValueError:
        response_data.seek(0)
        response_data = response_data.read()

    if isinstance(response, HTTPError):
        raise Exception(f"Connection error: {response}, data: {response_data}")

    return response_data
