# Procedure
1. wget https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.22-98547-g7a303a835-gcc-linux.tar.gz
2. tar zxf pin-3.22-98547-g7a303a835-gcc-linux.tar.gz
3. cd pin-3.22-98547-g7a303a835-gcc-linux/source/tools
4. make
    - Needed to `sudo apt update && sudo apt upgrade && sudo apt install libc6-dev-i386 gcc-multilib libstdc++-8-dev:i386`
5. export PIN_ROOT=$(pwd) (inside pintool directory)
6. Go to champsim directory ("../../ReExclusive-refurbished/Champsims/BaseChampsim-Re-Exclusive/")
7. export CHAMPSIM_ROOT=$(pwd)