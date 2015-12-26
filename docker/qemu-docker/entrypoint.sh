#!/bin/bash
# Docker entrypoint that does runtime setup of the container environment for KVM,
# before running the user-specified command.

/root/qemu/kvm-mknod.sh
exec "$@"
