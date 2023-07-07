# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
from rich.pretty import pprint
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

      # First of all populate options,
      # this will already take into account env vars and ini config
      self.set_options(var_options=variables, direct=kwargs)

      ret = []
      for vrf in variables["vrfs"]:
         for handoff in vrf["handoffs"]:
             if handoff["handoff_vlan"] == kwargs["vlan"]:
                 ret.append(handoff["handoff_interface"])


      return ret
