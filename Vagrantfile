# Arista config: enable eAPI and configure mgmt iface


Vagrant.configure(2) do |config|

  config.vm.define "cumulus" do |cumulus|
      cumulus.vm.box = "CumulusCommunity/cumulus-vx"
      cumulus.vm.provider "Virtualbox" do |v|
        v.memory = 1024
      end
      cumulus.vm.network "private_network", ip: "192.168.50.3", auto_config: false
      cumulus.vm.network "private_network", virtualbox__intnet: "swp1", auto_config: false
      cumulus.vm.network "private_network", virtualbox__intnet: "swp2", auto_config: false
      cumulus.vm.network "private_network", virtualbox__intnet: "swp3", auto_config: false
      cumulus.vm.network "private_network", virtualbox__intnet: "swp4", auto_config: false

      cumulus.vm.provision "shell", inline: "sudo net add interface swp1 ip address 192.168.50.3/24; net pending; net commit;"
  end

  config.vm.define "arista" do |arista|
      arista.vm.box = "vEOS-lab-4.18.1F"
      arista.vm.provider "Virtualbox" do |v|
        v.memory = 2048 
      end
      arista.vm.network "private_network", ip: "192.168.50.4", auto_config: false
      arista.vm.network "private_network", virtualbox__intnet: "swp1", auto_config: false
      arista.vm.network "private_network", virtualbox__intnet: "swp2", auto_config: false
      arista.vm.network "private_network", virtualbox__intnet: "swp3", auto_config: false
      arista.vm.network "private_network", virtualbox__intnet: "swp4", auto_config: false

      arista.vm.provision 'shell', inline: <<-SHELL
route add default gw 10.0.2.2 dev ma1
pip install pyeapi
 FastCli -p 15 -c "configure
username eapiuser privilege 15 role network-admin secret icanttellyou
management api http-commands
no shutdown
protocol https
conf t
int e 1
no switchport
ip add 192.168.50.4/24
end
copy running-config startup-config"
SHELL

  end

end


