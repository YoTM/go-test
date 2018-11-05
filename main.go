package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"time"
)

func Index(w http.ResponseWriter, r *http.Request) {
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

	// здесь прописываем заголовки и имя скаченному файлу со списком
	w.Header().Set("Content-Disposition", "attachment; filename=data.csv")
	w.Header().Set("Content-Type", r.Header.Get("Content-Type"))
	w.Header().Set("Content-Length", r.Header.Get("Content-Length"))

	//stream the body to the client without fully loading it into memory
	io.Copy(w, resp.Body)




}

func main() {
	http.HandleFunc("/", Index)
	err := http.ListenAndServe(":8000", nil)

	if err != nil {
		fmt.Println(err)
	}
}
