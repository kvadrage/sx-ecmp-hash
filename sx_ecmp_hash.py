#!/usr/bin/python
'''
This script is setting custom ECMP Hash fields for Mellanox Switches.
It tries to read and apply ECMP Hash configuration from /etc/sx_ecmp_hash.json.

'''

import sys
import errno
import json
import argparse

try:
    from python_sdk_api.sx_api import *
except:
    print("Error: can't import SX SDK API Python library!")
    sys.exit(-1)
 
PORT_NAME_PREFIX = "swp"
DEFAULT_ECMP_HASH_CFG = "/etc/sx_ecmp_hash/sx_ecmp_hash.json"

SX_ROUTER_ECMP_HASH_TYPE = dict((
    ("SX_ROUTER_ECMP_HASH_TYPE_CRC", SX_ROUTER_ECMP_HASH_TYPE_CRC),
    ("SX_ROUTER_ECMP_HASH_TYPE_XOR", SX_ROUTER_ECMP_HASH_TYPE_XOR),
    ("SX_ROUTER_ECMP_HASH_TYPE_RANDOM", SX_ROUTER_ECMP_HASH_TYPE_RANDOM)
))

SX_ROUTER_GLOBAL_ECMP_HASH_FIELD = dict((
    ("SX_ROUTER_ECMP_HASH_SRC_IP", SX_ROUTER_ECMP_HASH_SRC_IP),
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
))


SX_ROUTER_PORT_ECMP_HASH_FIELD_ENABLE = dict((
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_NON_IP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_NON_IP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV4", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV4),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV6", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV6),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV4", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV4),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_NON_IP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_NON_IP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV4", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV4),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV6", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV6),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV4", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV4),
    ("SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV6", SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV6)
))

SX_ROUTER_PORT_ECMP_HASH_FIELD = dict((
    ("SX_ROUTER_ECMP_HASH_OUTER_SMAC", SX_ROUTER_ECMP_HASH_OUTER_SMAC),
    ("SX_ROUTER_ECMP_HASH_OUTER_DMAC", SX_ROUTER_ECMP_HASH_OUTER_DMAC),
    ("SX_ROUTER_ECMP_HASH_OUTER_ETHERTYPE", SX_ROUTER_ECMP_HASH_OUTER_ETHERTYPE),
    ("SX_ROUTER_ECMP_HASH_OUTER_OVID", SX_ROUTER_ECMP_HASH_OUTER_OVID),
    ("SX_ROUTER_ECMP_HASH_OUTER_OPCP", SX_ROUTER_ECMP_HASH_OUTER_OPCP),
    ("SX_ROUTER_ECMP_HASH_OUTER_ODEI", SX_ROUTER_ECMP_HASH_OUTER_ODEI),
    ("SX_ROUTER_ECMP_HASH_OUTER_IVID", SX_ROUTER_ECMP_HASH_OUTER_IVID),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPCP", SX_ROUTER_ECMP_HASH_OUTER_IPCP),
    ("SX_ROUTER_ECMP_HASH_OUTER_IDEI", SX_ROUTER_ECMP_HASH_OUTER_IDEI),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_0", SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_0),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_1", SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_1),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_2", SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_2),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_3", SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_3),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_0", SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_0),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_1", SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_1),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_2", SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_2),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_3", SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_3),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_PROTOCOL", SX_ROUTER_ECMP_HASH_OUTER_IPV4_PROTOCOL),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_DSCP", SX_ROUTER_ECMP_HASH_OUTER_IPV4_DSCP),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_ECN", SX_ROUTER_ECMP_HASH_OUTER_IPV4_ECN),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV4_IP_L3_LENGTH", SX_ROUTER_ECMP_HASH_OUTER_IPV4_IP_L3_LENGTH),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15", SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER", SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_DSCP", SX_ROUTER_ECMP_HASH_OUTER_IPV6_DSCP),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_ECN", SX_ROUTER_ECMP_HASH_OUTER_IPV6_ECN),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_IP_L3_LENGTH", SX_ROUTER_ECMP_HASH_OUTER_IPV6_IP_L3_LENGTH),
    ("SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL", SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_SIP", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_SIP),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DIP", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DIP),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_NEXT_PROTOCOL", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_NEXT_PROTOCOL),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DSCP", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DSCP),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_ECN", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_ECN),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_L3_LENGTH", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_L3_LENGTH),
    ("SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_FLOW_LABEL", SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_FLOW_LABEL),
    ("SX_ROUTER_ECMP_HASH_OUTER_FCOE_SID", SX_ROUTER_ECMP_HASH_OUTER_FCOE_SID),
    ("SX_ROUTER_ECMP_HASH_OUTER_FCOE_DID", SX_ROUTER_ECMP_HASH_OUTER_FCOE_DID),
    ("SX_ROUTER_ECMP_HASH_OUTER_FCOE_OXID", SX_ROUTER_ECMP_HASH_OUTER_FCOE_OXID),
    ("SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_0", SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_0),
    ("SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_1", SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_1),
    ("SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_2", SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_2),
    ("SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_3", SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_3),
    ("SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_4", SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_4),
    ("SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_5", SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_5),
    ("SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_SPORT", SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_SPORT),
    ("SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_DPORT", SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_DPORT),
    ("SX_ROUTER_ECMP_HASH_OUTER_BTH_DQPN", SX_ROUTER_ECMP_HASH_OUTER_BTH_DQPN),
    ("SX_ROUTER_ECMP_HASH_OUTER_BTH_PKEY", SX_ROUTER_ECMP_HASH_OUTER_BTH_PKEY),
    ("SX_ROUTER_ECMP_HASH_OUTER_BTH_OPCODE", SX_ROUTER_ECMP_HASH_OUTER_BTH_OPCODE),
    ("SX_ROUTER_ECMP_HASH_OUTER_DETH_QKEY", SX_ROUTER_ECMP_HASH_OUTER_DETH_QKEY),
    ("SX_ROUTER_ECMP_HASH_OUTER_DETH_SQPN", SX_ROUTER_ECMP_HASH_OUTER_DETH_SQPN),
    ("SX_ROUTER_ECMP_HASH_OUTER_VNI", SX_ROUTER_ECMP_HASH_OUTER_VNI),
    ("SX_ROUTER_ECMP_HASH_OUTER_NVGRE_FLOW", SX_ROUTER_ECMP_HASH_OUTER_NVGRE_FLOW),
    ("SX_ROUTER_ECMP_HASH_OUTER_NVGRE_PROTOCOL", SX_ROUTER_ECMP_HASH_OUTER_NVGRE_PROTOCOL),
    ("SX_ROUTER_ECMP_HASH_OUTER_LAST", SX_ROUTER_ECMP_HASH_OUTER_LAST),
    ("SX_ROUTER_ECMP_HASH_INNER_SMAC", SX_ROUTER_ECMP_HASH_INNER_SMAC),
    ("SX_ROUTER_ECMP_HASH_INNER_DMAC", SX_ROUTER_ECMP_HASH_INNER_DMAC),
    ("SX_ROUTER_ECMP_HASH_INNER_ETHERTYPE", SX_ROUTER_ECMP_HASH_INNER_ETHERTYPE),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_0", SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_0),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_1", SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_1),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_2", SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_2),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_3", SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_3),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_0", SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_0),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_1", SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_1),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_2", SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_2),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_3", SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_3),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV4_PROTOCOL", SX_ROUTER_ECMP_HASH_INNER_IPV4_PROTOCOL),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTES_0_TO_7", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTES_0_TO_7),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_8", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_8),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_9", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_9),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_10", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_10),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_11", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_11),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_12", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_12),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_13", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_13),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_14", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_14),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_15", SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_15),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTES_0_TO_7", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTES_0_TO_7),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_8", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_8),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_9", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_9),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_10", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_10),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_11", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_11),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_12", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_12),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_13", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_13),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_14", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_14),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_15", SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_15),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_NEXT_HEADER", SX_ROUTER_ECMP_HASH_INNER_IPV6_NEXT_HEADER),
    ("SX_ROUTER_ECMP_HASH_INNER_IPV6_FLOW_LABEL", SX_ROUTER_ECMP_HASH_INNER_IPV6_FLOW_LABEL),
    ("SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_SPORT", SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_SPORT),
    ("SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_DPORT", SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_DPORT),
    ("SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_DQPN", SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_DQPN),
    ("SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_PKEY", SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_PKEY),
    ("SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_OPCODE", SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_OPCODE),
    ("SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_QKEY", SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_QKEY),
    ("SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_SQPN", SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_SQPN),
    ("SX_ROUTER_ECMP_HASH_INNER_LAST", SX_ROUTER_ECMP_HASH_INNER_LAST),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_INGRESS_PORT_NUMBER", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_INGRESS_PORT_NUMBER),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_0", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_0),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_1", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_1),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_2", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_2),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_3", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_3),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_4", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_4),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_5", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_5),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_6", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_6),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_7", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_7),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_8", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_8),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_9", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_9),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_10", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_10),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_11", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_11),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_12", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_12),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_13", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_13),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_14", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_14),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_15", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_15),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_LAST", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_LAST),
    ("SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_LAST", SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_LAST)
))

PORT_TYPE_NVE = 8
PORT_TYPE_VPORT = 2
PORT_TYPE_OFFSET = 28
PORT_TYPE_MASK = 0xF0000000


def check_vport(port):
    port_type = (port & PORT_TYPE_MASK) >> PORT_TYPE_OFFSET
    return port_type & PORT_TYPE_VPORT

def check_nve(port):
    port_type = (port & PORT_TYPE_MASK) >> PORT_TYPE_OFFSET
    return port_type & PORT_TYPE_NVE

def set_port_ecmp_hash_params(log_port, hash_params, hash_field_enable_list, hash_field_list):
    ecmp_hash_params_p = new_sx_router_ecmp_port_hash_params_t_p()
    ecmp_hash_params_p.ecmp_hash_type = hash_params.ecmp_hash_type
    ecmp_hash_params_p.seed = hash_params.seed
    ecmp_hash_params_p.symmetric_hash = hash_params.symmetric_hash
    
    hash_field_enable_list_cnt = len(hash_field_enable_list)
    hash_field_enable_list_arr = new_sx_router_ecmp_hash_field_enable_t_arr(hash_field_enable_list_cnt)
    
    hash_field_list_cnt = len(hash_field_list)
    hash_field_list_arr = new_sx_router_ecmp_hash_field_t_arr(hash_field_list_cnt)
    
    for i, field_name in enumerate(hash_field_enable_list):
        field = SX_ROUTER_PORT_ECMP_HASH_FIELD_ENABLE.get(field_name)
        if field:
            sx_router_ecmp_hash_field_enable_t_arr_setitem(hash_field_enable_list_arr, i, field)

    for i, field_name in enumerate(hash_field_list):
        field = SX_ROUTER_PORT_ECMP_HASH_FIELD.get(field_name)
        if field:
            sx_router_ecmp_hash_field_t_arr_setitem(hash_field_list_arr, i, field)
        
    rc = sx_api_router_ecmp_port_hash_params_set(handle, SX_ACCESS_CMD_SET, log_port, ecmp_hash_params_p, hash_field_enable_list_arr, hash_field_enable_list_cnt, hash_field_list_arr, hash_field_list_cnt)

    return rc

    
def print_global_ecmp_hash_params(ecmp_hash_params):
    if rc != 0:
        print("[-] Error getting ECMP hash params: %d" % rc)
        return rc
    print("ECMP Hash params:")
    print("    %-20s %s" % ("ECMP Hash Type:", ecmp_hash_params.ecmp_hash_type))
    print("    %-20s %d" % ("Symmetric Hash:", ecmp_hash_params.symmetric_hash))
    print("    %-20s %d" % ("Seed:", ecmp_hash_params.seed))
    print("    %-20s %d" % ("ECMP Hash:", ecmp_hash_params.ecmp_hash))
    print("ECMP Hash fields:")
    for name, bit in SX_ROUTER_GLOBAL_ECMP_HASH_FIELD:
        print("    %-40s %s" % (name, (ecmp_hash_params.ecmp_hash & bit) != 0))
    return rc

def get_global_ecmp_hash_params(handle):
    ecmp_hash_params = sx_router_ecmp_hash_params_t()
    rc = sx_api_router_ecmp_hash_params_get(handle, ecmp_hash_params)
    if rc != 0:
        return rc, None
    return rc, ecmp_hash_params


def set_global_ecmp_hash_params(handle, ecmp_hash_params):
    rc = sx_api_router_ecmp_hash_params_set(handle, ecmp_hash_params)
    return rc
            

def apply_global_ecmp_hash_cfg(handle, global_hash_config):
    new_hash_params = sx_router_ecmp_hash_params_t()
    
    print("[+] Applying legacy global ECMP Hash configuration")
    
    rc, curr_hash_params = get_global_ecmp_hash_params(handle)
    if rc != 0:
        print("[--] Error getting legacy global ECMP hash params: %d" % rc)
        print("[--] Probably new per-port ECMP Hash mode is already configured")
        return rc
    
    global_hash_params = global_hash_config.get("hash_params", {})
  
    hash_type = global_hash_params.get("hash_type")
    if hash_type:
        new_hash_params.ecmp_hash_type = SX_ROUTER_ECMP_HASH_TYPE.get(hash_type, curr_hash_params.ecmp_hash_type)
    else:
        new_hash_params.ecmp_hash_type = curr_hash_params.ecmp_hash_type
    
    new_hash_params.seed = global_hash_params.get("seed", curr_hash_params.seed)   
    new_hash_params.symmetric_hash = global_hash_params.get("symmetric_hash", curr_hash_params.symmetric_hash)
    
    hash_fields = global_hash_config.get("hash_fields")
    if hash_fields:
        ecmp_hash = 0
        for field in hash_fields:
            ecmp_hash |= SX_ROUTER_GLOBAL_ECMP_HASH_FIELD.get(field)
        new_hash_params.ecmp_hash = ecmp_hash
    else:
        new_hash_params.ecmp_hash = curr_hash_params.ecmp_hash

    return set_global_ecmp_hash_params(handle, new_hash_params)

def process_single_port_ecmp_hash_cfg(handle, log_port, port_hash_config, global_hash_params=None):
    port_hash_params_t_p = new_sx_router_ecmp_port_hash_params_t_p()
    if global_hash_params:
        port_hash_params_t_p.ecmp_hash_type = global_hash_params.ecmp_hash_type
        port_hash_params_t_p.seed = global_hash_params.seed
        port_hash_params_t_p.symmetric_hash = global_hash_params.symmetric_hash
    
    hash_params = port_hash_config.get("hash_params")
    hash_type = hash_params.get("hash_type")
    if hash_type:
        port_hash_params_t_p.ecmp_hash_type = SX_ROUTER_ECMP_HASH_TYPE.get(hash_type, 0)
    
    seed = hash_params.get("seed")
    if seed:
        port_hash_params_t_p.seed = seed
    
    symmetric_hash = hash_params.get("symmetric_hash")
    if symmetric_hash:
        port_hash_params_t_p.symmetric_hash = symmetric_hash
    
    hash_fields_enable = port_hash_config.get("hash_fields_enable")
    hash_fields = port_hash_config.get("hash_fields")
    if hash_fields_enable is None or hash_fields is None:
        print("[--] No 'hash_fields_enable' or 'hash_fields' section found in the configuration")
        return -1
    
    rc = set_port_ecmp_hash_params(log_port, port_hash_params_t_p, hash_fields_enable, hash_fields)
    
    return rc

def apply_port_ecmp_hash_cfg(handle, port_hash_config):
    ports_map = []
    port_num_max = 128
    port_attributes_list = new_sx_port_attributes_t_arr(port_num_max)
    port_cnt_p = new_uint32_t_p()
    uint32_t_p_assign(port_cnt_p, port_num_max)

    print("[+] Applying new port-based ECMP Hash configuration")

    # dump all device ports information
    rc = sx_api_port_device_get(handle, 1, 0, port_attributes_list, port_cnt_p)
    if rc != 0:
        print("[--] Error getting switchs ports information")
        return rc
    port_cnt = uint32_t_p_value(port_cnt_p)

    # populate port name (label name) to log_port mapping
    for i in range(port_cnt):
        port_attributes = sx_port_attributes_t_arr_getitem(port_attributes_list, i)
        is_vport = check_vport(int(port_attributes.log_port))
        is_nve = check_nve(int(port_attributes.log_port))
        if is_nve or is_vport:
            continue    
        port_name = "%s%d" % (PORT_NAME_PREFIX, port_attributes.port_mapping.module_port + 1)
        ports_map.append((port_name, port_attributes.log_port))
    
    # try to get existing global ECMP hash configuration
    rc, curr_global_hash_params = get_global_ecmp_hash_params(handle)
    if rc == 0:
        print("[++] Legacy global ECMP Hash mode is currently configured")
        print("[++] Overriding it with new per-port ECMP Hash configuration")
    
    # check if aggregate configuration for all ports is available
    all_ports_cfg = port_hash_config.get("all")
    if all_ports_cfg:
        print("[++] Applying single ECMP Hash configuration to all ports")
        result = 0
        for port_name, log_port in ports_map:
            print("[+++] Applying ECMP Hash configuration to port %s (log_port %x)" % (port_name, log_port))
            rc = process_single_port_ecmp_hash_cfg(handle, log_port, all_ports_cfg, curr_global_hash_params)
            if rc != 0:
                print("[---] Error applying ECMP Hash config on port %s (log_port %x)" % (port_name, log_port))
                result = rc
        return result
    
    result = 0
    # iterate all specific ports in the config
    for port_name, hash_config in port_hash_config.items(): 
        ports = [(port_name, log_port) for name,log_port in ports_map if name in port_name]
        if not ports:
            print("[--] Port %s doesn't exist" % port_name)
            continue
        for port_name, log_port in ports:
            print("[++] Applying ECMP Hash configuration to port %s (log_port %x)" % (port_name, log_port))
            rc = process_single_port_ecmp_hash_cfg(handle, log_port, hash_config, curr_global_hash_params)
            if rc != 0:
                print("[--] Error applying ECMP Hash config on port %s (log_port %x)" % (port_name, log_port))
                result = rc
    return result

def apply_ecmp_hash_cfg(handle, config):
    if not config:
        print("[-] Config undefined")
        return None
    
    global_hash_config = config.get("router_global_hash")
    if global_hash_config:
        return apply_global_ecmp_hash_cfg(handle, global_hash_config)
        
    port_hash_config = config.get("router_port_hash")
    if port_hash_config:
        return apply_port_ecmp_hash_cfg(handle, port_hash_config)
        
    print("[-] No ECMP Hash config provided")
    return None

def read_ecmp_hash_cfg(filename):
    config = None
    try:
        with open(filename) as fh:
            config = json.loads(fh.read())
    except IOError as e:
        print("[-] Error reading config file: %s" % e)
    except ValueError as e:
        print("[-] Error parsing config file: %s" % e)
    return config


def parse_args():
    parser = argparse.ArgumentParser(description="Mellanox ECMP Hash configuration tool")
    parser.add_argument("-c", "--config-file", help="Configuration file (json)", default=DEFAULT_ECMP_HASH_CFG)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    print("[+] Reading ECMP hash configuration from '%s'" % args.config_file)
    config = read_ecmp_hash_cfg(args.config_file)

    if not config:
        sys.exit(-1)
    
    print("[+] opening sdk")
    rc, handle = sx_api_open(None)
    if rc != 0:
        print("[-] Error opening SDK API: %d" % rc)
        sys.exit(rc)

    rc = apply_ecmp_hash_cfg(handle, config)
    if rc == 0:
        print("[+] ECMP Hash configuration applied successfully!")
    else:
        print("[-] Error applying ECMP Hash configuration: %d" % rc)

    print("[+] closing sdk")
    sx_api_close(handle)
    sys.exit(rc)
