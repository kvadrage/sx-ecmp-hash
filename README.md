# sx-ecmp-hash
Tool to configure custom ECMP Hash parameters for Mellanox Spectrum Switches with Cumulus Linux.

# Requirements
Mellanox Spectrum Switches running Cumulus Linux 3.x.

## Build
`debuild -us -uc`

## Install
`sudo dpkg -i sx-ecmp-hash_x.x.x-cl_all.deb`

`sudo systemctl enable sx-ecmp-hash.service`

# Usage
After installation this package creates `sx-ecmp-hash.service`, which runs `sx_ecmp_hash.py` script just after Cumulus switchd starts or restarts.

This script reads custom ECMP hash configuration from `/etc/sx_ecmp_hash/sx_ecmp_hash.json` file and applies new ECMP Hash parameters using Mellanox SX SDK API.

## Considerations
There're two different ECMP Hash configuration modes upported in Mellanox SX SDK API for Spectrum switches:
- **Global configuration mode (legacy API)** - allows configuring only limited number of packet fields for ECMP hashing 
- **Port configuration mode (new API)** - allows very flexible ECMP Hash cnfiguration with ~50 different packet fields for hashing

Cumulus Linux 3.x is using **Global configuration mode** by default.

> **IMPORTANT NOTE:** 
> Switching from Global mode to Port mode is supported.
> However, ***switching back from Port mode to Global mode is not supported***. Need to reboot the device or reload SDK.

## Configuration examples

You can find more examples [here](./examples/).

### Legacy global ECMP Hash mode

```json
{
    "router_global_hash": {
    "hash_params": {
        "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_CRC",
        "symmetric_hash": false,
        "seed": 98335670
    },
    "hash_fields": [
        "SX_ROUTER_ECMP_HASH_SRC_IP",
        "SX_ROUTER_ECMP_HASH_DST_IP",
        "SX_ROUTER_ECMP_HASH_TCLASS",
        "SX_ROUTER_ECMP_HASH_FLOW_LABEL",
        "SX_ROUTER_ECMP_HASH_TCP_UDP",
        "SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT",
        "SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT",
        "SX_ROUTER_ECMP_HASH_SMAC",
        "SX_ROUTER_ECMP_HASH_DMAC",
        "SX_ROUTER_ECMP_HASH_ETH_TYPE",
        "SX_ROUTER_ECMP_HASH_VID",
        "SX_ROUTER_ECMP_HASH_PCP",
        "SX_ROUTER_ECMP_HASH_DEI"
    ]
    }
}
```

### New per-port ECMP Hash mode

#### Configuration for all ports
```json
{
    "router_port_hash": {
        "all": {
        "hash_params": {
            "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_CRC",
            "symmetric_hash": true,
            "seed": 98335670
        },
        "hash_fields_enable": [
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP",
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP",
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV4",
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV6"
        ],
        "hash_fields": [
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_0",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_1",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_2",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_3",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_0",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_1",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_2",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_3",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTES_0_TO_7",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_8",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_9",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_10",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_11",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_12",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_13",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_14",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_15",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTES_0_TO_7",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_8",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_9",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_10",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_11",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_12",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_13",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_14",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_15",
            "SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_SPORT",
            "SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_DPORT",
            "SX_ROUTER_ECMP_HASH_INNER_IPV4_PROTOCOL",
            "SX_ROUTER_ECMP_HASH_INNER_IPV6_NEXT_HEADER"
        ]
        }
    }
}
```


#### Configuration for specific ports
```json
{
    "router_port_hash": {
        "swp1": {
        "hash_params": {
            "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_CRC",
            "symmetric_hash": true,
            "seed": 98335670
        },
        "hash_fields_enable": [
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP"
        ],
        "hash_fields": [
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL",
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER"
        ]
        },
        "swp2": {
        "hash_params": {
            "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_XOR",
            "symmetric_hash": false,
            "seed": 1
        },
        "hash_fields_enable": [
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
            "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP"
        ],
        "hash_fields": [
            "SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL"          
        ]
        }
    }
}
```

## Supported ECMP Hash types
- SX_ROUTER_ECMP_HASH_TYPE_CRC 	
- SX_ROUTER_ECMP_HASH_TYPE_XOR 	
- SX_ROUTER_ECMP_HASH_TYPE_RANDOM	

## Supported ECMP Hash fields

### Legacy global ECMP Hash mode

**enum sx_router_ecmp_hash_bit**
sx_router_ecmp_hash_bit_t enumerated type is used to store router ECMP hash configuration bits.

- SX_ROUTER_ECMP_HASH_SRC_IP 	
- SX_ROUTER_ECMP_HASH_DST_IP 	
- SX_ROUTER_ECMP_HASH_TCLASS 	
- SX_ROUTER_ECMP_HASH_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT 	
- SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT 	
- SX_ROUTER_ECMP_HASH_SMAC 	
- SX_ROUTER_ECMP_HASH_DMAC 	
- SX_ROUTER_ECMP_HASH_ETH_TYPE 	
- SX_ROUTER_ECMP_HASH_VID 	
- SX_ROUTER_ECMP_HASH_PCP 	
- SX_ROUTER_ECMP_HASH_DEI

### New port-based ECMP Hash mode

#### hash_fields_enable

**enum sx_router_ecmp_hash_field_enable**
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_NON_IP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV6 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_NON_IP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV6 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV6 	

#### hash_fields

**enum sx_router_ecmp_hash_field**
sx_router_ecmp_hash_field_t enumerated type is used to store the specific layer fields and fields that should be included in the hash calculation, for both the outer header and the inner header.

- SX_ROUTER_ECMP_HASH_OUTER_SMAC 	
- SX_ROUTER_ECMP_HASH_OUTER_DMAC 	
- SX_ROUTER_ECMP_HASH_OUTER_ETHERTYPE 	
- SX_ROUTER_ECMP_HASH_OUTER_OVID 	            < Outer VID>
- SX_ROUTER_ECMP_HASH_OUTER_OPCP 	            < Outer PCP>
- SX_ROUTER_ECMP_HASH_OUTER_ODEI 	            < Outer DEI>
- SX_ROUTER_ECMP_HASH_OUTER_IVID 	            < Inner VID>            
- SX_ROUTER_ECMP_HASH_OUTER_IPCP 	            < Inner PCP>            
- SX_ROUTER_ECMP_HASH_OUTER_IDEI 	            < Inner DEI>            
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DSCP 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_ECN 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_IP_L3_LENGTH 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DSCP 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_ECN 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_IP_L3_LENGTH 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_SIP 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DIP 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_NEXT_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DSCP 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_ECN 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_L3_LENGTH 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_OUTER_FCOE_SID 	
- SX_ROUTER_ECMP_HASH_OUTER_FCOE_DID 	
- SX_ROUTER_ECMP_HASH_OUTER_FCOE_OXID 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_0 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_1 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_2 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_3 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_4 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_5 	
- SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_SPORT 	
- SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_DPORT 	
- SX_ROUTER_ECMP_HASH_OUTER_BTH_DQPN 	
- SX_ROUTER_ECMP_HASH_OUTER_BTH_PKEY 	
- SX_ROUTER_ECMP_HASH_OUTER_BTH_OPCODE 	
- SX_ROUTER_ECMP_HASH_OUTER_DETH_QKEY 	
- SX_ROUTER_ECMP_HASH_OUTER_DETH_SQPN 	
- SX_ROUTER_ECMP_HASH_OUTER_VNI 	
- SX_ROUTER_ECMP_HASH_OUTER_NVGRE_FLOW 	
- SX_ROUTER_ECMP_HASH_OUTER_NVGRE_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_OUTER_LAST 	
- SX_ROUTER_ECMP_HASH_INNER_SMAC 	
- SX_ROUTER_ECMP_HASH_INNER_DMAC 	
- SX_ROUTER_ECMP_HASH_INNER_ETHERTYPE 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_NEXT_HEADER 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_SPORT 	
- SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_DPORT 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_DQPN 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_PKEY 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_OPCODE 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_QKEY 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_SQPN 	
- SX_ROUTER_ECMP_HASH_INNER_LAST 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_INGRESS_PORT_NUMBER 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_0 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_1 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_2 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_3 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_4 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_5 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_6 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_7 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_8 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_9 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_10 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_11 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_12 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_13 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_14 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_15 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_LAST 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_LAST 	
- SX_ROUTER_ECMP_HASH_MIN 	
- SX_ROUTER_ECMP_HASH_MAX 


# Support
Please contact Mellanox Support for any additional help:
https://mymellanox.force.com/support/SupportLogin 