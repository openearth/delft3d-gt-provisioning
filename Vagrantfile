# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "centos/7"

  # Keep box old now
  config.vm.box_check_update = false

  config.vm.define "django" do |django|

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    django.vm.network "forwarded_port", guest: 80, host: 8888
    django.vm.network "forwarded_port", guest: 8000, host: 8000

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    django.vm.network "private_network", ip: "10.0.1.2"

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    django.vm.synced_folder "../delft3d-gt-server", "/opt/delft3d-gt/delft3d-gt-server", type: "nfs", create: true
    django.vm.synced_folder "../delft3d-gt-ui", "/opt/delft3d-gt/delft3d-gt-ui", type: "nfs", create: true

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    django.vm.provider "virtualbox" do |vb|
       # Hide the VirtualBox GUI when booting the machine
       vb.gui = false
       vb.customize ["modifyvm", :id, "--ioapic", "on"]
       # Customize the amount of memory on the VM:
       vb.memory = "4096"
       vb.cpus = 2
       vb.name = "Delft3D GT Django"
    end

    # View the documentation for the provider you are using for more
    # information on available options.

    django.vm.provision "ansible" do |ansible|
      ansible.playbook = "site_local.yml"
      ansible.verbose = "vv"
      ansible.limit = "all"
      ansible.inventory_path = "inventory_local"
      ansible.extra_vars = {vagrant: true}
      ansible.tags = ['app', 'thredds', 'amazon']
    end
  end

  config.vm.define "nginx" do |nginx|

    nginx.vm.network "forwarded_port", guest: 80, host: 82
    nginx.vm.network "private_network", ip: "10.0.1.3"

    nginx.vm.provider "virtualbox" do |vb|
       vb.gui = false
       vb.customize ["modifyvm", :id, "--ioapic", "on"]
       vb.memory = "512"
       vb.cpus = 1
       vb.name = "Delft3D GT Nginx"
    end

    nginx.vm.provision "ansible" do |ansible|
      ansible.playbook = "site_local.yml"
      ansible.verbose = "vv"
      ansible.limit = "all"
      ansible.inventory_path = "inventory_local"
      ansible.extra_vars = {vagrant: true}
      ansible.tags = ['nginx']
    end
  end
end
