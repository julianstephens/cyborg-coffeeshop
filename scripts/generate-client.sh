#! /usr/bin/env bash

set -e
set -x

cd backend
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
cd ..
# node frontend/modify-openapi-operationids.js
mv openapi.json frontend/
cd frontend
pnpm dlx openapi-typescript ./openapi.json -o ./src/types/openapi.d.ts
pnpm dlx biome format --write ./src/client
