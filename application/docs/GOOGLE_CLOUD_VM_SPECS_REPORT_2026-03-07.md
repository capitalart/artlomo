# Google Cloud VM Specs Report

**Report Date:** 2026-03-07
**Collection Method:** Live OS inspection plus Google metadata service queries
**Host:** `ezy`

## Executive Summary

This VM is a Google Compute Engine instance running Debian 12 on an AMD Milan platform, sized for general-purpose workload execution with 4 vCPUs, 15 GiB RAM, and a 128 GB persistent disk.

## Compute Instance Identity

- Instance name: `ezy`.

- Instance hostname (metadata): `ezy.v2`.

- Instance ID: `4846096579077552789`.

- Project ID: `ezy-empire`.

- Project number: `609268697830`.

- Zone: `australia-southeast2-b`.

- Region: `australia-southeast2`.

- Virtualization detection: `google`.

- Hypervisor: KVM (full virtualization).

## Machine Type and CPU Platform

- Machine type (metadata path): `n2d-standard-4`.

- CPU platform: `AMD Milan`.

- CPU model (guest view): `AMD EPYC 7B13`.

- Architecture: `x86_64`.

- vCPU count: `4`.

- Topology (guest): 1 socket, 2 cores, 2 threads per core.

## Memory

- Total memory: `15 GiB`.

- Used at collection time: `3.8 GiB`.

- Free at collection time: `10 GiB`.

- Available at collection time: `11 GiB`.

- Swap: `0 B` configured.

## Disk and Filesystem

- Boot disk device: `sda`.

- Disk type/model (guest-visible): `PersistentDisk`.

- Disk size: `128 GB`.

- Root partition: `/dev/sda1` (ext4), mounted on `/`.

- EFI partition: `/dev/sda15` (vfat), mounted on `/boot/efi`.

Filesystem usage at collection time:

- `/` total: `126G`.

- `/` used: `42G`.

- `/` available: `79G`.

- `/` utilization: `35%`.

## Network Configuration

- Primary interface: `ens4`.

- Internal IP: `10.192.0.2/32`.

- Default gateway: `10.192.0.1`.

- Metadata route: `169.254.169.254` via `10.192.0.1`.

DNS configuration:

- Resolver endpoint: `169.254.169.254`.

- Search domain includes Google internal domains for project and zone scope.

## Scheduling and Availability Settings (GCE Metadata)

- Automatic restart: `TRUE`.

- Preemptible: `FALSE`.

- On-host maintenance behavior: `MIGRATE`.

This indicates a standard non-preemptible VM configured for restart and live migration behavior.

## Network Tags and Service Accounts

Network tags:

- `http-server`.

- `https-server`.

- `lb-health-check`.

Service accounts exposed in metadata:

- `609268697830-compute@developer.gserviceaccount.com/`.

- `default/`.

## Instance Attributes

Metadata instance attributes present:

- `enable-osconfig`.

- `ssh-keys`.

## OS and Kernel Details

- OS: Debian GNU/Linux 12 (bookworm).

- Kernel: `6.1.0-43-cloud-amd64`.

- Uptime at collection time: ~36 minutes.

- Load average at collection time: `0.00, 0.07, 0.10`.

## Security-Related CPU Notes (Guest-Reported)

The guest reports mitigations or non-affected status for major speculative execution and CPU vulnerability classes, with no immediate anomalies observed in `lscpu` output.

## Optional Additions for a Deeper Cloud Audit

If needed, a follow-up report can include:

- Attached disk type details from GCP API.

- VPC, subnet, and firewall policy objects from project configuration.

- External IP status and NAT details.

- IAM role bindings for the instance service account.

- Monitoring and logging sink configuration.

## Conclusion

The VM is a healthy, non-preemptible Google Compute Engine instance in `australia-southeast2-b`, sized as `n2d-standard-4` with 4 vCPUs, 15 GiB RAM, and 128 GB persistent storage.

It is suitable for the current ArtLomo workload profile and currently shows stable resource usage with substantial memory and disk headroom.
