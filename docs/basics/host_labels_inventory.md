#Hosts, Labels and Inventory

CMDB Syncer works with Hosts, Labels and Inventory. So far so simple, but what is what?

## Hosts
A Host is any kind of Device. It's identified by his hostname, bound to a source and contains
Labels and Inventory


## Labels and Inventory
Labels and Inventory are mostly the same, but have an important difference.
They both are Key:Value pairs, can be used in all Rules, Rewritten and Filtered.

The difference is only how they are dealt with their creation.
While the Labels are Imported and fully under control of the Import Plugin,
can inventory data come from multiple sources. Inventory Keys share their sources identify, as a prefix on their name.

Example:

- csv_ipaddress:127.0.0.1
- csv_alias:Test Server
- srctest_service_name: Test Service

In this example, you see Inventory Data of two sources, one is csv_, the other is srctest_.
So, the plugin using the key csv_, will control all keys with csv_ and the plugin with srctest as key, the others.