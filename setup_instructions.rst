Instructions
=============

Create a VM as per following requirements.


OS requirements
+++++++++++++++

- `CentOS 7 Minimal <http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1503-01.iso>`_

Hardware Requirements
+++++++++++++++++++++

- Memory: 4GB
- Processor: 4processors

After VM is ready
+++++++++++++++++

- To install RDO run **install_rdo.sh**.
- And once RDO is installed successfully run **auth_and_list_networks.py** to login as admin and list all the networks in Openstack.



**Note**

While this script was written there were some issue related to installing RDO. Here [1] is workaround to the bug.

[1] https://ask.openstack.org/en/question/85014/error-could-not-find-data-item-config_use_subnets-in-any-hiera-data-file/

