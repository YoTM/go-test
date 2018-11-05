package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "os/exec"
)

func Index(w http.ResponseWriter, r *http.Request) {

	// блок манипуляций с файлом

    fileUrl := "https://api.antizapret.info/all.php"

    err := DownloadFile("data.csv", fileUrl)
    if err != nil {
        panic(err)
    }

    // попытка достучаться до питона
    data_file := []byte("data.csv")
    cmd := exec.Command("python3", "get_urls.py")

    stdin, err := cmd.StdinPipe()
    if err != nil {
        panic(err)
    }

    go func() {
        defer stdin.Close()
        if _, err := stdin.Write(data_file); err != nil {
            panic(err)
        }
    }()

    fmt.Println("Exec status: ", cmd.Run())

}


func DownloadFile(filepath string, url string) error {

    fmt.Println("Downloading is started")

    // Create the file
    out, err := os.Create(filepath)
    if err != nil {
        return err
    }
    defer out.Close()

    // Get the data
    resp, err := http.Get(url)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    // Write the body to file
    _, err = io.Copy(out, resp.Body)

    fmt.Println("Downloading is complete...")

    if err != nil {
        return err
    }

    return nil
}

func main() {
	http.HandleFunc("/", Index)
	err := http.ListenAndServe(":8000", nil)

	if err != nil {
		fmt.Println(err)
	}
}
