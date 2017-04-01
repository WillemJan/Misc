node 'default'  {
  if versioncmp($::puppetversion,'3.6.1') >= 0 {

      $allow_virtual_packages = hiera('allow_virtual_packages',false)

          Package {
                allow_virtual => $allow_virtual_packages,
                    }
    }
    include 'particle'
    include 'particle_packages'
    
    group {
       "aloha":
        ensure  => present
    }
   
    user { 'aloha':
        ensure     => present,
        uid        => '1020',
        groups     => 'aloha',
        password   => '$1$zPYWqpie$yHWe5ym/Q/vunMVWqigI0/',
        shell      => '/bin/bash',
        home       => '/home/aloha',
        managehome => true,
    }
    
    file { '/home/aloha/':
        ensure => 'directory',
        owner  => '1020', 
        group  => 'aloha',
        mode   => '0700',
    }
    
     
    file { '/home/aloha/.ssh/':
        ensure => 'directory',
        owner  => '1020', 
        group  => 'aloha',
        mode   => '0700',
    }
    
    file { "/home/aloha/.ssh/authorized_keys":
            ensure => "present",
            owner => "aloha",
            group => "aloha",
            mode => "600",
            source =>'puppet:///modules/particle/authorized_keys',
    }
  
    file_line { 'sudo_rule':
      ensure => present,
      path => '/etc/sudoers',
      line => 'aloha ALL=(ALL) NOPASSWD: ALL',
    }

    exec { "inst":
      command => "/usr/bin/dpkg --configure -a",
      refreshonly => true,
    }
    exec { "inst1":
      command => "/usr/bin/apt-get -y -f install",
      refreshonly => true,
    }
     
    exec { "dist-upgrade":
      command => "/usr/bin/apt-get -y --force-yes dist-upgrade",
      refreshonly => true,
    }

   exec { 'ufw-config':
        command => '/usr/sbin/ufw enable && /usr/sbin/ufw default deny incoming && /usr/sbin/ufw default allow outgoing && /usr/sbin/ufw allow from 127.0.0.0/24 && /usr/sbin/ufw allow from 10.0.0.254 to any port 22 proto tcp && /usr/sbin/ufw allow from 10.0.0.254 to any port 4949 proto tcp && /usr/sbin/ufw allow from 10.0.0.1/24 to any port 80 proto tcp && /usr/sbin/ufw allow from 10.0.0.1/24 to any port 8080 proto tcp',
   }

}
