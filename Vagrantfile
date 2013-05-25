# -*- mode: ruby -*-
# vi: set ft=ruby :

BOX_NAME = ENV['BOX_NAME'] || "precise64"
BOX_URI = ENV['BOX_URI'] || "http://files.vagrantup.com/precise64.box"

# all versions of Vagrant run this
Vagrant::Config.run do |config|
  config.vm.box = BOX_NAME
  config.vm.box_url = BOX_URI
  config.vm.provision :shell, :path => "vagrant/bootstrap.sh"
  config.ssh.forward_agent = true

  # Vagrant 1.0.x config
  if Vagrant::VERSION < "1.1.0"
    config.vm.network :hostonly, "192.168.33.10"

    config.vm.share_folder("groundstation", "~/groundstation", File.dirname(__FILE__), :nfs=>true)
  end
end

# Vagrant 1.1.x config
Vagrant::VERSION >= "1.1.0" and Vagrant.configure("2") do |config|
  config.vm.network :private_network, ip: "192.168.33.10"

  config.vm.synced_folder(File.dirname(__FILE__), "/home/vagrant/groundstation")

  config.vm.provider :virtualbox do |vb|
    config.vm.box = BOX_NAME
    config.vm.box_url = BOX_URI

    vb.customize ["modifyvm", :id, "--memory", 1024]
    vb.customize ["modifyvm", :id, "--cpus", 2]
  end
end
