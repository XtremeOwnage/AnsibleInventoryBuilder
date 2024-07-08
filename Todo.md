## My Personal TODO List

Building and Deployment:
- [ ] DEB Package
- [ ] Linux Deployment Script


Github Items:
- [ ] Github CI/CD
- [ ] License 
- [ ] Contribution Guidelines.
- [ ] Ticket Templates

Misc Organization:
- [X] change host vars dir to hosts.
- [X] change group var dirs to groups.
- [X] rename group criteria to host criteria 
- [ ] add group criteria, to automatically nest groups

add collection operators 
- [ ] in collection 
- [ ] not in collection 
- [ ] length operator (count)

Add IP/Subnet Comparison Operators:
- [ ] "IP" ISIP Operator
- [ ] "IP" INSUBNET 10.100.1.0/24 (Check if IP is inside of the specified subnet)

add operands
- [X] gtz
- [X] eqz
- [X] ltz
- [X] nez

add support to host
- [ ] collection of groups

add support to groups 
- [ ] collection of hosts
- [ ] collection of children 
- [ ] collection of parents groups

Add caching
- [X] option to enable / disable cache
- [X] create dedicated cache library file
- [X] create unit tests for caching library.

add example ansible.cfg

proxmox support
- [ ] pull host
- [ ] pull lxc 
- [ ] pull vms
- [ ] tag vm/lxc
- [ ] copy proxmox tag
- [ ] support for pct enter


globals revamp
- [X] store config in /etc as yaml
- [X] store in current dir