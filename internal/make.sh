#!/bin/bash
echo "Now building GWtools..."

## gmml2
cd gmml2/
./make.sh -j ${COMPILE_JOBS:-4}
cd tests/
GMML_ROOT_DIR=$(git rev-parse --show-toplevel)
g++ -std=c++17 -I "${GMML_ROOT_DIR}" -L"${GMML_ROOT_DIR}"/bin/ -Wl,-rpath,"${GMML_ROOT_DIR}"/bin/ ../internalPrograms/glycomimeticPreprocessor/glycomimeticPreprocessor.cpp -lgmml2 -pthread -o gmPreProcessor.exe  
cd ../../

## gmml
cd gmml/
./make.sh -j ${COMPILE_JOBS:-4}
cd ../
export GEMSHOME=$(pwd) # This is for the glycomimetics compilation below

## glycomimetics
cd glycomimetics/glycam_gaff_interfacing/
source compile.sh
cd ../src/
source compile.sh
cd ../validation
source compile.sh

echo "Finished building GWTools."
