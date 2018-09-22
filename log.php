<?php
class Log
{
    private $uri, $method, $headers, $data, $ip, $time, $log;
    function __construct()
    {
        $this->dir = "/tmp/log/";
        $this->uri =$_SERVER['REQUEST_URI'];
        $this->method = $_SERVER['REQUEST_METHOD'];
        $this->headers = $this->get_headers();
        $this->data = file_get_contents("php://input");
        $this->ip = $this->get_ip();
        $this->time = $this->get_date();
        $this->log = array();
        $this->log['uri'] = $this->uri;
        $this->log['method'] = $this->method;
        $this->log['headers'] = $this->headers;
        $this->log['data'] = $this->data;
        $this->log['ip'] = $this->ip;
        $this->log['time'] = $this->time;
        $logjson = json_encode($this->log);
        $filename = $this->gen_randstr();
        if (!is_dir($this->dir))
        {
            mkdir($this->dir,0755);
        }

        file_put_contents($this->dir.$filename.date('H_i_s',time()), $logjson, FILE_APPEND);
    }

    function gen_randstr()
    {
        $s = "";
        for($i=0; $i<12; $i++)
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

    function get_date()
    {
        date_default_timezone_set('PRC');
        return date('Y-m-d H:i:s',time());
    }

    function get_ip()
    {
        return $_SERVER["REMOTE_ADDR"];
    }
}

$log = new Log();

?>