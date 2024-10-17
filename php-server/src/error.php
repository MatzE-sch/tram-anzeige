<?php
// Set the content type to application/json
header('Content-Type: application/json');

// Get the raw POST data
$rawData = file_get_contents('php://input');
error_log('raw: ' . $rawData);
$data = json_decode($rawData, true);

error_log('hi');
error_log('data:' . $data['error']);
// Check if the error key exists and is a string
if (isset($data['error']) && is_string($data['error'])) {
    // Log the error message to error.log
    $logFilePath = '/tmp/logs/error.log';
    error_log($data['error'] . PHP_EOL, 3, $logFilePath);
    // Ensure the directory and file have write permissions
    if (is_writable($logFilePath)) {
        error_log($data['error'] . PHP_EOL, 3, $logFilePath);
    } else {
        error_log('Log file is not writable: ' . $logFilePath);
    }
    // Send a success response
    echo json_encode(['status' => 'success']);
} else {
    // Send an error response
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid error message']);
}
?>
