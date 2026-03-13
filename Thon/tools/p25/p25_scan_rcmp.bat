@echo off
REM ============================================================
REM  P25 RCMP Scanner — Scans all known RCMP/public safety freqs
REM  Uses rtl_fm scanning mode with squelch
REM ============================================================
REM
REM  This scans across all known public safety frequencies
REM  and stops when it detects a signal (squelch break).
REM  The audio is piped to WSL dsdccx for P25 decoding.
REM
REM  Usage: just double-click or run from cmd
REM  Ctrl+C to stop
REM ============================================================

set RTL_SDR_DIR=E:\Thales\Thon\tools\rtl-sdr
REM If SDR# is using dongle 1, use dongle 0 for P25 (and vice versa)
set DEVICE_INDEX=0
set SAMPLE_RATE=48000
set GAIN=40
set SQUELCH=20

echo.
echo  P25 RCMP Scanner
echo  =================
echo  Scanning public safety frequencies with squelch...
echo  Will decode P25 when signal detected.
echo.
echo  Frequencies:
echo    155.475 MHz  RCMP Alberta VHF
echo    155.370 MHz  RCMP Mutual Aid
echo    154.280 MHz  Fire Mutual Aid AB
echo    155.340 MHz  EMS Alberta
echo    164.050 MHz  Alberta Forestry
echo    460.125 MHz  RCMP UHF
echo.
echo  Ctrl+C to stop.
echo.

REM rtl_fm scanning mode: -f freq -f freq -f freq ... with -l squelch
"%RTL_SDR_DIR%\rtl_fm.exe" -d %DEVICE_INDEX% -M fm -s %SAMPLE_RATE% -g %GAIN% -l %SQUELCH% -f 155475000 -f 155370000 -f 154280000 -f 155340000 -f 164050000 -f 460125000 - 2>nul | wsl -d kali-linux -- dsdccx -i - -o - -v 1
