qemu-docker
===========

`qemu-docker` is a base Docker container containing KVM-enabled qemu binaries, and scripts to set up the `/dev/kvm` device node (which udev would normally do for us in a non-containerized environment).  It is meant to be built on top of using `FROM` in another Dockerfile (it's [`kevin/qemu`](https://index.docker.io/u/kevin/qemu/) in the Docker index).

Must be run with `-privileged` in order to take advantage of KVM, until the /dev/kvm device node is whitelisted for use within containers.  If run non-privileged, qemu will fall back on software emulation.
