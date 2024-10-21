#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <station_name>"
    exit 1
fi

STATION_NAME=$(echo "$1" | jq -sRr @uri)

RESPONSE=$(curl -s "https://fahrtauskunft.avv-augsburg.de/efa/XML_STOPFINDER_REQUEST?avvStopFinderMacro=1&coordOutputFormat=WGS84%5Bdd.ddddd%5D&language=de&locationInfoActive=1&locationServerActive=1&name_sf=${STATION_NAME}&outputFormat=rapidJSON&serverInfo=1&sl3plusStopFinderMacro=dm&type_sf=any&version=10.5.17.3" \
    -H 'Cache-Control: no-cache')

if echo "$RESPONSE" | jq empty 2>/dev/null; then
    echo "$RESPONSE" | jq -r '.locations[] | select(.type == "stop") | "\(.name) = \(.id)"'
else
    echo "Error: Invalid response received from the server."
    exit 1
fi