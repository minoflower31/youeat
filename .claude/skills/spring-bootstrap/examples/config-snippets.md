# Example Config Snippets

## Example `.env.example`

```dotenv
SPRING_PROFILES_ACTIVE=local
DB_VENDOR=mysql
SPRING_DATASOURCE_URL="jdbc:mysql://localhost:3306/app?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Seoul"
SPRING_DATASOURCE_USERNAME=app_user
SPRING_DATASOURCE_PASSWORD=app_password
```

### `.env` quoting rules

`run.sh start` sources `.env` as a shell script. Quote values with `&`, `?`, space, or shell metacharacters. Don't leave JDBC URLs with query strings unquoted.

## Example `.gitignore` entries

If `.gitignore` exists, don't overwrite it. Append only missing entries.

```gitignore
.env
.app.pid
log/
build/
.gradle/
.idea/
*.iml
out/
```

## Example JPA settings

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: update
      naming:
        physical-strategy: org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
    open-in-view: false
    properties:
      hibernate:
        format_sql: true
```

## Example logging settings

```yaml
logging:
  file:
    path: log
    name: ${logging.file.path}/${spring.application.name}.log
  level:
    root: info
    org:
      hibernate:
        type:
          descriptor:
            sql: trace
  pattern:
    console: "%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(%5p) %clr([${spring.application.name},%X{trace_id},%X{span_id}]) %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m %n%wEx"
    file: "%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(%5p) %clr([${spring.application.name},%X{trace_id},%X{span_id}]) %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m %n%wEx"
  logback:
    rollingpolicy:
      file-name-pattern: ${logging.file.name}.%d{yyyyMMdd}.%i
      max-history: 10
      max-file-size: 1GB
```

## Example Flyway settings

```yaml
spring:
  flyway:
    enabled: true
    baseline-on-migrate: true
    locations: classpath:db/migration/${db.vendor}
```

## Example `BaseEntity` responsibilities

- `createdAt`: `@CreatedDate`, `nullable=false`, `updatable=false`
- `createdBy`: `@CreatedBy`, `updatable=false`
- `updatedAt`: `@LastModifiedDate`
- `updatedBy`: `@LastModifiedBy`

## Example `ApiResponse` shape

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "OK",
  "data": {},
  "timestamp": "2026-04-16T12:34:56"
}
```

## Example Gradle packaging rule

```groovy
jar {
    enabled = false
}
```
