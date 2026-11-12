<?php
// Copy to ~/portfolio-contact/config.php, outside public_html.
// Keep this file private (0600). Never put a real password in the website archive.
return [
    'host' => 'smtp.gmail.com',
    'port' => 465,
    'encryption' => 'ssl',
    'username' => 'sender@example.com',
    'password' => '', // Google app password; not the Google account or FTP password.
    'from' => 'sender@example.com',
    'to' => 'recipient@example.com',
    'origin' => 'https://lawrencerailey.com',
];
