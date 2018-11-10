package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "os/exec"
    //"path/filepath"
    //"io/ioutil"
    //"encoding/csv"
    //"bufio"
)


func Index(w http.ResponseWriter, r *http.Request) {

    fmt.Fprintf(w, "Content filtr is running!") // отправляем данные на клиентскую сторону

	// блок манипуляций с файлом

    fileUrl := "https://api.antizapret.info/all.php"

    err := DownloadFile("data.csv", fileUrl)
    if err != nil {
        panic(err)
    }

    // Запускаем парсер на питоне
    data_file := []byte("data.csv")
    cmd := exec.Command("python3", "parser.py")

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

    // сохраняем ответ парсера в файл out.csv
    outfile, err := os.Create("./out.csv")
    if err != nil {
        panic(err)
    }
    defer outfile.Close()
    cmd.Stdout = outfile

    err = cmd.Start(); if err != nil {
        panic(err)
    }
    cmd.Wait()

   // fmt.Println("Exec status: ", cmd.Run())

    // здесь прописываем заголовки и имя скаченному файлу со списком
	w.Header().Set("Content-Disposition", "attachment; filename=response.csv")
	w.Header().Set("Content-Type", r.Header.Get("Content-Type"))
	w.Header().Set("Content-Length", r.Header.Get("Content-Length"))

	//
	io.Copy(w, outfile)

   // отдаём файл результата клиенту
    //fmt.Println("Read request: " + "out.csv")
   // file, err := ioutil.ReadAll(outfile)     //ReadFile("./out.csv")
 //   if err != nil {
  //    fmt.Println("Cann't open file: " + "out.csv")
 //   } else {
  //    w.Write(file)
   // }



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
	http.HandleFunc("/getAllUrls", Index)
	err := http.ListenAndServe(":8080", nil)

	if err != nil {
		fmt.Println(err)
	}
}
