- G++: `g++ shred-files.cpp -o shred-files -O2`
- MSVC:

    ```PowerShell
    cl.exe /EHsc /O2 /std:c++20 shred-files.cpp /Fe:shred-files.exe
    # /EHsc ISO-standard C++ exception handling
    ```
