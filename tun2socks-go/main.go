package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"go.uber.org/automaxprocs/maxprocs"
	"gopkg.in/yaml.v3"

	_ "github.com/xjasonlyu/tun2socks/v2/dns"
	"github.com/xjasonlyu/tun2socks/v2/engine"
	"github.com/xjasonlyu/tun2socks/v2/internal/version"
	"github.com/xjasonlyu/tun2socks/v2/log"
)

var (
	key = new(engine.Key)

	configFile  string
	versionFlag bool
)

func init() {
}

func main() {
	maxprocs.Set(maxprocs.Logger(func(string, ...any) {}))

	if versionFlag {
		fmt.Println(version.String())
		fmt.Println(version.BuildString())
		os.Exit(0)
	}

	if configFile != "" {
		data, err := os.ReadFile(configFile)
		if err != nil {
			log.Fatalf("Failed to read config file '%s': %v", configFile, err)
		}
		if err = yaml.Unmarshal(data, key); err != nil {
			log.Fatalf("Failed to unmarshal config file '%s': %v", configFile, err)
		}
	}

	engine.Insert(key)

	engine.Start()
	defer engine.Stop()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh
}

//export startFromArgs
func startFromArgs(device string, networkInterface string, logLevel string, proxy string, restAPI string) {
	customKey := new(engine.Key)

	customKey.Device = device
	customKey.Interface = networkInterface
	customKey.LogLevel = logLevel
	customKey.Proxy = proxy
	customKey.RestAPI = restAPI

	engine.Insert(customKey)

	engine.Start()
	defer engine.Stop()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	<-sigCh
}
