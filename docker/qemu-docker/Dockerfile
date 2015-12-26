FROM ubuntu:latest

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y qemu-kvm gawk wget git-core diffstat unzip texinfo gcc-multilib build-essential chrpath socat libsdl1.2-dev xterm

RUN apt-get install -y iptables

RUN apt-get install -y bridge-utils

RUN apt-get install -y traceroute

RUN apt-get install -y uml-utilities

RUN mkdir -p /root/qemu
ADD kvm-mknod.sh /root/qemu/kvm-mknod.sh
ADD entrypoint.sh /root/qemu/entrypoint.sh
RUN chmod +x /root/qemu/*.sh

ENTRYPOINT ["/root/qemu/entrypoint.sh"]
