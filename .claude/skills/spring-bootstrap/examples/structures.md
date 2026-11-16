# Example Structures

## Example package structure

Top-level packages by domain. Layer folders (`controller/service/repository`) live inside the domain package, never at the top.

```text
com/example/app/
├─ common
│  ├─ config
│  ├─ constant
│  ├─ entity
│  ├─ exception
│  ├─ response
│  └─ util
├─ {domainA}
│  ├─ controller
│  ├─ service
│  ├─ repository
│  └─ dto
├─ {domainB}
│  ├─ controller
│  ├─ service
│  ├─ handler
│  └─ dto
└─ external
```

## Example profile files

```text
src/main/resources
├─ application.yml
├─ application-local.yml
├─ application-stg.yml
└─ application-prod.yml

src/test/resources
└─ application-test.yml
```

## Example JPA auditing structure

```text
common
├─ config
│  └─ JpaAuditingConfig
└─ entity
   └─ BaseEntity
```
