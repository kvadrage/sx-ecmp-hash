#!/usr/bin/python
'''
This script is setting custom ECMP Hash fields for Mellanox Switches.
First it tries to read and apply ECMP Hash configuration from file 
(/etc/sx_ecmp_hash.conf).
Otherwise it applies the following default config:
    SX_ROUTER_ECMP_HASH_SRC_IP
    SX_ROUTER_ECMP_HASH_DST_IP
    SX_ROUTER_ECMP_HASH_TCP_UDP
    SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT
    SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT
    SX_ROUTER_ECMP_HASH_SMAC
    SX_ROUTER_ECMP_HASH_DMAC
    SX_ROUTER_ECMP_HASH_ETH_TYPE
    SX_ROUTER_ECMP_HASH_VID

'''

import sys, errno
sys.path.append('/lib/python2.7/dist-packages/python_sdk_api/')
sys.path.append('/lib/python2.7/site-packages/python_sdk_api/')
sys.path.append('/usr/lib/python2.7/dist-packages/python_sdk_api/')
sys.path.append('/usr/lib/python2.7/site-packages/python_sdk_api/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/python_sdk_api/')
sys.path.append('/usr/local/lib/python2.7/site-packages/python_sdk_api/')
from sx_api import *

ECMP_HASH_CFG = "/etc/sx_ecmp_hash.conf"
DEFAULT_ECMP_HASH = SX_ROUTER_ECMP_HASH_SRC_IP | \
                    SX_ROUTER_ECMP_HASH_DST_IP | \
                    SX_ROUTER_ECMP_HASH_TCP_UDP | \
                    SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT | \
                    SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT | \
                    SX_ROUTER_ECMP_HASH_SMAC | \
                    SX_ROUTER_ECMP_HASH_DMAC | \
                    SX_ROUTER_ECMP_HASH_ETH_TYPE | \
                    SX_ROUTER_ECMP_HASH_VID

ECMP_HASH_BITS = (
    ("SX_ROUTER_ECMP_HASH_SRC_IP", SX_ROUTER_ECMP_HASH_SRC_IP ),
    ("SX_ROUTER_ECMP_HASH_DST_IP", SX_ROUTER_ECMP_HASH_DST_IP),
    ("SX_ROUTER_ECMP_HASH_TCLASS", SX_ROUTER_ECMP_HASH_TCLASS),
    ("SX_ROUTER_ECMP_HASH_FLOW_LABEL", SX_ROUTER_ECMP_HASH_FLOW_LABEL),
    ("SX_ROUTER_ECMP_HASH_TCP_UDP", SX_ROUTER_ECMP_HASH_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT", SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT),
    ("SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT", SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT),
    ("SX_ROUTER_ECMP_HASH_SMAC", SX_ROUTER_ECMP_HASH_SMAC),
    ("SX_ROUTER_ECMP_HASH_DMAC", SX_ROUTER_ECMP_HASH_DMAC),
    ("SX_ROUTER_ECMP_HASH_ETH_TYPE", SX_ROUTER_ECMP_HASH_ETH_TYPE),
    ("SX_ROUTER_ECMP_HASH_VID", SX_ROUTER_ECMP_HASH_VID),
    ("SX_ROUTER_ECMP_HASH_PCP", SX_ROUTER_ECMP_HASH_PCP),
    ("SX_ROUTER_ECMP_HASH_DEI", SX_ROUTER_ECMP_HASH_DEI)
)

def print_ecmp_hash_fields(ecmp_hash):
    for bit in ECMP_HASH_BITS:
        print("    %-40s %s" % (bit[0], (ecmp_hash & bit[1]) != 0))

def dump_ecmp_hash_params(handle):
    router_ecmp_hash_params = sx_router_ecmp_hash_params_t()
    rc = sx_api_router_ecmp_hash_params_get(handle, router_ecmp_hash_params)
    if rc != 0:
        print("[-] Error getting ECMP hash params: %d" % rc)
        return rc
    print("ECMP Hash params: %s" % router_ecmp_hash_params.ecmp_hash)
    print("    %-20s %s" % ("ECMP Hash Type:", router_ecmp_hash_params.ecmp_hash_type))
    print("    %-20s %d" % ("Symmetric Hash:", router_ecmp_hash_params.symmetric_hash))
    print("    %-20s %d" % ("Seed:", router_ecmp_hash_params.seed))
    print("    %-20s %d" % ("ECMP Hash:", router_ecmp_hash_params.ecmp_hash))
    print("ECMP Hash fields:")
    print_ecmp_hash_fields(router_ecmp_hash_params.ecmp_hash)
    return rc

def set_ecmp_hash(handle, ecmp_hash):
    router_ecmp_hash_params = sx_router_ecmp_hash_params_t()
    rc = sx_api_router_ecmp_hash_params_get(handle, router_ecmp_hash_params)
    if rc != 0:
        print("[-] Error getting ECMP hash params: %d" % rc)
        return rc
    router_ecmp_hash_params.ecmp_hash = new_ecmp_hash
    rc = sx_api_router_ecmp_hash_params_set(handle, router_ecmp_hash_params)
    if rc != 0:
        print("[-] Error setting ECMP hash params: %d" % rc) 
    return rc

def read_ecmp_hash_cfg(filename):
    ecmp_hash = 0
    hash_bits = dict(ECMP_HASH_BITS)
    try:
        with open(filename) as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("$"):
                    continue
                bit = hash_bits.get(line)
                if bit:
                    ecmp_hash |= bit
    except IOError:
        return None
    return ecmp_hash
            

print("[+] opening sdk")
rc, handle = sx_api_open(None)
if rc != 0:
    print("[-] Error opening SDK API: %d" % rc)
    sys.exit(rc)

print("[+] Getting ECMP hash params")
rc = dump_ecmp_hash_params(handle)
if rc != 0: 
    exit(rc)

# configure new ECMP hash values
print("[+] Reading ECMP hash configuration from %s" % ECMP_HASH_CFG)
new_ecmp_hash = read_ecmp_hash_cfg(ECMP_HASH_CFG)
if new_ecmp_hash is None:
    print("[-] Can't read ECMP hash configuration. Using default")
    new_ecmp_hash = DEFAULT_ECMP_HASH

print("[+] Setting new ECMP hash values: %d" % new_ecmp_hash)
rc = set_ecmp_hash(handle, new_ecmp_hash)
if rc != 0: 
    exit(rc)

print("[+] Getting updated ECMP hash params")
dump_ecmp_hash_params(handle)

print("[+] closing sdk")
sx_api_close(handle)