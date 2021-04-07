#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
__metaclass__ = type
DOCUMENTATION = '''
---
module: azure_rm_expressroute
version_added: "0.1.2"
short_description: Manage Express Route Circuits
description:
    - Create, update and delete instance of Express Route.
options:
    resource_groups:
        description:
            - Name of the resource group to which the resource belongs.
    name:
        description:
            - Unique name of the app service plan to create or update.
        required: True
    location:
        description:
            - Resource location. If not set, location from the resource group will be used as default.
    provider:
        description:
            - The service Provider Name
    peering_location:
        description:
            - The peering location
    bandwith:
        description:
            - The BandwidthInMbps
    sku:
        description:
            - The name of the SKU.
            - Please see (https://azure.microsoft.com/en-in/pricing/details/expressroute/)
        default: Standard
        choices:
            - Standard
            - Premium
    billing model:
        description:
            - The tier of the SKU
        default: Metered
        choices:
            - Metered
            - Unlimited
    state:
      description:
          - Assert the state of the express route.
          - Use C(present) to create or update an express route and C(absent) to delete it.
      default: present
      choices:
          - absent
          - present
extends_documentation_fragment:
- azure.azcollection.azure
author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldasan)
    - Sakar Mehra (@sakar97)
'''
EXAMPLES = '''
    - name: Create a express route
      azure_rm_expressroute:
        resource_group: myResourceGroup
        name: myAppPlan
        location: eastus
        provider: Airtel
        peering_location: Chennai2
        bandwith: 10
        sku: Standard
        billing_model: Metered
'''
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureExpressRoute(AzureRMModuleBase):
    def __init__(self):
        print("AzureExpressRoute INIT CALLED")
        # define user inputs from playbook
        self.service_provider_properties_spec = dict(
            service_provider_name=dict(type='str'),
            peering_location=dict(type='str'),
            bandwidth_in_mbps=dict(type='str')
        )

        self.sku_spec = dict(
            name=dict(type='str', required=True),
            tier=dict(type='str', choices=['Standard', 'Premium', 'Basic', 'Local'], required=True),
            family=dict(type='str', choices=['UnlimitedData', 'MeteredData'], required=True)
        )

        self.authorizations_spec = dict(
            name=dict(type='str', required=True)
        )

        self.module_arg_spec = dict(
            resource_group=dict(type='str', required=True),
            name=dict(type='str', required=True),
            location=dict(type='str', required=True),
            sku=dict(type='dict', options=self.sku_spec, required=True),
            tags=dict(type='dict'),
            allow_classic_operations=dict(type='bool'),
            authorizations=dict(type='list', options=self.authorizations_spec),
            state=dict(choices=['present', 'absent'],
                       default='present', type='str'),
            service_provider_properties=dict(type='dict', options=self.service_provider_properties_spec),
            global_reach_enabled=dict(type='bool')
        )

        self.resource_group = None
        self.name = None
        self.location = None
        self.allow_classic_operations = None
        self.authorizations = None
        self.service_provider_properties = None
        self. global_reach_enabled = None
        self.sku = None
        self.tags = None
        self.state = None
        self.results = dict(
            changed=False,
            state=dict()
        )
        super(AzureExpressRoute, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=False,
                                                facts_module=True,
                                                supports_tags=False)

    def exec_module(self, **kwargs):
        results = dict()

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        if self.state == "absent":
            results['type'] = "123"
            self.delete_expressroute()
            self.results['state']['status'] = 'Deleted'

        self.log("CALLING CREATE OR UPDATE")
        self.create_or_update_express_route(self.module.params)
        return self.results

    def create_or_update_express_route(self, params):
        '''
        Create or update Express route.
        :return: create or update Express route instance state dictionary
        '''
        self.log("create or update Express Route {0}".format(self.name))
        try:
            response = self.network_client.express_route_circuits.create_or_update(
                resource_group_name=params.get("resource_group"),
                circuit_name=params.get("name"),
                parameters=params)

            self.log("Response : {0}".format(response))
        except CloudError as ex:
            self.fail("Failed to create express route {0} in resource group {1}: {2}".format(
                self.name, self.resource_group, str(ex)))
        return True

    def delete_expressroute(self):
        '''
        Deletes specified express route circuit
        :return True
        '''
        self.log("Deleting the express route {0}".format(self.name))
        try:
            response = self.network_client.express_route_circuits.delete(resource_group_name=self.resource_group,
                                                                         name=self.name)
        except CloudError as e:
            self.log('Error attempting to delete express route.')
            self.fail(
                "Error deleting the express route : {0}".format(str(e)))
        return True


def main():
    AzureExpressRoute()


if __name__ == '__main__':
    main()
