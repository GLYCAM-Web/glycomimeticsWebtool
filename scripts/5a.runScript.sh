#!/bin/bash

if [[ ! -d simulation || $# -ne 1 ]]; then
    echo "$0 must be called from the folder that contains simulation/"
    echo "Usage: $0 systemInfoFile"
    echo "Exmpl: $0 systeminfo.txt"
    echo "Exiting."
    exit 1
fi
systemInfo=$1
source $systemInfo # $installPath
cd simulation/

#Check that natural ligand exists
if [[ ! $(ls -d natural) ]]; then
    echo "Natural ligand folder was not generated in simulation/. Check for earlier errors. Exiting."
    exit 1
fi

#Check that analogs exist
if [[ ! $(ls -d analog_*) ]]; then
    echo "No analogs folders have been generated in simulation/. Check for earlier errors. Exiting."
    exit 1
fi

for dirname in $( ls -d analog_* ); 
do
    analog_name=$(echo ${dirname} | sed "s/analog_//")
    echo "Calling next step like this:"
    echo "$installPath/scripts/5b.setupRunTleap.sh $analog_name ../$systemInfo"
    $installPath/scripts/5b.setupRunTleap.sh $analog_name ../$systemInfo
done
#Now do natural:
$installPath/scripts/5b.setupRunTleap.sh natural ../$systemInfo

echo "$0 finished setting up and running tleap for each system."
