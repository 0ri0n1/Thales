@echo off
REM ============================================================
REM  P25 Capture (Windows) — Records FM-demodulated audio
REM  Then decodes P25 in Docker Kali
REM ============================================================
REM
REM  This captures raw FM audio from dongle 1 to a file,
REM  then copies it to Docker Kali for P25 decoding.
REM
REM  Usage: p25_capture_windows.bat [frequency_mhz] [seconds]
REM  Example: p25_capture_windows.bat 155.475 60
REM ============================================================

set RTL_SDR_DIR=E:\Thales\Thon\tools\rtl-sdr
set P25_DIR=E:\Thales\Thon\tools\p25
set OUTPUT_DIR=E:\Thales\Thon\output\sdr\p25_captures
REM If SDR# is using dongle 1, use dongle 0 for P25 (and vice versa)
set DEVICE_INDEX=0
set SAMPLE_RATE=48000
set GAIN=40

REM Default frequency and duration
set FREQ_MHZ=%1
set DURATION=%2
if "%FREQ_MHZ%"=="" set FREQ_MHZ=155.475
if "%DURATION%"=="" set DURATION=60

REM Convert MHz to Hz (batch can't do floating point, use PowerShell)
for /f %%i in ('powershell -Command "[int](%FREQ_MHZ% * 1000000)"') do set FREQ_HZ=%%i

REM Timestamp for filename
for /f %%i in ('powershell -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TIMESTAMP=%%i

set OUTFILE=%OUTPUT_DIR%\p25_capture_%FREQ_MHZ%MHz_%TIMESTAMP%.raw

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo.
echo  P25 Capture (Windows)
echo  =====================
echo  Frequency: %FREQ_MHZ% MHz (%FREQ_HZ% Hz)
echo  Duration:  %DURATION% seconds
echo  Dongle:    %DEVICE_INDEX%
echo  Output:    %OUTFILE%
echo.
echo  Recording for %DURATION% seconds...
echo.

REM Capture FM-demodulated audio from dongle 1
REM -t flag: negative value = exit after squelch timeout, positive = exit after N squelch events
REM Using timeout command to limit duration
start /b "" "%RTL_SDR_DIR%\rtl_fm.exe" -d %DEVICE_INDEX% -f %FREQ_HZ% -M fm -s %SAMPLE_RATE% -g %GAIN% -l 0 "%OUTFILE%"

timeout /t %DURATION% /nobreak >nul

REM Kill rtl_fm
taskkill /f /im rtl_fm.exe >nul 2>&1

echo.
echo  [*] Capture complete: %OUTFILE%
echo.

REM Check if file has data
for %%A in ("%OUTFILE%") do set FILESIZE=%%~zA
if "%FILESIZE%"=="0" (
    echo  [!] Warning: capture file is empty. Check dongle connection.
    goto :end
)
echo  [*] Captured %FILESIZE% bytes

echo.
echo  [*] Copying to Docker Kali for P25 decoding...
docker cp "%OUTFILE%" kali-mcp-pentest:/root/data/

echo.
echo  [*] Decoding P25...
docker exec kali-mcp-pentest bash -c "dsdccx -i /root/data/p25_capture_%FREQ_MHZ%MHz_%TIMESTAMP%.raw -o /root/data/p25_decoded_%FREQ_MHZ%MHz_%TIMESTAMP%.raw -v 1 2>&1 | tail -20"

echo.
echo  [*] Done. Decoded audio at:
echo      Docker: /root/data/p25_decoded_%FREQ_MHZ%MHz_%TIMESTAMP%.raw
echo.
echo  To play the decoded audio:
echo    docker exec kali-mcp-pentest aplay -r 8000 -f S16_LE -t raw -c 1 /root/data/p25_decoded_%FREQ_MHZ%MHz_%TIMESTAMP%.raw
echo.

:end
pause
