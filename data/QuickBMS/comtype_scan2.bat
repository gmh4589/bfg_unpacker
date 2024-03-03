@echo off
if [%1]==[] goto help
if [%2]==[] goto help
if [%3]==[] goto help

    FOR /L %%i IN (1,1,1000) DO (
       "data\QuickBMS\quickbms" -a "%%i %4" %1 %2 %3
    )
    goto end

:help
    echo .
    echo QuickBMS comtype scanner 2 (version 0.1.2)
    echo by Luigi Auriemma
    echo e-mail: aluigi@autistici.org
    echo web:    aluigi.org
    echo .
    echo you must specify:
    echo - the path of comtype2_scan.bms
    echo - the input file compressed with the unknown algorithm
    echo - the output folder where placing the unpacked files
    echo .
    echo example:
    echo   comtype_scan2 c:\comtype_scan2.bms c:\dump.dat c:\output_folder [max_size]
    echo .
    echo if an algorithm doesn't return immediately press CTRL-C
    echo and answer 'n' [no] when will be asked to "terminate batch job"
    echo .
:end
