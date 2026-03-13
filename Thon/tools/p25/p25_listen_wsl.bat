@echo off
REM ============================================================
REM  P25 Live Listener (WSL Pipe) — Best real-time approach
REM  Pipes Windows rtl_fm.exe directly to WSL Kali dsdccx
REM ============================================================
REM
REM  PREREQUISITE: dsdcc must be installed in WSL Kali
REM    wsl -d kali-linux -- sudo apt install -y dsdcc
REM
REM  Usage: p25_listen_wsl.bat [frequency_mhz]
REM  Example: p25_listen_wsl.bat 155.475
REM
REM  RCMP Frequencies:
REM    155.475  RCMP Alberta VHF (may be encrypted)
REM    155.370  RCMP Mutual Aid (more likely analog)
REM    154.280  Fire Mutual Aid AB (best bet for analog)
REM    155.340  EMS Alberta (transitional)
REM    164.050  Alberta Forestry (wildfire ops, summer)
REM ============================================================

set RTL_SDR_DIR=E:\Thales\Thon\tools\rtl-sdr
REM If SDR# is using dongle 1, use dongle 0 for P25 (and vice versa)
set DEVICE_INDEX=0
set SAMPLE_RATE=48000
set GAIN=40

set FREQ_MHZ=%1
if "%FREQ_MHZ%"=="" set FREQ_MHZ=155.475

for /f %%i in ('powershell -Command "[int](%FREQ_MHZ% * 1000000)"') do set FREQ_HZ=%%i

echo.
echo  P25 Live Listener (WSL Pipe)
echo  ============================
echo  Frequency: %FREQ_MHZ% MHz (%FREQ_HZ% Hz)
echo  Dongle:    %DEVICE_INDEX%
echo.
echo  Pipeline: rtl_fm.exe -^> dsdccx (WSL Kali)
echo.
echo  If you hear digital noise instead of voice, the channel
echo  is likely encrypted. Try: 155.370 or 154.280
echo.
echo  Ctrl+C to stop.
echo.

"%RTL_SDR_DIR%\rtl_fm.exe" -d %DEVICE_INDEX% -f %FREQ_HZ% -M fm -s %SAMPLE_RATE% -g %GAIN% -l 20 -E dc - 2>nul | wsl -d kali-linux -- dsdccx -i - -o - -v 1
