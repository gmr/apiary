apiary
======
Apiary is a modern data-center management tool that includes provisioning,
configuration management and inventory control.

Inventory Management
--------------------
Instead of treating inventory management as an after-thought or leaving it to an
external system, Apiary is designed to be the canonical source of information
about systems in your data center. Servers may be added via the administration
interface or via a RESTful API. Each systems has an event log which may be used
to keep track of incidents and service history. Setup Nagios to email Apiary for
alerts and recoveries and Apiary can keep track of hardware and software
problems automatically.

Using Apiary's inventory discovery agent or startup environment, all information
available in the operating system about a system, such as its manufacturer,
model, serial number, UUID and hardware specifications will be automatically
added to the inventory management system.

Server Provisioning
-------------------
Apiary allows for the installation of CentOS and Ubuntu based linux systems and
may be used for other types of systems as well. Installation media is imported
into Apiary, where in combination with the management of dhcpd, new systems can
be PXE booted into an automated network install. Using Apiary's powerful
configuration management allows for "out-of-the-box" provisioning of system with
their appropriate configuration.

Configuration Management
------------------------
Apiary uses the same configuration management concepts if you are provisioning a
new system or deploying configuration changes to an existing system:

- Packages are a natural mapping to distribution specific package management
conventions such as rpm files in RedHat based distributions or .deb files in
Ubuntu.

- Management classes can be used to indicate packages which should be installed
and configuration file templates should be used when provisioning or managing a
system.

- Tagging provides context about a system for configuration templates, triggers
and in the administration interface. Tags can be used for both package
installation and for configuration file templates.

- Systems can also be organized into a colony, grouping them together for
configuration management. Colonies are useful for creating organized system
groupings such as for Hadoop or RabbitMQ clusters managed by the same Apiary
server.

DNS Management
--------------
If you let Apiary managed your DNS, as systems are added, updated and removed
in the system inventory, DNS is automatically updated. Individual colonies may
specify host name templates allowing for granular multi-level domain names for
groups of systems.

Integration with External Applications
--------------------------------------
Based upon events that occur during the lifespan of a system, Apiary is able to
interface with external systems. Servers can be enabled and disabled in a load
balancer and managed in tools like Nagios or New Relic.

Organization Example
--------------------
Suppose you are adding a server to a new Hadoop cluster on your network.
Assigning the "Hadoop" management class to the server tells Apiary it should
use all of the configuration templates for a Hadoop server. Because you may
want to run multiple Hadoop  clusters, this server should be assigned to a
distinct colony for the Hadoop cluster it is to belong in. Finally, the server
should be tagged with its role in the cluster, indicating if it's a name node,
secondary name node, job tracker, or some other role.
