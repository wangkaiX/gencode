package main

import (
	"time"
    "net/http"

	"${package_graphql_resolver_dir}"
	"${package_project_dir}/app/define"

	graphql "github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/relay"
)

var schema_graphql = ` 
${schema_graphql}
`

func InitGraphql() {
	schema := graphql.MustParseSchema(schema_graphql, &${os.path.basename(package_graphql_resolver_dir)}.${graphql_resovler_type})
	handler := relay.Handler{Schema: schema}
    mux := http.ServeMux{}
    mux.Handle("/graphql", &handler)
    
    server := http.Server{
        WriteTimeout : 10 * time.Second,
        ReadTimeout : 10 * time.Second,
		Addr : fmt.Sprintf("%s:%s", define.Cfg.GraphqlAddr.Ip, define.Cfg.GraphqlAddr.Port),
        Handler : &mux,
    }
    server.ListenAndServe()
}
