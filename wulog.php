<?php

$config = array(
    #level 1 just log requests
    #level 2 log requests and response and check flag in response
    #level 3 Intercept requests waf 1
    #level 4 Intercept requests waf 2
    #level 5 return static pages
    #level 6 except ip in ipwhite, others will intercept
    "level" => 5,
    "ipwhite" => ['127.0.0.1'],
    "ipblack" => ['172.91.0.137', '172.91.0.29', '172.91.0.76', '172.91.0.109']
);

header("ip:".$_SERVER['REMOTE_ADDR']);

class Log
{
    private $path, $method, $headers, $data, $get, $ip, $time, $response, $log;
    function __construct($config)
    {
        $this->config = $config;

        $this->req = "/tmp/req/";
        $this->res = "/tmp/res/";
        $this->ip = $_SERVER["REMOTE_ADDR"];

        if (!in_array($this->ip, $this->config['ipwhite']))
        {
            $this->start();
        }


    }

    function start()
    {
        $this->path =$_SERVER['PHP_SELF'];
        $this->method = $_SERVER['REQUEST_METHOD'];
        $this->headers = $this->get_headers();
        $this->post = $_POST;
        $this->get = $_GET;
        $this->time = date('Y-m-d H:i:s',time());
        $this->filename = $this->gen_randstr().date('H_i_s',time());
        $this->attack = false;
        $this->file = $this->get_file();
        $this->log = array();
        $this->log['uid'] = md5($this->filename);
        $this->log['path'] = $this->path;
        $this->log['method'] = $this->method;
        $this->log['headers'] = $this->headers;
        $this->log['post'] = $this->post;
        $this->log['get'] = $this->get;
        $this->log['ip'] = $this->ip;
        $this->log['time'] = $this->time;
        $this->log['file'] = $this->file;

        if (!is_dir($this->req))
        {
            mkdir($this->req,0755);
        }

        if (!is_dir($this->res))
        {
            mkdir($this->res,0755);
        }

        $logjson = json_encode($this->log);
        file_put_contents($this->req.$this->filename, $logjson, FILE_APPEND);


        if ($this->config['level'] > 4)
        {
            if (in_array($this->ip, $this->config['ipblack']))
            {
                $this->mydie();
            }

        }

        if ($this->config['level'] > 5)
        {
            if (!in_array($this->ip, $this->config['ipwhite']))
            {
                $this->mydie();
            }

        }


        if ($this->config['level'] > 1)
        {
            ob_start(array($this,"get_response"));
        }




    }

    function gen_randstr()
    {
        $s = "";
        for($i=0; $i<32; $i++)
        {
            $s .=chr(rand(0x61, 0x7a));
        }
        return $s;
    }

    function get_headers()
    {
        $headers = array();
        foreach($_SERVER as $key =>$value)
        {
            if(substr($key,0,5) === 'HTTP_')
            {
                $key = substr($key,5);
                $key = explode("_",$key);
                for ($i=0; $i<count($key); $i++)
                {
                    $key[$i] = ucfirst(strtolower($key[$i]));
                }
                $key = implode("-",$key);
                $headers[$key] = $value;
            }
        }
        return $headers;
    }



    function get_flag()
    {
        $flag = file_get_contents("/flag/flag.txt");
        $flag_base64 = base64_encode($flag);
        return "$flag|$flag_base64";
    }

    function get_file()
    {
        if (!empty($_FILES))
        {
            echo "have file upload";
        }

        $files = array();
        $tmpfile = array();

        foreach ($_FILES as $key=>$value)
        {
            $tmpfile['name'] = $key;
            $tmpfile['filename'] = $_FILES[$key]['name'];
            $tmpfile['content'] = base64_encode(file_get_contents($_FILES[$key]['tmp_name']));
            $files[] = $tmpfile;
        }

        return $files;

    }

    function get_response($response)
    {
        $flag = $this->get_flag();

        if (preg_match("/$flag/i", $response) === 1)
        {
            $this->attack = true;
        }

        $resp = array(
            "uid"=>md5($this->filename),
            "res"=>$response,
            "attack"=>$this->attack
        );

        $logjson = json_encode($resp);
        file_put_contents($this->res.$this->filename, $logjson, FILE_APPEND);

        $response = preg_replace("/$flag/i", "go away hacker", $response);

        return $response;
    }

    function mydie()
    {
        header('HTTP/1.1 503 Service Temporarily Unavailable');
        header('Status: 503 Service Temporarily Unavailable');
        header('Retry-After: 300');
        $html = file_get_contents("cant.html");
        $html = str_replace("{{host}}", $_SERVER['HTTP_HOST'], $html);
        #sleep(30);
        die($html);
    }
}

$log = new Log($config);
?>
