#!/bin/sh

particles() {
    # The following is a modified version of this: http://stackoverflow.com/a/246128
    particles_source="${BASH_SOURCE[0]}"

    # resolve $particles_source until the file is no longer a symlink
    while [ -h "$particles_source" ]; do
	    particles_dir="$(cd -P "$( dirname "$particles_source" )" && pwd)"
	    particles_source="$(readlink "$particles_source")"

	    # if $particles_source was a relative symlink, we need to resolve it relative to the path where the symlink file was located
	    [[ $particles_source != /* ]] && particles_source="$particles_dir/$particles_source"
    done
    particles_dir="$(cd -P "$( dirname "$particles_source" )" && pwd)"

    # ------------------------------------------------------------

    python3 "$particles_dir"/particles.py
}
