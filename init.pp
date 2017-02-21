class particle_packages {
   $enhancers = [
    'pulseaudio',
    'pulseaudio-module-bluetooth',
    'pulseaudio-utils',
    'puppet',
    'puppet-common',
    'python-all',
    'python-all-dev',
    'python-apt',
    'python-apt-common',
    'python-audioread',
    'python-blinker',
    'python-bs4',
    'python-cairo',
    'python-cffi-backend',
    'python-chardet',
    'python-click',
    'python-colorama',
    'python-cryptography',
    'python-dateutil',
    'python-dev',
    'python-docutils',
    'python-empy',
    'python-enum34',
    'python-flask',
    'python-genmsg',
    'python-genpy',
    'python-gi',
    'python-glitch',
    'python-gobject',
    'python-gobject-2',
    'python-gpiozero',
    'python-gst0.10-dev',
    'python-gst-1.0',
    'python-gtk2',
    'python-gunicorn',
    'python-html5lib',
    'python-idna',
    'python-image-geometry',
    'python-insanity',
    'python-ipaddress',
    'python-itsdangerous',
    'python-jedi',
    'python-jinja2',
    'python-lxml',
    'python-magic',
    'python-markdown',
    'python-markupsafe',
    'python-minecraftpi',
    'python-minimal',
    'python-mpdclient',
    'python-nmap',
    'python-numpy',
    'python-opencv',
    'python-opencv-apps',
    'python-openssl',
    'python-picamera',
    'python-pifacecommon',
    'python-pifacedigitalio',
    'python-pigpio',
    'python-pil',
    'python-pip',
    'python-pip-whl',
    'python-pkg-resources',
    'python-pocketsphinx',
    'python-pyasn1',
    'python-pygame',
    'python-pygments',
    'python-pyinotify',
    'python-roman',
    'python-rpi.gpio',
    'python-rtimulib',
    'python-sense-hat',
    'python-serial',
    'python-setuptools',
    'python-simplejson',
    'python-six',
    'python-smbus',
    'python-sphinxbase',
    'python-spidev',
    'python-std-msgs',
    'python-support',
    'python-talloc',
    'python-tk',
    'python-werkzeug',
    'python-wheel',
    'python-xklavier',
    'python-yaml',
    'python-zmq',
]
    package { 
      $enhancers: ensure => 'present',
      install_options => ['--allow-unauthenticated', '-f', '-y'],
    }

   
   $dehancers = [
        'bootchart',
        'bootchart2',
        'lightdm',
        'exim4-base',
	    'exim4-config',
	    'exim4-daemon-light',
	    'plymouth',
        'libplymouth4:armhf',
        'libreoffice-common',
        'libreoffice-style-galaxy',
        'mountall',
   ]

    package { 
      $dehancers: ensure => 'absent',
      install_options => ['-f', '-y'],
    }

    file_line { 'sudo_rule_nopi':
      ensure => absent,
      path => '/etc/sudoers',
      line => 'pi ALL=(ALL) NOPASSWD: ALL',
    }
    
    file_line { 'no_stdpilogin':
      ensure => absent,
      path => '/etc/passwd',
      line => 'pi:x:1000:1000:,,,:/home/pi:/bin/bash',
    }
    
    file_line { 'no_stdpilogin1':
      ensure => present,
      path => '/etc/shadow',
      line => 'pi:x:1000:1000:,,,:/home/pi:/bin/false',
    }
    
    file_line { 'no_64m':
      ensure => absent,
      path => '/etc/memcached.conf',
      line => '-m 64',
    }

    file_line { 'swap':
      ensure => absent,
      path => '/etc/dphys-swapfile',
      line => 'CONF_SWAPSIZE=100',
    }

    file_line { 'swap1':
      ensure => present,
      path => '/etc/dphys-swapfile',
      line => 'CONF_SWAPSIZE=400',
    }

    file_line { 'yes_4m':
      ensure => present,
      path => '/etc/memcached.conf',
      line => '-m 4',
    }

    file_line { 'remotesyslog':
      ensure => present,
      path => '/etc/rsyslog.conf',
      line => '*.* @@10.0.0.254',
    }
}

