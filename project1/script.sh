#!/bin/bash

#installing java

sudo apt-get update
sudo apt install openjdk-8-jdk-headless

#installing hadoop
cd ~
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz
tar -zxf hadoop-3.2.1.tar.gz
ln -s hadoop-3.2.1 hadoop


#changing the hadoop/etc/hadoop/hadoop-env.sh
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> hadoop/etc/hadoop/hadoop-env.sh

#cluster configuration
#modifying /etc/hosts/

sudo sed -i '1d' /etc/hosts
sudo sed -i '1s/^/10.254.4.24 vm1\n/' /etc/hosts
sudo sed -i '2s/^/10.254.3.112 vm2\n/' /etc/hosts
sudo sed -i '3s/^/10.254.3.240 vm3\n/' /etc/hosts