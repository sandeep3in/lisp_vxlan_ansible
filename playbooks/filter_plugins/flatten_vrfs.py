class FilterModule(object):
    ''' Nested dict filter '''

    def filters(self):
        return {
            'flatten_vrfs': self.flatten_vrfs
        }

    def flatten_vrfs(self, vrfs):
        flat_vrfs = {}
        for device_vrf in vrfs:
            for vrf in device_vrf:
                if flat_vrfs.get(vrf["vrf"]) is None:
                    flat_vrfs[vrf["vrf"]] = vrf["handoffs"]
                else:
                    for item in vrf["handoffs"]:
                        flat_vrfs[vrf["vrf"]].append(item)
        return flat_vrfs
