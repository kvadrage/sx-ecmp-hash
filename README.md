# sx-ecmp-hash
Setting custom ECMP Hash for Mellanox Switches with Cumulus Linux

# Requirements
Mellanox Spectrum Switches running Cumulus Linux 3.x

## Build
`debuild -us -uc`

## Install
`sudo dpkg -i sx-ecmp-hash_x.x.x-cl_all.deb`

`sudo systemctl enable sx-ecmp-hash.service`

## Usage
After installation this package creates `sx-ecmp-hash.service`, which runs `sx_ecmp_hash.py` script just after Cumulus switchd starts or restarts.

Script tries to read custom ECMP hash configuration from `/etc/sx_ecmp_hash.conf` file and apply new ECMP Hash params using Mellanox SDK API.
If configuration file is not available the script applies default ECMP Hash config with the following fields activated:
- SX_ROUTER_ECMP_HASH_SRC_IP
- SX_ROUTER_ECMP_HASH_DST_IP
- SX_ROUTER_ECMP_HASH_TCP_UDP
- SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT
- SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT
- SX_ROUTER_ECMP_HASH_SMAC
- SX_ROUTER_ECMP_HASH_DMAC
- SX_ROUTER_ECMP_HASH_ETH_TYPE
- SX_ROUTER_ECMP_HASH_VID

