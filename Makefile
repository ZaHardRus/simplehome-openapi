source_openapi_dest := ./openapi/openapi.yaml
bundled_openapi_dest := ./openapi/bundled_openapi

install_npm_dependencies:
	npm i -g swagger-cli

bundle_openapi:
	swagger-cli bundle $(source_openapi_dest) --outfile "$(bundled_openapi_dest).yaml" --type yaml -d

bundle_openapi_json:
	swagger-cli bundle $(source_openapi_dest) --outfile "$(bundled_openapi_dest).json" --type json -d
