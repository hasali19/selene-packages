#!/usr/bin/bash
# Generates the vendored crates tarball (Source1) and the cargo source
# replacement config (Source2) for niri.spec.
# Usage: sources.sh <outdir> <spec>
# Expects Source0 to already be downloaded into <outdir> (spectool -g).

set -euo pipefail

outdir=$(realpath "$1")
spec=$2

command -v cargo >/dev/null || dnf -y install cargo

name=niri
commit=$(sed -n 's/^%global commit \+\([0-9a-f]\{40\}\)$/\1/p' "$spec")

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

tar -xzf "$outdir/$name-$commit.tar.gz" -C "$work"
cd "$work/$name-$commit"
cargo vendor --locked --versioned-dirs vendor > "$outdir/vendor.toml"
tar -cJf "$outdir/$name-$commit-vendor.tar.xz" vendor/
