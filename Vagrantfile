Vagrant.configure(2) do |config|
  config.vm.box = "bento/centos-7.2"

  config.vm.define "zabbix" do |config|
    config.vm.hostname = "zabbix"
    config.vm.network "forwarded_port", guest: 80, host: 8888
    config.vm.network "private_network", ip: "192.168.33.10", virtualbox__intnet: "zabbix"

    config.vm.provision "shell", inline: <<-SHELL
      yum -y install epel-release
      yum -y install bash-completion vim-enhanced mailx nc rsync patch
      yum -y install ansible colordiff
    SHELL
  end

  config.vm.define "sv01" do |config|
    config.vm.hostname = "sv01"
    config.vm.network "private_network", ip: "192.168.33.11", virtualbox__intnet: "zabbix"
  end

  config.vm.define "sv02" do |config|
    config.vm.hostname = "sv02"
    config.vm.network "private_network", ip: "192.168.33.12", virtualbox__intnet: "zabbix"
  end

  config.vm.define "sv03" do |config|
    config.vm.hostname = "sv03"
    config.vm.network "private_network", ip: "192.168.33.13", virtualbox__intnet: "zabbix"
  end

  config.vm.provision "shell", inline: <<-SHELL
    yum -y install net-snmp net-snmp-utils net-snmp-perl
    cp -an /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.orig

    echo '
      rocommunity oreore default .1
      syslocation vagrant
      syscontact Ore <ore@example.com>
      proc crond
      disk /
      load 12
    ' | sed 's/ *//' | tee /etc/snmp/snmpd.conf

    systemctl enable snmpd
    systemctl start  snmpd
    systemctl status snmpd
  SHELL

  config.vm.provider :virtualbox do |v|
    v.linked_clone = true
  end
end
