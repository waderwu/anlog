<?php
define("logdir", "/tmp/".$_GET['dir']."/");

$list = scandir(logdir);
$ret = array();

foreach($list as $file)
{
    if (($file !== ".") && ($file !== ".."))
    {
        $ret[$file] = file_get_contents(logdir.$file);
        unlink(logdir.$file);
    }
}

echo json_encode($ret);
