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
        return intval(-($now->getTimestamp() - $time->getTimestamp()));
    } else {
        return intval(($time->getTimestamp() - $now->getTimestamp())); 
    }
}

function get_departure_times($url) {
    $response = file_get_contents($url);
    // print($response);
    if ($response === FALSE) {
        throw new Exception("Fehler beim Abrufen der Daten von der URL");
    }
    // echo $response;
    $data = json_decode($response, true);
    // error_log('data');  
    // file_put_contents('logfile.log', json_encode($data, JSON_PRETTY_PRINT), FILE_APPEND);
    $departure = [];
    foreach ($data["stopEvents"] as $stopEvent) {
        // TODO: validate???
        if (isset($stopEvent["isCancelled"]) && $stopEvent["isCancelled"] === true) {
            continue;
        }
        // echo '<pre>'; print_r($stopEvent["transportation"]["destination"]["name"]); echo '</pre>';
        // echo '<pre>'; print_r($stopEvent["departureTimePlanned"]); echo '</pre>';
        $bahnsteig = $stopEvent["location"]["properties"]["platform"];
        $lineNumber = $stopEvent["transportation"]["number"];
        $destination = $stopEvent["transportation"]["destination"]["name"];
        // destination:
        // Augsburg Hbf
        // Oberhausen, Nord P+R
        // Augsburg, Josefinum
        // Haunstetten, Nord
        // ?? Rotes tor ??
        

        // echo '<pre>'; print_r($stopEvent); echo '</pre>';
        if (isset($stopEvent["departureTimeEstimated"])) {
            $time = time_to_now($stopEvent["departureTimeEstimated"]);
        } else {
            $time = time_to_now($stopEvent["departureTimePlanned"]);
        }
        
        $max_time_in_future = 30*60; // 30 minutes
        if ($time > $max_time_in_future) { 
            continue;
        }
        $departure[] = [
            "destination" => $destination,
            "bahnsteig" => $bahnsteig,
            "lineNumber" => $lineNumber,
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

// src: https://fahrtauskunft.avv-augsburg.de/sl3+/departureMonitor?formik=mtcb0%3Dfalse%26mtcb10%3Dfalse%26mtcb11%3Dfalse%26mtcb5%3Dfalse%26mtcb6%3Dfalse%26mtcb7%3Dfalse%26origin%3Dde%253A09761%253A407&lng=de
// fischertor
// $url = "https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?calcOneDirection=1&coordOutputFormat=WGS84[dd.ddddd]&deleteAssignedStops_dm=1&depSequence=10&depType=stopEvents&doNotSearchForStops=1&genMaps=0&imparedOptionsActive=1&inclMOT_10=true&inclMOT_11=true&inclMOT_13=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&includeCompleteStopSeq=1&includedMeans=checkbox&itOptionsActive=1&itdDateTimeDepArr=dep&language=de&locationServerActive=1&maxTimeLoop=1&mode=direct&name_dm=de%3A09761%3A547&outputFormat=rapidJSON&ptOptionsActive=1&serverInfo=1&sl3plusDMMacro=1&type_dm=any&useAllStops=1&useProxFootSearch=0&useRealtime=1&version=10.5.17.3";
// fischertor 'de:09761:547' de%3A09761%3A547
// wertachbrücke 'de:09761:407'

if (isset($_GET['stop_id'])) {
    $stop_id = $_GET['stop_id'];
} else {
    $stop_id = 'de:09761:407';
}

// $url = "https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?outputFormat=rapidJSON&name_dm=de%3A09761%3A407&itdDateTimeDepArr=dep&mode=direct&useRealtime=1&deleteAssignedStops_dm=1&depSequence=10&calcOneDirection=1&ptOptionsActive=1&language=de&type_dm=any&useAllStops=1&inclMOT_5=true&maxTimeLoop=1&limit=10";
// Construct the URL with query parameters for the API request
$url = "https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?" . http_build_query([
    'outputFormat' => 'rapidJSON',          // The format of the output data
    'name_dm' => $stop_id,                  // The stop ID for the departure monitor
    'itdDateTimeDepArr' => 'dep',           // Specifies departure time
    'mode' => 'direct',                     // Direct mode for the request
    'useRealtime' => '1',                   // Use real-time data
    'deleteAssignedStops_dm' => '1',        // Delete assigned stops in departure monitor
    'depSequence' => '10',                  // Number of departures to retrieve
    'calcOneDirection' => '1',              // Calculate in one direction
    'ptOptionsActive' => '1',               // Public transport options active
    'language' => 'de',                     // Language of the response
    'type_dm' => 'any',                     // Type of departure monitor
    'useAllStops' => '1',                   // Use all stops
    'inclMOT_5' => 'true',                  // Include mode of transport 5 (e.g., tram)
    'maxTimeLoop' => '1',                   // Maximum time loop
    'limit' => '20'                         // Limit the number of timeloops?
]);

error_log($url);
try {
    $departure_times = get_departure_times($url);
    header('Content-Type: application/json');
    echo json_encode($departure_times);
    error_log(json_encode($departure_times));
} catch (Exception $e) {
    header('Content-Type: application/json', true, 500);
    echo json_encode(["error" => $e->getMessage()]);
}
?>