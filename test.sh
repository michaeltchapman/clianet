vagrant up cumulus
clianet 192.168.50.3 --user vagrant -i .vagrant/machines/cumulus/virtualbox/private_key cumulus port swp3 add_vlan 15
