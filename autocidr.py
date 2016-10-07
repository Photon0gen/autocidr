#!/usr/bin/python
import sys
sys.path.append('./lib/')
import netaddr
import pprint
import math

'''
To assign CIDRs to the Subnets we will:
    1. Confirm the sum of minimum addresses fits inside the VPC CIDR address space
    2. For each Subnet
        3. Calculate the next available address
        4. Calculate the Netmask required to fit the minimum address space of the subnet
        5. Calculate the CIDR
'''



def getSmallestPrefix(min_addresses):
     return 32 - int(math.ceil(math.log(min_addresses,2)))  # log2, then round up


def getCIDRs(vpc_cidr, subnets):
    '''
vpc_cidr = "10.8.8.0/24"
subnets = {
    'Proxy': {},
    'Collector': { 'MinSize': 100 },
    'Bastion': {},
    'Application': { 'MinSize': 30 }
}
'''
    MIN_ADDRESS_SPACE=16
    sorted_subnets = sorted(subnets.iteritems(), key=lambda s: s[1].get('MinSize',MIN_ADDRESS_SPACE), reverse=True)

    vpc_network = netaddr.IPNetwork(vpc_cidr)
    # get a list of all the addresses in the VPC
    available_addresses=list(vpc_network)
    address_index=0
    for subnet in sorted_subnets:
        next_address=available_addresses[address_index]
        # figure out how big of a prefix we need for this subnet
        min_addr=subnet[1].get('MinSize', MIN_ADDRESS_SPACE)
        snet_first_address=next_address
        snet_prefix = getSmallestPrefix(min_addr)
        # create the cidr from the next available address and the prefix
        snet_cidr = netaddr.IPNetwork(str(next_address)+"/"+str(snet_prefix))
        subnets[subnet[0]]['cidr'] = str(snet_cidr.cidr)
        # get the last address in the subnet
        cidr_last=list(snet_cidr)[-1]
        cidr_last_index = available_addresses.index(cidr_last)
        address_index = cidr_last_index + 1

    return subnets
