#!/bin/bash

if [[ ! -d simulation || $# -ne 1 ]]; then
    echo "$0 must be run in a folder that contains the simulation/ directory"
    echo "Usage: You must supply the location of MD_Utils Roe protocol folder"
    echo "Exmpl: $0 /programs/glycomimeticsWebtool/internal/MD_Utils/protocols/RoeProtocol/"
    echo "Exiting"
    exit 1
fi
mdProtocolDirectory=$1

#Now make simulation directories, one for each analog
cd simulation/
for folder in analog_* natural; do
    #Use this to run md of glycomimetic analogs
    mkdir $folder/3_md/
    cd $folder/3_md/
    #Copy the MD_Utils folder
    rsync -avL $mdProtocolDirectory .  # the L resolves symlinks.
    rsync -av ../1_leap/cocomplex.prmtop MdInput.parm7
    rsync -av ../1_leap/cocomplex.rst7 MdInput.rst7
    # Only write out solute, not solvent
    n=$(grep -c "^ATOM" ../1_leap/cocomplex_nowat_noion.pdb)
    sed -i "s/ntwprt = 0/ntwprt = $n/g" 10.produ.in
    # Job name
    sed -i "s/JOBNAME/$folder/g" submit.GPU.sh
    sed -i "s/JOBNAME/$folder/g" submit.CPU.sh
    # Hack: If we are not on harper, we need to disable the GPU
    if [[ $(hostname) == "harper" ]]; then
        sbatch --no-requeue submit.GPU.sh
    else
        # replace useCuda='Y' with useCuda='N' to disable GPU requirement
        # Note: This is a possible use case for overrides in Local_Run_Parameters.bash, but it wasn't simply working here.
        # cp Local_Run_Parameters.bash.example Local_Run_Parameters.bash
        sed -i "s/useCuda='Y'/useCuda='N'/g" Run_Parameters.bash
        # TODO: It should be possible to run the multi-part script directly and let it manage CPU/GPU resources instad.
        sbatch --no-requeue submit.CPU.sh
    fi
    cd ../../
done
echo "Finished $0. Ran from $PWD"
