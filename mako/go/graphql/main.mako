package main

import (
	"time"

	"${pro_path}/app/resolver"
	"git.ucloudadmin.com/securityhouse/dataflow/pkg/httpserver"

	graphql "github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/relay"
)

func main() {
	schema := graphql.MustParseSchema(schema_str, &resolver.Resolver{})
	handler := relay.Handler{Schema: schema}
	h := httpserver.InitHttpServer(
		httpserver.Trace(false),
		httpserver.HostPort("", "40011"),
		httpserver.ReadTimeout(10*time.Second),
		httpserver.WriteTimeout(10*time.Second),
		httpserver.PathFunc("/graphql", "GET,POST", handler.ServeHTTP),
	)
	h.Run()
	select {}
}
