# Procedure
1. Run the following: `wget https://cseweb.ucsd.edu/~calder/simpoint/releases/SimPoint.3.2.tar.gz`
2. Run `tar -xvzf SimPoint.3.2.tar.gz`
3. To avoid compiler errors, you will need to make a few changes
    - `#include <climits>` and `#include <cstring>` in `analysiscode/Utilities.h`
    - `#include <iostream>` in `analysiscode/Datapoint.h`
    - Replace every occurence of `Utilities::check(input,` in `analysiscode/Simpoint.cpp` with `Utilities::check(input.is_open()`
    - Replace every occurence of `Utilities::check(output,` in `analysiscode/Simpoint.cpp` with `Utilities::check(output.is_open()`
4. Run `cd SimPoint3.2 && make`
# Alternative Procedure
1. Use the SimPoint.3.2 directory in this directory
