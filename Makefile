source_openapi_dest := ./openapi/openapi.yaml
bundled_openapi_dest := ./openapi/bundled_openapi

install_npm_dependencies:
	npm i -g swagger-cli
	# npm i -g @redocly/cli@latest

bundle_openapi:
	swagger-cli bundle $(source_openapi_dest) --outfile "$(bundled_openapi_dest).yaml" --type yaml -d
	# redocly bundle -o "$(bundled_openapi_dest).yaml" --ext yaml $(source_openapi_dest)

bundle_openapi_json:
	swagger-cli bundle $(source_openapi_dest) --outfile "$(bundled_openapi_dest).json" --type json -d -r
	# redocly bundle -o "$(bundled_openapi_dest).json" --ext json $(source_openapi_dest)
