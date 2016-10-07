AUTO CIDR
=========

Automatically generate CIDRs for the subnets in your VPC.

Given the:
  * CIDR of the VPC
  * hash of Subnets
    * subnet can specify 'MinSize' (defaults to 16 (/28 prefix) which is the minimum AWS allows)

Returns the dictionary of subnets with 'cidr' added for each subnet

### Install

```
pip install -t lib/ -r requirements.txt
```
