# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.network "forwarded_port", guest: 80, host: 80
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.network "forwarded_port", guest: 5432, host: 5432
    config.vm.provider "virtualbox" do |vb|
        vb.memory = "6096" #adjust this based on your dev laptop memory capacity
    end
    config.vm.provision "shell" do |local|
        local.inline = $LocalScript
    end
    config.vm.synced_folder '.', '/vagrant', disabled: true # disable default rsync to avoid confusion when searching the server.
    #config.vm.synced_folder "./twitter", "/usr/local/lib/python2.7/dist-packages/geonode/twitter" # enable this to allow rsync to deploy to your virtualbox (good for local dev)
end


# Main Provisioning Shell Script
$LocalScript = <<SCRIPT
    set -x # Print commands and their arguments as they are executed.
    exec > >(tee -i logfileLocal.txt) #Log all the Vagrant commands here
    exec 2>&1
    echo starting LocalScript
    date

    sudo add-apt-repository -y ppa:geonode/snapshots
    sudo apt-get update
    sudo apt-get install geonode -y
    geonode createsuperuser --username=admin --email=webservices@admin.com --noinput #this needs a password later
    sudo geonode-updateip 127.0.0.1
    geonode syncdb
    geonode collectstatic --noinput
    sudo service apache2 restart
    sudo chmod 777 -R /etc/geonode /usr/local/lib/python2.7/dist-packages/geonode/settings.py /usr/local/lib/python2.7/dist-packages/geonode/urls.py /var/log/apache2

    echo finishing LocalScript >&2
SCRIPT