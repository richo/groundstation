#!/bin/bash

# In your Vagrant file, add a shell provisioner, pointing to this file:
# config.vm.provision :shell, :path => "babushka.sh"

# Download and chmod the Babushka installer, if it's not already installed.
if ! which babushka >/dev/null ; then
  echo installing babushka
  wget -O - https://s3.amazonaws.com/99designs-babushka/bootstrap | bash
fi

echo installing docker
./groundstation/vagrant/docker.sh
