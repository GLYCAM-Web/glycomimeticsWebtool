#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 frameInterval"
    echo "Exmpl: $0 50"
    exit 1
fi
interval=$1

if [ ! -d "simulation" ]; then
    echo "$0 must be run in a folder than contains the simulation/ folder"
    exit 1
fi
cd simulation/

if [[ ! -d "frames/summary" ]];then
    mkdir -p frames/summary
fi

for i in analog_* natural; do
    if [[ ! -d "frames/${i}" ]]; then
        mkdir frames/${i}
    fi

    rm -f frames/${i}/*
    rm -f frames_ligand/${i}/*

    prefix="frame_"
    path="frames/${i}/${prefix}"
echo "parm ${i}/1_leap/cocomplex_nowat_noion.prmtop
trajin ${i}/3_md/10.produ.nc 1 ${num_frames} ${interval}
autoimage
trajout ${path} pdb multi nobox
go
" > frames/cpptraj_writeframes.in

    cpptraj < frames/cpptraj_writeframes.in

    for j in $(ls ${path}*);do
        x=$(echo $j | sed "s/${prefix}.//")
        x+=".pdb"
        mv ${j} ${x}
    done
done
    
