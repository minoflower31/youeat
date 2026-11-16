# Example Scripts

## Example metadata fetch

```bash
curl -s https://start.spring.io/metadata/client
```

## Example minimal metadata fetch

```bash
curl -s https://start.spring.io/metadata/client | jq '{
  bootVersion: .bootVersion.default,
  javaVersion: .javaVersion.default,
  packaging: .packaging.default,
  language: .language.default,
  type: .type.default,
  groupId: .groupId.default,
  artifactId: .artifactId.default,
  name: .name.default,
  description: .description.default,
  packageName: .packageName.default
}'
```

## Example on-demand metadata fields

```bash
curl -s https://start.spring.io/metadata/client | jq '.bootVersion.values[].id'
curl -s https://start.spring.io/metadata/client | jq '.javaVersion.values[].id'
curl -s https://start.spring.io/metadata/client | jq '.packaging.values[].id'
curl -s https://start.spring.io/metadata/client | jq '.language.values[].id'
curl -s https://start.spring.io/metadata/client | jq '.type.values[].id'
```

## Example Initializr command shape

```bash
curl -G https://start.spring.io/starter.zip \
  -d type=gradle-project \
  -d language=java \
  -d bootVersion=4.0.5 \
  -d configurationFileFormat=yaml \
  -d javaVersion=25 \
  -d packaging=jar \
  -d groupId=com.example \
  -d artifactId=myapp \
  -d name=myapp \
  --data-urlencode "description=Example project" \
  -d packageName=com.example.myapp \
  -d dependencies=web,validation,data-jpa,lombok \
  -o myapp.zip
```

## Example `run.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

PID_FILE=".app.pid"

start() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "already running (PID $(cat "$PID_FILE"))"
    exit 1
  fi

  if [ -f .env ]; then
    set -a
    . ./.env
    set +a
  fi

  mkdir -p log
  nohup java -jar build/libs/*.jar --spring.profiles.active="${SPRING_PROFILES_ACTIVE:-local}" >/dev/null 2>&1 &
  echo $! > "$PID_FILE"
  echo "started (PID $!)"
}

stop() {
  if [ ! -f "$PID_FILE" ]; then
    echo "not running"
    return 0
  fi
  pid=$(cat "$PID_FILE")
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid"
    echo "stopped (PID $pid)"
  else
    echo "stale pid file"
  fi
  rm -f "$PID_FILE"
}

status() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "running (PID $(cat "$PID_FILE"))"
  else
    echo "not running"
  fi
}

case "${1:-}" in
  start)  start ;;
  stop)   stop ;;
  status) status ;;
  *) echo "usage: $0 {start|stop|status}"; exit 2 ;;
esac
```
