
.. image:: https://travis-ci.org/internap/cellar.svg?branch=master
    :target: https://travis-ci.org/internap/cellar

======
cellar
======

OpenStack Ironic and Neutron have uncovered a need in the OpenStack world: a CMDB.
Currently, there is no component to keep track of your assets and the way they are
connected. We suggest creating OpenStack Cellar. This component would be responsible
to track assets like Physical Servers, Network Switches, Racks, and their relations.

It would only track assets and not be responsible to act on them. For example, managing
the power state for a Physical Server would go through Ironic. By creating this component,
we aim to reduce the complexity and multi-vendor aspect of managing a datacenter.

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/cellar
* Source: http://git.openstack.org/cgit/openstack/cellar
* Bugs: http://bugs.launchpad.net/cellar
