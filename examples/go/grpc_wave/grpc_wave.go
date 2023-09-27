package main

import (
	"math"
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
		machrpc.WithCertificate(clientKey, clientCert, serverCert),
	)
	if err := cli.Connect(); err != nil {
		panic(err)
	}
	defer cli.Disconnect()

	sqlText := `insert into example (name, time, value) values (?, ?, ?)`

	for ts := range time.Tick(500 * time.Millisecond) {
		delta := float64(ts.UnixMilli()%15000) / 15000
		theta := 2 * math.Pi * delta
		sin, cos := math.Sin(theta), math.Cos(theta)
		if result := cli.Exec(sqlText, "wave.sin", ts, sin); result.Err() != nil {
			panic(result.Err())
		}
		if result := cli.Exec(sqlText, "wave.cos", ts, cos); result.Err() != nil {
			panic(result.Err())
		}
	}
}
