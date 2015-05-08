# Copyright 2015 Rackspace US Inc.
# All Rights Reserved.
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
from neutron_lbaas.tests.tempest.v2.api import base

from tempest.common.utils import data_utils
from tempest import exceptions as ex
from tempest import test


class AclsTestJSON(base.BaseTestCase):

    """
    Tests the following operations in the Neutron-LBaaS API using the
    REST client for Acls:

        list acls
        create acl
        get acl
        update acl
        delete acl
    """

    @classmethod
    def resource_setup(cls):
        super(AclsTestJSON, cls).resource_setup()
        if not test.is_extension_enabled('lbaas', 'network'):
            msg = "lbaas extension not enabled."
            raise cls.skipException(msg)
        network_name = data_utils.rand_name('network-')
        cls.network = cls.create_network(network_name)
        cls.subnet = cls.create_subnet(cls.network)
        cls.load_balancer = cls._create_load_balancer(
            tenant_id=cls.subnet.get('tenant_id'),
            vip_subnet_id=cls.subnet.get('id'))
        cls.listener = cls._create_listener(
            loadbalancer_id=cls.load_balancer.get('id'),
            protocol='HTTP', protocol_port=80)

    @test.attr(type='smoke')
    def test_list_acl_empty(self):
        """Test get acl."""
        acl_list = self.acls_client.list_acls()
        self.assertEmpty(acl_list)

    @test.attr(type='smoke')
    def test_list_acls_one(self):
        """Test list one acl."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        acl_list = self.acls_client.list_acls()
        self.assertIn(acl, acl_list)
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='smoke')
    def test_list_acls_two(self):
        """Test list acls with two acls."""
        acl1 = self._create_acl(name='test_name',
                                listener_id=self.listener.get('id'),
                                action='url_end',
                                condition='/login',
                                operator='redirect location',
                                match='http://www.letv.com',
                                match_condition='test_name')

        acl2 = self._create_acl(name='test_name2',
                                listener_id=self.listener.get('id'),
                                action='url_end',
                                condition='/login',
                                operator='redirect location',
                                match='http://www.letv.com',
                                match_condition='test_name2')
        acl_list = self.acls_client.list_acls()
        self.assertEqual(2, len(acl_list))
        self.assertIn(acl1, acl_list)
        self.assertIn(acl2, acl_list)
        # cleanup test
        self._delete_acl(acl1.get('id'))
        self._delete_acl(acl2.get('id'))

    @test.attr(type='smoke')
    def test_get_acl(self):
        """Test get one acl."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        acl_test = self.acls_client.get_acl(acl.get('id'))
        self.assertEqual(acl, acl_test)
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='smoke')
    def test_create_acl(self):
        """Test create an acl for listener."""
        new_acl = self._create_acl(
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')
        acl = self.acls_client.get_acl(new_acl.get('id'))
        self.assertEqual(new_acl, acl)
        # cleanup test
        self._delete_acl(new_acl.get('id'))

    @test.attr(type='smoke')
    def test_create_acl_with_all_param(self):
        """Test create an acl with all param for listener."""
        new_acl = self._create_acl(
            name='test_name',
            description='this is a test acl.',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            acl_type='Redirect',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name',
            admin_state_up=True)
        acl = self.acls_client.get_acl(new_acl.get('id'))
        self.assertEqual(new_acl, acl)
        # cleanup test
        self._delete_acl(new_acl.get('id'))

    @test.attr(type='negative')
    def test_create_duplicated_acl_in_same_listener(self):
        """Test failed to create same acl name in same listener."""
        new_acl = self._create_acl(
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')
        acl = self.acls_client.get_acl(new_acl.get('id'))
        self.assertEqual(new_acl, acl)

        self.assertRaises(
            ex.Conflict, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

        # cleanup test
        self._delete_acl(new_acl.get('id'))

    @test.attr(type='smoke')
    def test_create_acl_missing_name(self):
        """Test create acl with a missing required field name."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='smoke')
    def test_create_acl_missing_listener_id(self):
        """Test create acl with a missing required field listener_id."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='smoke')
    def test_create_acl_missing_action(self):
        """Test create acl with a missing required field action."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='smoke')
    def test_create_acl_missing_condition(self):
        """Test create acl with a missing required field condition."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='smoke')
    def test_create_acl_missing_operator(self):
        """Test create acl with a missing required field operator."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='smoke')
    def test_create_acl_missing_match_condition(self):
        """Test create acl with a missing required field match_condition."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com')

    @test.attr(type='negative')
    def test_create_acl_invalid_name(self):
        """Test create acl with an invalid name."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='!@#$@#%!~',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_invalid_match_condition(self):
        """Test create acl with an invalid match_condition."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='#@~~!#@#asdf ')

    @test.attr(type='negative')
    def test_create_acl_invalid_listener_id(self):
        """Test create acl with an invalid listener_id."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id="xxx",
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_invalid_admin_state_up(self):
        """Test update listener with an invalid admin_state_up."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name',
            admin_state_up='abc123')

    @test.attr(type='negative')
    def test_create_acl_invalid_tenant_id(self):
        """Test create listener with an invalid tenant id."""
        self.assertRaises(
            ex.BadRequest, self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name',
            tenant_id="&^%123")

    @test.attr(type='negative')
    def test_create_acl_empty_listener_id(self):
        """Test create acl with an empty listener_id."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id='',
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_empty_name(self):
        """Test create acl with an empty name."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_empty_action(self):
        """Test create acl with an empty action."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_empty_condition(self):
        """Test create acl with an empty condition."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_empty_operator(self):
        """Test create acl with an empty operator."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='',
            match='http://www.letv.com',
            match_condition='test_name')

    @test.attr(type='negative')
    def test_create_acl_empty_match_condition(self):
        """Test create acl with an empty condition."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='')

    @test.attr(type='negative')
    def test_create_acl_empty_match(self):
        """Test create acl with an empty match."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='',
                               match_condition='test_name')
        acl_test = self.acls_client.get_acl(acl.get('id'))
        self.assertEqual(acl, acl_test)
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_create_acl_empty_admin_state_up(self):
        """Test update acl with an empty admin_state_up."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name',
            admin_state_up='')

    @test.attr(type='negative')
    def test_create_acl_empty_tenant_id(self):
        """Test create acl with an empty tenant id."""
        self.assertRaises(
            ex.BadRequest,
            self._create_acl,
            name='test_name',
            listener_id=self.listener.get('id'),
            action='url_end',
            condition='/login',
            operator='redirect location',
            match='http://www.letv.com',
            match_condition='test_name',
            tenant_id='')

    @test.attr(type='smoke')
    def test_create_acl_empty_description(self):
        """Test create acl with an empty description."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name',
                               description='')
        acl_test = self.acls_client.get_acl(acl.get('id'))
        self.assertEqual(acl, acl_test)
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_create_acl_incorrect_attribute(self):
        """Test create a acl with an extra, incorrect field."""
        self.assertRaises(ex.BadRequest,
                          self._create_acl,
                          name='test_name',
                          listener_id=self.listener.get('id'),
                          action='url_end',
                          condition='/login',
                          operator='redirect location',
                          match='http://www.letv.com',
                          match_condition='test_name',
                          incorrect_attribute="incorrect_attribute")

    @test.attr(type='smoke')
    def test_update_acl(self):
        """Test update acl."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        match = "http://www.google.com"
        new_acl = self._update_acl(
            acl.get('id'), match=match)
        self.assertEqual(match, new_acl.get('match'))
        # cleanup test
        self._delete_acl(new_acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_invalid_tenant_id(self):
        """Test update acl with an invalid tenant id."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          tenant_id="&^%123")
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_invalid_admin_state_up(self):
        """Test update a acl with an invalid admin_state_up."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          admin_state_up="$23")
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_invalid_name(self):
        """Test update a acl with an invalid name."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          name="!@#$zzz")
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_invalid_match_condition(self):
        """Test update a acl with an invalid match_condition."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          match_condition="####$#$asfasd@#$zzz")
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_listener_id_failed(self):
        """Test failed to update an acl listener_id."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          listener_id='123')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_tenant_id(self):
        """Test failed to update an acl tenant_id."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          tenant_id='123')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_name(self):
        """Test update acl with an empty name."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          name='')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_action(self):
        """Test update acl with an empty action."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          action='')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_condition(self):
        """Test update acl with an empty condition."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          condition='')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_operator(self):
        """Test update acl with an empty operator."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          operator='')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_match_condition(self):
        """Test update acl with an empty condition."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          match_condition='')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='smoke')
    def test_update_acl_empty_match(self):
        """Test update acl with an empty match."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        match = ''
        new_acl = self._update_acl(
            acl.get('id'), match=match)
        self.assertEqual(match, new_acl.get('match'))
        # cleanup test
        self._delete_acl(new_acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_empty_admin_state_up(self):
        """Test update acl with an empty admin_state_up."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          admin_state_up='')
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='smoke')
    def test_update_acl_empty_description(self):
        """Test update acl with an empty description."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name',
                               description='123456')
        description = ''
        new_acl = self._update_acl(
            acl.get('id'), description=description)
        self.assertEqual(description, new_acl.get('description'))
        # cleanup test
        self._delete_acl(new_acl.get('id'))

    @test.attr(type='negative')
    def test_update_acl_extra_attribute(self):
        """Test update an acl with an extra, incorrect field."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self.assertRaises(ex.BadRequest,
                          self._update_acl,
                          acl.get('id'),
                          incorrect_attribute="incorrect_attribute")
        # cleanup test
        self._delete_acl(acl.get('id'))

    @test.attr(type='smoke')
    def test_delete_acl(self):
        """Test delete acl."""
        acl = self._create_acl(name='test_name',
                               listener_id=self.listener.get('id'),
                               action='url_end',
                               condition='/login',
                               operator='redirect location',
                               match='http://www.letv.com',
                               match_condition='test_name')
        self._delete_acl(acl.get('id'))
        self.assertRaises(ex.NotFound,
                          self.acls_client.get_acl,
                          acl.get('id'))
