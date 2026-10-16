#!/usr/bin/bash
# Generates the vendored crates tarball (Source1) for alacritty.spec.
# Usage: sources.sh <outdir> <spec>
# Expects Source0 to already be downloaded into <outdir> (spectool -g).

set -euo pipefail

outdir=$(realpath "$1")
spec=$2

command -v cargo >/dev/null || dnf -y install cargo

name=alacritty
version=$(rpmspec -q --srpm --queryformat '%{version}' "$spec")

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

tar -xzf "$outdir/$name-$version.tar.gz" -C "$work"
cd "$work/$name-$version"
cargo vendor --locked --versioned-dirs vendor >/dev/null
tar -cJf "$outdir/$name-$version-vendor.tar.xz" vendor/
