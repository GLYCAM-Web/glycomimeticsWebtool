#!/bin/bash
echo "Now building GWtools with GEMSHOME:
$GEMSHOME"

echo "Compiling Oliver's preprocessor executables."
## gmml2
cd $GEMSHOME/gmml2/tests/
GMML_ROOT_DIR=$(git rev-parse --show-toplevel)
g++ -std=c++17 -I "${GMML_ROOT_DIR}" -L"${GMML_ROOT_DIR}"/bin/ -Wl,-rpath,"${GMML_ROOT_DIR}"/bin/ ../internalPrograms/glycomimeticPreprocessor/glycomimeticPreprocessor.cpp -lgmml2 -pthread -o gmPreProcessor.exe  
cd - # return whence was
mv $GEMSHOME/gmml2/tests/gmPreProcessor.exe .

echo "Copying necessary library files for Yao's executables"
mkdir -p gmml/dat/prep
cp -r $GEMSHOME/gmml/dat/CurrentParams gmml/dat/
cp -r $GEMSHOME/gmml/dat/prep/*.prep gmml/dat/prep/

echo "Compiling Yao's glycomimetic executables"
## glycomimetics
cd glycomimetics/glycam_gaff_interfacing/
source compile.sh
cd ../src/
source compile.sh
cd ../validation
source compile.sh
cd ../../
echo "Finished building GWTools."
