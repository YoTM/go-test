package main

import (
    "fmt"
    "io"
   // "io/ioutil"
    "log"
    "os"
    "net"
	"net/http"
	"time"
)

func main() {
    // адрес со списком запрещенных ресурсов
	url := "https://api.antizapret.info/all.php"

	timeout := time.Duration(5) * time.Second
	transport := &http.Transport{
		ResponseHeaderTimeout: timeout,
		Dial: func(network, addr string) (net.Conn, error) {
			return net.DialTimeout(network, addr, timeout)
		},
		DisableKeepAlives: true,
	}

	client := &http.Client{
		Transport: transport,
	}

	resp, err := client.Get(url)
	if err != nil {
		fmt.Println(err)
	}

	defer resp.Body.Close()


    // Вывожу файл в консоль
    if _, err := io.Copy(os.Stdout, resp.Body); err != nil {
		log.Fatal(err)
	}

}