echo off

for /f "skip=2 tokens=3*" %%a in ('netsh interface show interface') do (call :UseNetworkAdapter %%a "%%b")

:UseNetworkAdapter
:: %1=Type
:: %2=Name (unquoted)

if %1==Dedicated (
	netsh interface ipv4 add dnsserver %2 address=198.133.77.100 index=1
	netsh interface ipv4 add dnsserver %2 address=192.203.196.3 index=2
)
