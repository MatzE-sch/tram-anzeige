<?php
date_default_timezone_set('Europe/Berlin');

function time_to_now($time) {
    $gmt = new DateTimeZone('UTC');
    $cest = new DateTimeZone('Europe/Berlin');
    
    $time = DateTime::createFromFormat('Y-m-d\TH:i:s\Z', $time, $gmt);
    if ($time === false) {
        throw new Exception("Ungültiges Datumsformat: $time");
    }
    $time->setTimezone($cest);
    
    $now = new DateTime('now', $cest);

    if ($time < $now) {
        return intval(-($now->getTimestamp() - $time->getTimestamp()) / 60);
    } else {
        return intval(($time->getTimestamp() - $now->getTimestamp()) / 60);
    }
}

function get_departure_times($url) {
    $response = file_get_contents($url);
    if ($response === FALSE) {
        throw new Exception("Fehler beim Abrufen der Daten von der URL");
    }
    
    $data = json_decode($response, true);
    
    $departure = [];
    foreach ($data["stopEvents"] as $stopEvent) {
        echo '<pre>'; print_r($stopEvent["transportation"]["destination"]["name"]); echo '</pre>';
        echo '<pre>'; print_r($stopEvent["departureTimePlanned"]); echo '</pre>';

        if ($stopEvent["location"]['id'] == "de:09761:547:0:a") {
            $dest = "Haunstetten";
            $peron = "A";
        } else {
            $dest = "P&R Nord";
            $peron = "E";
        }

        if (isset($stopEvent["departureTimeEstimated"])) {
            $time = time_to_now($stopEvent["departureTimeEstimated"]);
        } else {
            $time = "N/A";
        }

        $departure[] = [
            /* old format 
            "plan" => time_to_now($data["journeys"][$i]["legs"][0]["origin"]["departureTimePlanned"]),
            "estimate" => time_to_now($data["journeys"][$i]["legs"][0]["origin"]["departureTimeEstimated"]),
            "base" => time_to_now($data["journeys"][$i]["legs"][0]["origin"]["departureTimeBaseTimetable"])
            */
            "destination" => $dest,
            "peron" => $peron,
            "plan" => time_to_now($stopEvent["departureTimePlanned"]),
            "estimated" => $time,


        ];
    }
    
    return $departure;
}

    // search for spocific destination
    //$url = "https://www.efa.de/efa/XML_TRIP_REQUEST2?itdTripDateTimeDepArr=dep&language=de&lineRestriction=400&locationServerActive=1&name_destination=de%3A09761%3A101&name_origin=de%3A09761%3A547&outputFormat=rapidJSON&type_destination=any&type_notVia=any&type_origin=any&type_via=any&useRealtime=1";
    //$url = $_GET['url'];
    //print($url);
/*
$url = "https://www.efa.de/efa/XML_DM_REQUEST?depSequence=10&depType=stopEvents&doNotSearchForStops=1&genMaps=0&imparedOptionsActive=1&inclMOT_1=true&inclMOT_10=true&inclMOT_11=true&inclMOT_13=true&inclMOT_14=true&inclMOT_15=true&inclMOT_16=true&inclMOT_17=true&inclMOT_18=true&inclMOT_19=true&inclMOT_2=true&inclMOT_3=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&inclMOT_8=true&inclMOT_9=true&includeCompleteStopSeq=1&includedMeans=checkbox&itOptionsActive=1&itdDateTimeDepArr=dep&language=de&locationServerActive=1&maxTimeLoop=1&mergeDep=1&mode=direct&name_dm=de%3A09761%3A547&outputFormat=rapidJSON&ptOptionsActive=1&serverInfo=1&sl3plusDMMacro=1&type_dm=any&useAllStops=1&useProxFootSearch=0&useRealtime=1&version=10.5.17.3"; */

// Die Daten werden von der AVV API abgerufen - hier gibts auch die Echtzeitdaten - bei anderen nicht!

// fischertor
// $url = "https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?calcOneDirection=1&coordOutputFormat=WGS84[dd.ddddd]&deleteAssignedStops_dm=1&depSequence=10&depType=stopEvents&doNotSearchForStops=1&genMaps=0&imparedOptionsActive=1&inclMOT_10=true&inclMOT_11=true&inclMOT_13=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&includeCompleteStopSeq=1&includedMeans=checkbox&itOptionsActive=1&itdDateTimeDepArr=dep&language=de&locationServerActive=1&maxTimeLoop=1&mode=direct&name_dm=de%3A09761%3A547&outputFormat=rapidJSON&ptOptionsActive=1&serverInfo=1&sl3plusDMMacro=1&type_dm=any&useAllStops=1&useProxFootSearch=0&useRealtime=1&version=10.5.17.3";
// wertachbrücke
$url = "https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?calcOneDirection=1&coordOutputFormat=WGS84[dd.ddddd]&deleteAssignedStops_dm=1&depSequence=10&depType=stopEvents&doNotSearchForStops=1&genMaps=0&imparedOptionsActive=1&inclMOT_10=true&inclMOT_11=true&inclMOT_13=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&includeCompleteStopSeq=1&includedMeans=checkbox&itOptionsActive=1&itdDateTimeDepArr=dep&language=de&locationServerActive=1&maxTimeLoop=1&mode=direct&name_dm=de%3A09761%3A407&outputFormat=rapidJSON&ptOptionsActive=1&serverInfo=1&sl3plusDMMacro=1&type_dm=any&useAllStops=1&useProxFootSearch=0&useRealtime=1&version=10.5.17.3";
try {
    $departure_times = get_departure_times($url);
    header('Content-Type: application/json');
    echo json_encode($departure_times);
} catch (Exception $e) {
    header('Content-Type: application/json', true, 500);
    echo json_encode(["error" => $e->getMessage()]);
}
?>