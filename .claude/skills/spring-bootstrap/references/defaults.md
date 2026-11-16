# Team-Standard Defaults

## Base defaults

- Project: `Gradle - Groovy`
- Language: `Java`
- Packaging default: `jar`
- Bootstrapping source: `Spring Initializr`
- Configuration file format: `yaml` -> rename to `application.yml`

## Base common dependencies

- `web`
- `validation`
- `jpa`
- `lombok`

## Typical DB driver example

- `mysql` -> `mysql-connector-j`

## Optional data-access features

- `flyway`
- `querydsl`

## Test/build defaults

- `@ActiveProfiles("test")`
- H2 for `test` profile
- If `bootJar` is used, disable plain `jar`

## Dependency rules

- Include only dependencies the user approved
- Don't add extra dependencies from habit or convenience
- If `SSR용`, `thymeleaf` is mandatory
- If `API 전용`, `thymeleaf` is excluded by default
- If Flyway is enabled, migration directories must match DB strategy
- If Flyway is enabled, enable `baseline-on-migrate`
- If Querydsl is enabled, generated source/build hooks must be configured
