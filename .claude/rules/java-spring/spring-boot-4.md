---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle"
  - "**/build.gradle.kts"
  - "**/settings.gradle"
  - "**/settings.gradle.kts"
  - "**/application*.yml"
  - "**/application*.properties"
---

# Spring Boot 4.x Rule

## Official Docs (WebFetch the relevant section before work)
- Spring Boot: https://docs.spring.io/spring-boot/reference/
- API: https://docs.spring.io/spring-boot/api/
- Spring Framework: https://docs.spring.io/spring-framework/reference/

## Core Rules
1. **New dependency/config key**: WebFetch the relevant reference section first.
2. **Uncertain API**: Do not write from generative knowledge. Verify against official docs.
3. **Real cases only**: This file is append-only. Add real pitfalls encountered during work immediately.

## Known Issues

> Keep entries concise and AI-readable. Record only real issues observed in practice. Use one row per issue in the format: `Title | Problem | Resolution`.

| Title | Problem | Resolution |
|---|---|---|
| Gradle Version | Gradle 8.x used with Java 25 causes `Unsupported class file major version 69` during `_BuildScript_` semantic analysis | Migrate Gradle wrapper to `9.4.1` |
| Starter Renames | Legacy starter coordinates can be misleading or deprecated in Spring Boot 4 | Rename to SB4 coordinates: `-web` -> `-webmvc`, `-web-services` -> `-webservices`, `-oauth2-*` -> `-security-oauth2-*` |
| 404 Config Key | `spring.mvc.throw-exception-if-no-handler-found` is carried over from SB3 even though SB4 no longer needs that pattern | Remove the key. For HTML 404 pages, `templates/error/404.html` is sufficient |
| ControllerAdvice 404 Handling | `/api/**` transport-level 404 responses are not wrapped by `@ControllerAdvice(annotations=...)` | Handle via a custom `ErrorController` because `NoResourceFoundException` is raised by `ResourceHttpRequestHandler`, outside `@Controller` |
| ErrorController Package | `org.springframework.boot.web.servlet.error.ErrorController` import no longer resolves | Use `org.springframework.boot.webmvc.error.ErrorController` |
| Thymeleaf Layout Dialect | Initializing `thymeleaf-layout-dialect` with `3.4.0` causes version mismatch with Spring Boot 4 targets | Upgrade to `4.x`. Spring Boot 4 alignment is documented at https://ultraq.github.io/thymeleaf-layout-dialect/migrating-to-4.0/ |
| @DataJpaTest Package | `org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest` import no longer resolves on SB4 | Use `org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest` (provided by `spring-boot-data-jpa-test` module pulled in via `spring-boot-starter-data-jpa-test`) |
| Jackson 3 Packages | SB4 ships Jackson 3.x. `com.fasterxml.jackson.databind.ObjectMapper` / `ObjectNode` no longer resolve | Import from `tools.jackson.databind.*` (e.g., `tools.jackson.databind.ObjectMapper`, `tools.jackson.databind.node.ObjectNode`). Annotations such as `@JsonInclude` remain under `com.fasterxml.jackson.annotation.*` |
| ValidationAutoConfiguration Package | `org.springframework.boot.autoconfigure.validation.ValidationAutoConfiguration` import no longer resolves on SB4 | Use `org.springframework.boot.validation.autoconfigure.ValidationAutoConfiguration` (provided by `spring-boot-validation` module pulled in via `spring-boot-starter-validation`) |
| Security Test Starter | Adding `org.springframework.security:spring-security-test` directly bypasses SB4 BOM test-starter convention | Use `org.springframework.boot:spring-boot-starter-security-test` (exists on Maven Central for 4.x) |
| AutoConfigureMockMvc Package | `org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc` import no longer resolves on SB4 | Use `org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc` (same module as `WebMvcTest`) |
| Security 7 EntryPoint Redirect | MockMvc assertion `redirectedUrl("http://localhost/login")` fails for unauthenticated requests | Spring Security 7 `LoginUrlAuthenticationEntryPoint` redirects with a relative URI; assert `redirectedUrl("/login")` |
| CSRF Token Rotation on Login | CSRF token obtained before form login becomes invalid after authentication succeeds (`CsrfAuthenticationStrategy` rotates it), breaking curl-based logout/POST verification | Re-fetch the token from a post-login page that renders a `th:action` form; in MockMvc use `with(csrf())` |
| NoResourceFoundException Constructor | Spring Framework 7 `NoResourceFoundException(HttpMethod, String)` 2-arg constructor no longer exists | Use the 3-arg form `NoResourceFoundException(HttpMethod, resourcePath, matchedPattern)` |
| ContentDisposition Dual Filename | `ContentDisposition.attachment().filename(name, UTF_8)` emits both `filename=` and `filename*=UTF-8''...` even for pure-ASCII names, breaking exact-match header assertions | Assert with `containsString("filename=...")` instead of exact header equality |
| H2 DATE_FORMAT Unsupported | Native query using MySQL `DATE_FORMAT(col,'%Y-%m')` throws `JdbcSQLSyntaxErrorException` under test profile H2(MODE=MySQL) even though prod MySQL accepts it | Isolate the month/format expression behind a vendor dialect; for H2 use standard `SUBSTRING(CAST(col AS VARCHAR),1,7)` to extract `yyyy-MM` |
| AssertJ POI Row Ambiguity | `assertThat(xssfRow)` fails to compile ("reference to assertThat is ambiguous") because `XSSFRow` implements both `Comparable` and `Iterable`, matching two AssertJ overloads | Cast to Object for null checks: `assertThat((Object) row).isNotNull()` |
