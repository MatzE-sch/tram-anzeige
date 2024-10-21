#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <station_name>"
    exit 1
fi

STATION_NAME=$(echo "$1" | jq -sRr @uri)

RESPONSE=$(curl -s "https://fahrtauskunft.avv-augsburg.de/efa/XML_STOPFINDER_REQUEST?avvStopFinderMacro=1&coordOutputFormat=WGS84%5Bdd.ddddd%5D&language=de&locationInfoActive=1&locationServerActive=1&name_sf=${STATION_NAME}&outputFormat=rapidJSON&serverInfo=1&sl3plusStopFinderMacro=dm&type_sf=any&version=10.5.17.3" \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.7,de-DE;q=0.3' \
    # -H 'Accept-Encoding: gzip, deflate, br, zstd' \
    -H 'Referer: https://fahrtauskunft.avv-augsburg.de/sl3+/departureMonitor?lng=de' \
    -H 'Connection: keep-alive' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Priority: u=4' \
    -H 'Pragma: no-cache' \
    -H 'Cache-Control: no-cache')

if echo "$RESPONSE" | jq empty 2>/dev/null; then
    echo "$RESPONSE" | jq -r '.locations[] | select(.type == "stop") | "\(.name) = \(.id)"'
else
    echo "Error: Invalid response received from the server."
    exit 1
fi