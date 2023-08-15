package encryptutils

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func Decryptkey(data string) string {
	ct, _ := base64.StdEncoding.DecodeString(data)
	block, _ := aes.NewCipher([]byte("Y3Rme2szeV8zbmNyeXA3XzFuZ19rM3l9"))

	if len(ct) < aes.BlockSize {
		return ""
	}

	iv := ct[:aes.BlockSize]
	ct = ct[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	stream.XORKeyStream(ct, ct)

	return string(ct)
}

func Encrypt(file string) string {
	data, err := os.ReadFile(file)
	bytes := []byte(data)

	if err != nil {
		panic(nil)
	}

	key := []byte("Y3Rme2szeV8zbmNyeXA3XzFuZ19rM3l9")

	block, err := aes.NewCipher(key)
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
