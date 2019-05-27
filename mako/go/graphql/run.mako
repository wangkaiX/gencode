package main

import (
	"time"
    "net/http"

	"${pro_path}/app/graphqlresolver"

	graphql "github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/relay"
)

func GraphqlRun() {
	schema := graphql.MustParseSchema(schema_str, &graphqlresolver.Resolver{})
	handler := relay.Handler{Schema: schema}
    mux := http.ServeMux{}
    mux.Handle("/graphql", &handler)
    
    server := http.Server{
        WriteTimeout : 10 * time.Second,
        ReadTimeout : 10 * time.Second,
        Addr : "${ip}:${port}",
        Handler : &mux,
    }
    server.ListenAndServe()
}
