#!/usr/bin/python
#
# Copyright (c) 2020 Sakar Mehra (@sakar97), Praveen Ghuge (@praveenghuge), Karl Dasan (@ikarldasan)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '''
---
module: azure_expressroute_info
short_description: Get Azure Express Route facts
description:
    - Get facts of Azure Express Route.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: True
    name:
        description:
            - The name of the express route.
        required: True
extends_documentation_fragment:
- azure.azcollection.azure
author:
    - Praveen Ghuge (@praveenghuge)
    - Karl Dasan (@ikarldasan)
    - Sakar Mehra (@sakar97)
'''
EXAMPLES = '''
  - name: Get facts of specific expressroute
    community.azure.azure_rm_expressroute_info:
      resource_group: myResourceGroup
      name: myExpressRoute
'''
RETURN = '''
'''
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from msrestazure.azure_exceptions import CloudError
    from azure.mgmt.network import NetworkManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass
class AzureExpressRouteInfo(AzureRMModuleBase):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            ),
            express_route_name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.name = None
        self.express_route_name = None
        print("\n***************************\n")
        print("module_arg_spec: ", self.module_arg_spec)
        print("\n***************************\n")
        super(AzureExpressRouteInfo, self).__init__(self.module_arg_spec, supports_tags=False)
    def exec_module(self, **kwargs):
        is_old_facts = self.module._name == 'azure_rm_expressroute_info'
        if is_old_facts:
            self.module.deprecate("The 'azure_rm_expressroute_info' module has been renamed to 'azure_rm_expressroute_info'",
                                  version='3.0.0', collection_name='community.azure')  # was 2.13
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        if self.name is not None:
            result = self.get()
        # self.results = None
        return self.results
    def get(self):
        response = None
        results = []
        try:
            response = self.network_client.express_route_circuits.get(resource_group_name=self.resource_group,
                                                       circuit_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.fail('Could not get facts for Subnet.')
        if response is not None:
            print("\n=============================================\n")
            print("response: ", response)
            print("\n=============================================\n")
            results.append(self.format_response(response))
            # results = self.format_response(response)
        print("\n^^^^^^^^results: ", results)
        return results
    def format_response(self, item):
        print("-----------INSIDE FORMAT RESPONSE---------------")
        d = item.as_dict()
        print("d: ", d)
        print("type(d): ", type(d))
        d = {
            'additional_properties': d.get('additional_properties', {}),
            'id': d.get('id', None),
            'name': d.get('name', None),
            'type': d.get('type', None),
            'location': d.get('location', '').replace(' ', '').lower(),
            'tags': d.get('tags', None),
            # 'sku': <azure.mgmt.network.v2019_06_01.models._models_py3.ExpressRouteCircuitSku object at 0x7feb0dd91c40>,
            # 'sku': d['sku']['tier'].lower(),
            'allow_classic_operations': d.get('allow_classic_operations', None),
            'circuit_provisioning_state': d.get('circuit_provisioning_state', None),
            'service_provider_provisioning_state': d.get('service_provider_provisioning_state', None),
            'authorizations': d.get('authorizations', []),
            'peerings': d.get('peerings', []),
            'service_key': d.get('service_key', None),
            'service_provider_notes': d.get('service_provider_notes', None),
            # 'service_provider_properties': <azure.mgmt.network.v2019_06_01.models._models_py3.ExpressRouteCircuitServiceProviderProperties object at 0x7feb0dd91c70>,
            'express_route_port': d.get('express_route_port', None),
            'bandwidth_in_gbps': d.get('bandwidth_in_gbps', None),
            'stag': d.get('stag', None),
            'provisioning_state': d.get('provisioning_state', None),
            'gateway_manager_etag': d.get('gateway_manager_etag', ''),
            'global_reach_enabled': d.get('global_reach_enabled', '')
        }
        print("d AFTER:", d)
        return d
def main():
    AzureExpressRouteInfo()
if __name__ == '__main__':
    main() 
