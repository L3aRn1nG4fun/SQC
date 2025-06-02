@echo off
setlocal EnableDelayedExpansion

:: Get current date
for /f "tokens=1-3 delims=/.- " %%a in ("%date%") do (
    set d1=%%a
    set d2=%%b
    set d3=%%c
)

:: Auto-detect format (YYYY/MM/DD or DD/MM/YYYY, etc.)
if %d1% GEQ 2020 (
    set year=%d1%
    set month=%d2%
    set day=%d3%
) else if %d3% GEQ 2020 (
    set day=%d1%
    set month=%d2%
    set year=%d3%
) else (
    set day=%d2%
    set month=%d1%
    set year=%d3%
)

:: Trim year to 2 digits
set year2=%year:~-2%

:: Get weekday (0 = Sunday ... 6 = Saturday)
for /f "skip=1" %%i in ('wmic path win32_localtime get dayofweek') do (
    set dow=%%i
    goto :gotdow
)
:gotdow

:: Convert 0 (Sunday) to 7
if "%dow%"=="0" (
    set weekday=7
) else (
    set /a weekday=%dow%
)

:: Clean leading zeros safely
set /a dayClean=10%day% %% 100
set /a yearClean=10%year2% %% 100

:: Calculate sum
set /a sum=dayClean + weekday + yearClean

:: Call reverse function
call :reverse !sum!

:: Print expected passcode
echo [INFO] Today's expected passcode is: !reversed!

:: Prompt for input
set /p usercode=Enter passcode: 

:: Check
if "%usercode%"=="!reversed!" (
    echo Access granted.
    :: Prompt for API Key
    set /p API_KEY="Enter the API Key: "

    :: Prompt for Tenant URL
    set /p TENANT_URL="Enter the Tenant URL (without https://): "

    :: Run the command with the provided API Key and Tenant URL
    hcp-feature-util-2.1.0\hcp-feature-util -k %API_KEY% -a %TENANT_URL% -f KmIwsServicePlatformEmbedded=true
) else (
    echo Access denied.
)

pause
exit /b

:: ----------------------------
:: Reverse function
:reverse
setlocal EnableDelayedExpansion
set "str=%~1"
set "rev="
:loop
if defined str (
    set "last=!str:~-1!"
    set "rev=!rev!!last!"
    set "str=!str:~0,-1!"
    goto loop
)
endlocal & set "reversed=%rev%"
exit /b

    
:: End the script
endlocal
