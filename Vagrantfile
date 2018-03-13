# Decent example of vagrant-libvirt switch style setup here:
# https://github.com/skamithi/vagrant-cw-libvirt/blob/master/Vagrantfile


swp10 = [8010, 9010]
swp11 = [8011, 9011]
swp12 = [8012, 9012]
swp13 = [8013, 9013]

# Arista box is created locally, following:
# https://codingpackets.com/blog/arista-vagrant-libvirt-box-install/
# CHANGE AS NEEDED IF USING ARISTA
arista_boot_iso_path = "/var/lib/libvirt/images/Aboot-veos-8.0.0.iso"

Vagrant.configure(2) do |config|

  config.vm.define "cumulus" do |cumulus|
      cumulus.vm.box = "CumulusCommunity/cumulus-vx"
      #cumulus.vm.provider "Virtualbox" do |v|
      #  v.memory = 1024
#
#	cumulus.vm.network "private_network", ip: "192.168.50.3", auto_config: false
#	cumulus.vm.network "private_network", virtualbox__intnet: "swp1", auto_config: false
#	cumulus.vm.network "private_network", virtualbox__intnet: "swp2", auto_config: false
#	cumulus.vm.network "private_network", virtualbox__intnet: "swp3", auto_config: false
#	cumulus.vm.network "private_network", virtualbox__intnet: "swp4", auto_config: false
#      end

      cumulus.vm.provider :libvirt do |libvirt|
        libvirt.memory = 1024 
      end

      cumulus.vm.synced_folder '.', '/vagrant', :disabled => true

      config.vm.network :private_network,
        :auto_config => false,
        :libvirt__network_name => "mgmt",
        :libvirt__dhcp_enabled => false,
        :libvirt__forward_mode => 'veryisolated'

	config.vm.network "private_network",
         :libvirt__tunnel_type => "udp",
         :libvirt__tunnel_port => swp10[0],
         :libvirt__tunnel_local_port => swp10[1]

	config.vm.network "private_network",
          :libvirt__tunnel_type => "udp",
          :libvirt__tunnel_port => swp11[0],
          :libvirt__tunnel_local_port => swp11[1]

	config.vm.network "private_network",
          :libvirt__tunnel_type => "udp",
          :libvirt__tunnel_port => swp12[0],
          :libvirt__tunnel_local_port => swp12[1]

	config.vm.network "private_network",
         :libvirt__tunnel_type => "udp",
          :libvirt__tunnel_port => swp13[0],
          :libvirt__tunnel_local_port => swp13[1]

      cumulus.vm.provision "shell", inline: "sudo net add interface swp1 ip address 192.168.50.3/24; net pending; net commit;"

  end

  
  config.vm.define "arista" do |arista|
      #arista.vm.provider "Virtualbox" do |v|
      #  v.memory = 2048 
      #end
      #arista.vm.network "private_network", ip: "192.168.50.4", auto_config: false
      #arista.vm.network "private_network", virtualbox__intnet: "swp1", auto_config: false
      #arista.vm.network "private_network", virtualbox__intnet: "swp2", auto_config: false
      #arista.vm.network "private_network", virtualbox__intnet: "swp3", auto_config: false
      #arista.vm.network "private_network", virtualbox__intnet: "swp4", auto_config: false

    arista.vm.box = "arista/veos-box"

    # Turn off shared folders
    arista.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    # Dont change default SSH key - already in image
    arista.ssh.insert_key = false

    # Set guest type to prevent guest type detection
    #arista.vm.guest = :freebsd

    arista.vm.provider :libvirt do |domain|
      #domain.nic_adapter_count = 1
      domain.cpu_mode = "custom"
      domain.cpu_model = nil
      domain.driver = "kvm"
      domain.machine_type = "pc-i440fx-1.5"
      domain.emulator_path = "/usr/bin/qemu-system-x86_64"
      domain.disk_bus = 'ide'
      domain.cpus = 2
      domain.memory = 2048
      # this needs to be set to the aboot image, which can be obtained from the
      # arista website
      domain.storage :file, :device => :cdrom, dev: "hdc", :path => "/var/lib/libvirt/images/Aboot-veos-8.0.0.iso"
      # Boot from cd first
      domain.boot 'cdrom'
      domain.boot 'hd'

      #domain.management_network_mode = 'none'
    end  

    #arista.vm.network "private_network",
    #  :libvirt__tunnel_type => "udp",
    #  :libvirt__tunnel_port => swp10[0],
    #  :libvirt__tunnel_local_port => swp10[1]

    arista.vm.network "private_network",
      auto_config: false,
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_port => '9001',
      :libvirt__tunnel_local_port => '8001'
    # em4
    arista.vm.network "private_network",
      auto_config: false,
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_port => '9002',
      :libvirt__tunnel_local_port => '8002'
    # em5
    arista.vm.network "private_network",
      auto_config: false,
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_port => '9003',
      :libvirt__tunnel_local_port => '8003'
    # em6
    arista.vm.network "private_network",
      auto_config: false,
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_port => '9004',
      :libvirt__tunnel_local_port => '8004'
     # Arista config: enable eAPI and configure mgmt iface 
     arista.vm.provision 'shell', inline: <<-SHELL
sudo route add default gw `route -n | grep ma1 | cut -d ' ' -f 1 | cut -d '.' -f 1-3`.1 dev ma1
FastCli -p 15 -c "configure
ip name-server 8.8.8.8 8.8.4.4
username eapiuser privilege 15 role network-admin secret icanttellyou
management api http-commands
no shutdown
protocol https
copy running-config startup-config"
pip install pyeapi
SHELL
    end

end


