# Copyright 2015 Rackspace US Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import urllib

from oslo_serialization import jsonutils
from tempest.common import service_client


class AclsClientJSON(service_client.ServiceClient):
    """
    Tests Acls API
    """

    def list_acls(self, params=None):
        """List all acls."""
        url = 'v2.0/lbaas/acls'
        if params:
            url = '{0}?{1}'.format(url, urllib.urlencode(params))
        resp, body = self.get(url)
        body = jsonutils.loads(body)
        self.expected_success(200, resp.status)
        return service_client.ResponseBodyList(resp, body['acls'])

    def get_acl(self, acl_id, params=None):
        """Get acl details."""
        url = 'v2.0/lbaas/acls/{0}'.format(acl_id)
        if params:
            url = '{0}?{1}'.format(url, urllib.urlencode(params))
        resp, body = self.get(url)
        body = jsonutils.loads(body)
        self.expected_success(200, resp.status)
        return service_client.ResponseBody(resp, body['acl'])

    def create_acl(self, **kwargs):
        """Create a acl build."""
        post_body = jsonutils.dumps({'acl': kwargs})
        resp, body = self.post('v2.0/lbaas/acls', post_body)
        body = jsonutils.loads(body)
        self.expected_success(201, resp.status)
        return service_client.ResponseBody(resp, body['acl'])

    def update_acl(self, acl_id, **kwargs):
        """Update an acl build."""
        put_body = jsonutils.dumps({'acl': kwargs})
        resp, body = self.put('v2.0/lbaas/acls/{0}'
                              .format(acl_id), put_body)
        body = jsonutils.loads(body)
        self.expected_success(200, resp.status)
        return service_client.ResponseBody(resp, body['acl'])

    def delete_acl(self, acl_id):
        """Delete an existing acl build."""
        resp, body = self.delete("v2.0/lbaas/acls/{0}"
                                 .format(acl_id))
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)
