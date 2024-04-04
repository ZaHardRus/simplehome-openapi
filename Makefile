source_openapi_dest := ./openapi/openapi.yaml
bundled_openapi_dest := ./openapi/bundled_openapi

install_npm_dependencies:
	npm i -g @redocly/cli@latest

bundle_openapi:
	redocly bundle --remove-unused-components -o "$(bundled_openapi_dest).yaml" --ext yaml $(source_openapi_dest)

bundle_openapi_json:
	redocly bundle --remove-unused-components -o "$(bundled_openapi_dest).json" --ext json $(source_openapi_dest)
