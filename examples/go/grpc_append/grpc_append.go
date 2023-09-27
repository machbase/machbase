package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/machbase/neo-grpc/machrpc"
)

func main() {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		panic(err)
	}
	serverAddr := "127.0.0.1:5655"
	serverCert := filepath.Join(homeDir, ".config", "machbase", "cert", "machbase_cert.pem")

	// This example substitute server's key & cert for the client's key, cert.
	// It is just for the briefness of sample code
	// Client applicates **SHOULD** issue a certificate for each one.
	// Please refer to the "API Authentication" section of the documents.
	clientKey := filepath.Join(homeDir, ".config", "machbase", "cert", "machbase_key.pem")
	clientCert := filepath.Join(homeDir, ".config", "machbase", "cert", "machbase_cert.pem")

	cli := machrpc.NewClient(
		machrpc.WithServer(serverAddr),
		machrpc.WithCertificate(clientKey, clientCert, serverCert))
	if err := cli.Connect(); err != nil {
		panic(err)
	}
	defer cli.Disconnect()

	tableName := "example"
	appender, err := cli.Appender(tableName)
	if err != nil {
		panic(err)
	}
	defer appender.Close()

	ts := time.Now()
	for i := 0; i < 100; i++ {
		datum := [3]any{}
		datum[0] = "go-append-ex"           // name
		datum[1] = ts.Add(time.Duration(i)) // time
		datum[2] = 1.0001 * float64(i+1)    // value
		err := appender.Append(datum[:]...)
		if err != nil {
			panic(err)
		}
	}
	fmt.Println("append done.")
}
