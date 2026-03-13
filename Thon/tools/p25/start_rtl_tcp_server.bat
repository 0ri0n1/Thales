@echo off
REM ============================================================
REM  RTL-TCP Server — Serves RTL-SDR dongle 1 over TCP
REM  This makes dongle 1 available to Docker Kali for P25 decode
REM ============================================================
REM
REM  Dongle 0 = SDR# (aviation)
REM  Dongle 1 = P25 decode (this server)
REM
REM  Usage: just double-click this file, or run from cmd
REM  To stop: Ctrl+C or close the window
REM ============================================================

set RTL_SDR_DIR=E:\Thales\Thon\tools\rtl-sdr
REM If SDR# is using dongle 1, use dongle 0 for P25 (and vice versa)
set DEVICE_INDEX=0
set LISTEN_ADDR=0.0.0.0
set LISTEN_PORT=1234

echo.
echo  RTL-TCP Server for P25 Decoding
echo  ================================
echo  Serving dongle %DEVICE_INDEX% on %LISTEN_ADDR%:%LISTEN_PORT%
echo  Docker Kali can connect via host.docker.internal:%LISTEN_PORT%
echo.
echo  Press Ctrl+C to stop.
echo.

"%RTL_SDR_DIR%\rtl_tcp.exe" -d %DEVICE_INDEX% -a %LISTEN_ADDR% -p %LISTEN_PORT% -g 40 -s 240000
