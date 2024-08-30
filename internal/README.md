# Installation

git clone -b webtoolOnlyBranch https://github.com/GLYCAM-Web/glycomimetics glycomimetics  
git clone -b glycomimeticsWebtool https://github.com/GLYCAM-Web/MD_Utils MD_Utils  
git clone -b feature_ChangesForFork https://github.com/GLYCAM-Web/gmml2 gmml2  

## gmml2
cd gmml2/  
./make.sh -j 24  
cd tests/  
GMML_ROOT_DIR=$(git rev-parse --show-toplevel)  
g++ -std=c++17 -I "${GMML_ROOT_DIR}" -L"${GMML_ROOT_DIR}"/bin/ -Wl,-rpath,"${GMML_ROOT_DIR}"/bin/ ../internalPrograms/glycomimeticPreprocessor/glycomimeticPreprocessor.cpp -lgmml2 -pthread -o gmPreProcessor.exe  
cd ../../  

## glycomimetics
cd glycomimetics/glycam_gaff_interfacing/  
source compile.sh  
cd ../src/  
source compile.sh  

