# dawg-control
Control system for DAWG

## conf directory
Move `local.conf` into poky's `./build/conf/` directory after sourcing `oe-init-build-env` and before building yocto

### docker and qemu network setup
TODO: automate this

This is using https://github.com/jpetazzo/pipework and https://github.com/jpetazzo/pxe

Not included is starting up the pxe docker container and using pipework to give it eth1 interface with 192.168.1.1/24

```
LAUNCH THE DOCKER CONTAINER

ubuntu@ubuntu-VirtualBox:/workspace/poky/build$ docker run -ti --privileged -v /workspace/:/workspace qemu-kvm /bin/bash

GET THE NAME OF THE CONTAINER FOR INPUT TO THE PIPEWORK SCRIPT

ubuntu@ubuntu-VirtualBox:/workspace/qemu-docker$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
02885ebf9a3d        qemu-kvm            "/root/qemu/entrypoin"   6 seconds ago       Up 5 seconds                            tender_wozniak
84060cec8df2        pxe                 "/bin/sh -c 'echo Set"   2 hours ago         Up 2 hours                              sad_babbage

RUN PIPEWORK WITH THE NAME OF THE CONTAINER AND DESIRED IP

ubuntu@ubuntu-VirtualBox:/workspace/pipework$ sudo ./pipework br0 tender_wozniak 192.168.1.2/24

LOOK AT THE NEW INTERFACE IN THE CONTAINER

root@02885ebf9a3d:/# ifconfig
eth0      Link encap:Ethernet  HWaddr 02:42:ac:11:00:03
          inet addr:172.17.0.3  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:acff:fe11:3/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:26 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:4238 (4.2 KB)  TX bytes:648 (648.0 B)

eth1      Link encap:Ethernet  HWaddr f6:e8:a5:0c:47:ea
          inet addr:192.168.1.2  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::f4e8:a5ff:fe0c:47ea/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:26 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4317 (4.3 KB)  TX bytes:690 (690.0 B)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

CREATE THE TAP0 INTERFACE IN THE DOCKER CONTAINER

root@02885ebf9a3d:/# tunctl -t tap0
Set 'tap0' persistent and owned by uid 0

CREATE BR0 BRIDGE

root@02885ebf9a3d:/# brctl addbr br0
root@02885ebf9a3d:/# brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.000000000000    no

ADD ETH1 AND TAP0 TO BR0 BRIDGE

root@02885ebf9a3d:/# brctl addif br0 eth1
root@02885ebf9a3d:/# brctl addif br0 tap0
root@02885ebf9a3d:/# brctl show
bridge name    bridge id        STP enabled    interfaces
br0        8000.b6706cbb4116    no        eth1
                            tap0
LOOK AT THE INTERFACES AND ADDRESSES

root@02885ebf9a3d:/# ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: tap0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop master br0 state DOWN group default qlen 500
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
3: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
142: eth0@if143: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:3/64 scope link
       valid_lft forever preferred_lft forever
144: eth1@if145: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
    link/ether f6:e8:a5:0c:47:ea brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.2/24 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::f4e8:a5ff:fe0c:47ea/64 scope link
       valid_lft forever preferred_lft forever

MOVE THE IP FROM ETH1 TO BR0

root@02885ebf9a3d:/# ip addr flush dev eth1
root@02885ebf9a3d:/# ip addr add 192.168.1.2/24 dev br0
root@02885ebf9a3d:/# ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: tap0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop master br0 state DOWN group default qlen 500
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
3: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.2/24 scope global br0
       valid_lft forever preferred_lft forever
142: eth0@if143: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:3/64 scope link
       valid_lft forever preferred_lft forever
144: eth1@if145: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
    link/ether f6:e8:a5:0c:47:ea brd ff:ff:ff:ff:ff:ff

MAKE SURE ETH1 IS IN PROMISCUOUS MODE

root@02885ebf9a3d:/# ip link set eth1 up promisc on
root@02885ebf9a3d:/# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: tap0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop master br0 state DOWN mode DEFAULT group default qlen 500
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
142: eth0@if143: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
144: eth1@if145: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP mode DEFAULT group default qlen 1000
    link/ether f6:e8:a5:0c:47:ea brd ff:ff:ff:ff:ff:ff

SET BR0 INTERFACE UP

root@02885ebf9a3d:/# ip link set br0 up
root@02885ebf9a3d:/# ifconfig
br0       Link encap:Ethernet  HWaddr b6:70:6c:bb:41:16
          inet addr:192.168.1.2  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::b470:6cff:febb:4116/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:508 (508.0 B)

eth0      Link encap:Ethernet  HWaddr 02:42:ac:11:00:03
          inet addr:172.17.0.3  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:acff:fe11:3/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:229 errors:0 dropped:0 overruns:0 frame:0
          TX packets:131 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:165332 (165.3 KB)  TX bytes:7783 (7.7 KB)

eth1      Link encap:Ethernet  HWaddr f6:e8:a5:0c:47:ea
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:29 errors:0 dropped:0 overruns:0 frame:0
          TX packets:17 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4638 (4.6 KB)  TX bytes:1378 (1.3 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

SET TAP0 INTERFACE UP

root@02885ebf9a3d:/# ip link set tap0 up
root@02885ebf9a3d:/# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: tap0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast master br0 state DOWN mode DEFAULT group default qlen 500
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether b6:70:6c:bb:41:16 brd ff:ff:ff:ff:ff:ff
142: eth0@if143: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
144: eth1@if145: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP mode DEFAULT group default qlen 1000
    link/ether f6:e8:a5:0c:47:ea brd ff:ff:ff:ff:ff:ff

TEST PINGING THE DHCP SERVER ON BR0 INTERFACE

root@02885ebf9a3d:/# ping 192.168.1.1 -I br0
PING 192.168.1.1 (192.168.1.1) from 192.168.1.2 br0: 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.061 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=0.064 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=0.074 ms

RUN THE QEMU MACHINE WITH TAP0 FOR THE INTERFACE

root@02885ebf9a3d:/# /workspace/poky/build/tmp/sysroots/x86_64-linux/usr/bin/qemu-system-x86_64 -kernel /workspace/poky/build/tmp/deploy/images/qemux86-64/bzImage-qemux86-64.bin -net nic,model=virtio -net tap,vlan=0,ifname=tap0,script=no,downscript=no -cpu core2duo -drive file=/workspace/poky/build/tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64-20151225193227.rootfs.ext4,if=virtio,format=raw -show-cursor -usb -usbdevice wacom-tablet -no-reboot -vga none -serial stdio -m 256 --append 'vga=0 uvesafb.mode_option=640x480-32 root=/dev/vda rw mem=256M ip=192.168.1.3::192.168.1.1:255.255.255.0 oprofile.timer=1 rootfstype=ext4'
VNC server running on `::1:5900'

Poky (Yocto Project Reference Distro) 2.0 qemux86-64 /dev/ttyS0

qemux86-64 login: root

LOOK AT THE INTERFACES

root@qemux86-64:~# ifconfig
eth0      Link encap:Ethernet  HWaddr 52:54:00:12:34:56
          inet addr:192.168.1.3  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fe12:3456/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:7 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:578 (578.0 B)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

PING THE DHCP SERVER TO TEST CONNECTIVITY

root@qemux86-64:~# ping 192.168.1.1 -c 3
PING 192.168.1.1 (192.168.1.1): 56 data bytes
64 bytes from 192.168.1.1: seq=0 ttl=64 time=30.228 ms
64 bytes from 192.168.1.1: seq=1 ttl=64 time=12.424 ms
64 bytes from 192.168.1.1: seq=2 ttl=64 time=2.591 ms

--- 192.168.1.1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.591/15.081/30.228 ms

GET A DHCP LEASE FROM THE DHCP SERVER

root@qemux86-64:~# dhclient -v eth0
Internet Systems Consortium DHCP Client 4.3.2
Copyright 2004-2015 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/eth0/52:54:00:12:34:56
Sending on   LPF/eth0/52:54:00:12:34:56
Sending on   Socket/fallback
DHCPREQUEST on eth0 to 255.255.255.255 port 67
DHCPACK from 192.168.1.1
bound to 192.168.1.122 -- renewal in 1625 seconds.
root@qemux86-64:~# ifconfig
eth0      Link encap:Ethernet  HWaddr 52:54:00:12:34:56
          inet addr:192.168.1.3  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fe12:3456/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:7 errors:0 dropped:0 overruns:0 frame:0
          TX packets:14 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:762 (762.0 B)  TX bytes:1368 (1.3 KiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:49 (49.0 B)  TX bytes:49 (49.0 B)

TEST CONNECTIVITY TO THE OUTSIDE WORLD

root@qemux86-64:~# ping google.com -c 3
PING google.com (74.125.225.14): 56 data bytes
64 bytes from 74.125.225.14: seq=0 ttl=59 time=28.748 ms
64 bytes from 74.125.225.14: seq=1 ttl=59 time=28.528 ms
64 bytes from 74.125.225.14: seq=2 ttl=59 time=20.139 ms

--- google.com ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 20.139/25.805/28.748 ms
```
