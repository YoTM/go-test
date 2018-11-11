package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "os/exec"
    "io/ioutil"
)

// Считыватель файлов. Принимает имя файла и выдаёт его содержимое
func readFile(iFileName string) string {
  // Считываем файл
  lData, err := ioutil.ReadFile(iFileName)
  var lOut string // Объявляем строчную переменную
  // Если файл существует - записываем его в переменную lOut
  if !os.IsNotExist(err) {
        lOut = string(lData)
    } else { // Иначе - отправляем стандартный текст
        lOut = "404"
    }
  return lOut // Возвращаем полученную информацию
}

func Index(w http.ResponseWriter, r *http.Request) {

    fmt.Fprintf(w, "Content filtr is running!\n") // отправляем данные на клиентскую сторону

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

    lData := readFile("./out.csv") // Считываем файл

    // Отправляет в ответ на запрос
    fmt.Fprintln(w, lData)
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
