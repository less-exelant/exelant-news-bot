<?php
/*
Plugin Name: My Python Plugin
Description: A plugin to run Python code via shortcode.
Version: 1.0
Author: Your Name
*/

function run_python_code() {
    $output = shell_exec('python3 /Users/alexadraposes/exelant-news-bot/news_bot.py');
    return $output;
}

add_shortcode('my_python_shortcode', 'run_python_code');
?>
