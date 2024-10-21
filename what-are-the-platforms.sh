#!/bin/bash

# prompt:
# write a .sh skript that takes asks https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?calcOneDirection=1&coordOutputFormat=WGS84%5Bdd.ddddd%5D&deleteAssignedStops_dm=1&depSequence=30&depType=stopEvents&doNotSearchForStops=1&genMaps=0&imparedOptionsActive=1&inclMOT_10=true&inclMOT_11=true&inclMOT_13=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&includeCompleteStopSeq=1&includedMeans=checkbox&itOptionsActive=1&itdDateTimeDepArr=dep&language=de&locationServerActive=1&maxTimeLoop=1&mode=direct&name_dm=de%3A09761%3A407&outputFormat=rapidJSON&ptOptionsActive=1&serverInfo=1&sl3plusDMMacro=1&type_dm=any&useAllStops=1&useProxFootSearch=0&useRealtime=1&version=10.5.17.3

# its result looks like this:

# serverInfo {…} version "10.5.17.3" systemMessages [] locations 0 id "de:09761:407" isGlobalId true name "Augsburg, Wertachbrücke" disassembledName "Wertachbrücke" coord […] type "stop" matchQuality 100000 isBest true parent {…} assignedStops […] properties {…} stopEvents 0 location id "de:09761:407:0:a" isGlobalId true name "Augsburg, Wertachbrücke" disassembledName "Bstg. a" type "platform" pointType "PLATFORM" coord […] properties {…} parent {…} departureTimePlanned "2024-10-21T02:40:00Z" departureTimeBaseTimetable "2024-10-21T02:40:00Z" transportation id "avg:03004: :R:j24" name "Straßenbahn 4" number "4" product {…} destination id "2000422" name "Oberhausen, Nord P+R" type "stop" properties tripCode 411 lineDisplay "LINE" origin id "80000589" name "Augsburg Hbf" type "stop" infos […] previousLocations […] onwardLocations […] properties AVMSTripID "28986-00092-1" 1 {…} 2 {…}

# and prints following:

# the stop name
# the stop id
# all the line names and numbers
# all the platforms where the lines depart

# URL to fetch data from
URL="https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?calcOneDirection=1&coordOutputFormat=WGS84%5Bdd.ddddd%5D&deleteAssignedStops_dm=1&depSequence=30&depType=stopEvents&doNotSearchForStops=1&genMaps=0&imparedOptionsActive=1&inclMOT_10=true&inclMOT_11=true&inclMOT_13=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&includeCompleteStopSeq=1&includedMeans=checkbox&itOptionsActive=1&itdDateTimeDepArr=dep&language=de&locationServerActive=1&maxTimeLoop=1&mode=direct&name_dm=de%3A09761%3A407&outputFormat=rapidJSON&ptOptionsActive=1&serverInfo=1&sl3plusDMMacro=1&type_dm=any&useAllStops=1&useProxFootSearch=0&useRealtime=1&version=10.5.17.3"

# Fetch the data
response=$(curl -s "$URL")

# Extract and print the stop name
stop_name=$(echo "$response" | jq -r '.locations[0].name')
echo "Stop Name: $stop_name"

# Extract and print the stop id
stop_id=$(echo "$response" | jq -r '.locations[0].id')
echo "Stop ID: $stop_id"

# Extract and print all the line names and numbers
echo "Lines:"
echo "$response" | jq -r '.stopEvents[] | "\(.transportation.name) \(.transportation.number)"'

# Extract and print all the platforms where the lines depart
echo "Platforms:"
echo "$response" | jq -r '.stopEvents[] | .location.disassembledName'