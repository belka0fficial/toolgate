
# ToolGate



ToolGate is a local self-hosted control plane for agent tools and keys.



It gives you:

- key storage

- tool registry

- tool execution

- remove / restore lifecycle

- audit log

- untrusted output wrapping

- basic security classification

- local CLI



## Current stack



- FastAPI

- Postgres

- Docker

- Bash CLI



## Install



Clone the repo and install the CLI:



```bash

git clone https://github.com/belka0fficial/toolgate.git

cd toolgate

./scripts/install.sh

toolgate

````



If the command is not found in a new shell, run:



```bash

export PATH="$HOME/.local/bin:$PATH"

```



## Start Postgres



From the repo root:



```bash

docker compose up -d

```



## Run API



```bash

cd services/api

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8010

```



## API docs



* [http://localhost:8010/docs](http://localhost:8010/docs)



## CLI usage



### Keys



Add a key:



```bash

toolgate keys:add GITHUB_KEY github

```



List keys:



```bash

toolgate keys:list

```



Get key metadata:



```bash

toolgate keys:get GITHUB_KEY

```



### Tools



List tools:



```bash

toolgate tools:list

```



List removed tools:



```bash

toolgate tools:removed

```



Get tool metadata:



```bash

toolgate tools:get github.create_repo

```



Execute a tool:



```bash

toolgate tools:execute github.list_repos '{}'

```



Execute a tool with arguments:



```bash

toolgate tools:execute github.create_repo '{"name":"toolgate-cli-test","private":true}'

```



Remove a tool:



```bash

toolgate tools:remove github.create_repo

```



Restore a tool:



```bash

toolgate tools:restore github.create_repo

```



## Current features



* store keys through ToolGate

* register tools

* execute HTTP tools

* remove / restore tools

* inspect audit logs through API

* wrap external tool output as untrusted data



## Current limitations



* only HTTP executor is implemented in v1

* MCP executor is not implemented yet

* local executor is not implemented yet

* CLI does not yet support tools:add and tools:edit

* UI is not built yet

