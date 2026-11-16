---
paths:
  - "**/*.java"
---
# Java Coding Style

## Formatting

- **google-java-format** (indent, imports, line breaks are delegated to the formatter)
- Member order: constants, fields, constructors, public methods, protected, private
- Blank line at every logical-block boundary inside a method body (setup / validate / act / record).
  Applies equally to boundaries without a comment: the formatter never inserts one, so it is the
  author's duty at writing time. Numbered step comments for flow methods are owned by
  `.claude/rules/comment.md`.

## Immutability

- Prefer `record` for value types and simple DTOs (Java 16+); expose construction via static factory `of()`
- Complex DTOs (many optional fields or inheritance) use Lombok `@Builder` + `@NoArgsConstructor(access = PRIVATE)`
- Mark fields `final` by default — use mutable state only when required
- Return defensive copies from public APIs: `List.copyOf()`, `Map.copyOf()`, `Set.copyOf()`
- Copy-on-write: return new instances rather than mutating existing ones

```java
// Simple — record + static factory
public record SampleDTO(String id, String name, String description) {
  public static SampleDTO of(String id, String name, String description) {
    return new SampleDTO(id, name, description);
  }
}

// Complex — Builder, private no-args
@Getter
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class SampleResponseDTO {
  private String id;
  private String name;
  @JsonInclude(JsonInclude.Include.NON_NULL)
  private String optionalField;
  private LocalDateTime createdAt;

  @Builder
  public SampleResponseDTO(String id, String name, String optionalField,
      LocalDateTime createdAt) {
    this.id = id;
    this.name = name;
    this.optionalField = optionalField;
    this.createdAt = createdAt;
  }
}

// Defensive copy
public List<LineItem> getItems() {
  return List.copyOf(items);
}
```

## Naming

Standard Java conventions apply. Project-specific rule:
- Acronyms use PascalCase, not uppercase (`HttpClient`, `XmlParser` — not `HTTPClient`, `XMLParser`)

## Package Layout — Domain First

Top-level packages by domain. Layer folders (`controller/service/repository`) live inside the domain package, never at the top.

```
com/example/app/
├── {domainA}/
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── dto/
│   └── exception/
├── {domainB}/
│   ├── controller/
│   ├── service/
│   ├── handler/
│   └── dto/
└── config/
```

## Modern Java Features

Use modern language features where they improve clarity:
- **Sealed classes** for closed type hierarchies (Java 17+)
- **Pattern matching** with `instanceof` — no explicit cast (Java 16+)
- **Text blocks** for multi-line strings — SQL, JSON templates (Java 15+)
- **Switch expressions** with arrow syntax (Java 14+)
- **Pattern matching in switch** — exhaustive sealed type handling (Java 21+)

```java
// Pattern matching instanceof
if (shape instanceof Circle c) {
    return Math.PI * c.radius() * c.radius();
}

// Sealed type hierarchy
public sealed interface PaymentMethod permits CreditCard, BankTransfer, Wallet {}

// Switch expression
String label = switch (status) {
    case ACTIVE -> "Active";
    case SUSPENDED -> "Suspended";
    case CLOSED -> "Closed";
};
```

## Optional Usage

- Return `Optional<T>` from finder methods that may have no result
- Use `map()`, `flatMap()`, `orElseThrow()` — never call `get()` without `isPresent()`
- Never use `Optional` as a field type or method parameter

```java
// GOOD
return repository.findById(id)
    .map(ResponseDto::from)
    .orElseThrow(() -> new OrderNotFoundException(id));

// BAD — Optional as parameter
public void process(Optional<String> name) {}
```

## ConfigurationProperties

Declare as `record` with nested records for hierarchical options. Plain class + `@Setter` is forbidden.

```java
@ConfigurationProperties(prefix = "sample")
public record SampleProperties(
    Local local,
    Remote remote,
    String defaultKey,
    Integer expiredHours
) {
  public record Local(boolean enabled, String basePath) {}
  public record Remote(boolean enabled, String endpoint, String region) {}
}
```

## Bean Validation Messages — Korean

Bean Validation `message` attributes (`@NotBlank`, `@Size`, `@Pattern`, `@Email`, …) are written as user-facing Korean sentences, never English defaults.

```java
@NotBlank(message = "사용자 ID는 필수값입니다.")
@Size(max = 30, message = "사용자 ID는 최대 30자리이어야 합니다.")
@Pattern(regexp = "^[a-zA-Z0-9_]*$", message = "사용자 ID는 영문자, 숫자, _만 입력 가능합니다.")
private String userId;
```

## Type Routing — Map Factory with Default Fallback

Do not branch implementations with `if/else`. Inject the implementation list via constructor, register into a `Map`, and look up by key. Unmatched keys fall back to a domain default.

```java
@Component
public class SampleHandlerFactory {
  private final Map<String, SampleHandler> handlerMap = new HashMap<>();

  public SampleHandlerFactory(List<SampleHandler> handlers) {
    for (SampleHandler handler : handlers) {
      handlerMap.put(handler.getType().name(), handler);
    }
  }

  public SampleHandler getHandler(String type) {
    return handlerMap.getOrDefault(type, handlerMap.get(SampleType.DEFAULT.name()));
  }
}
```

## Error Handling

- Prefer unchecked exceptions for domain errors
- Create domain-specific exceptions extending `RuntimeException`
- Avoid broad `catch (Exception e)` unless at top-level handlers
- Include context in exception messages

```java
public class OrderNotFoundException extends RuntimeException {
    public OrderNotFoundException(Long id) {
        super("Order not found: id=" + id);
    }
}
```

## Streams

- No side effects in stream operations; if the logic is convoluted, use a plain loop.

## Tests

- JUnit 5 + AssertJ (`assertThat`). Class and methods package-private.
- Method name: descriptive English (`emptyPageReturnsNoItems`), not `test1`.
- Every `@Test` MUST carry a Korean `@DisplayName` that states the behaviour as a sentence
  (`~한다` / `~된다`). The method name is for the IDE; the `@DisplayName` is what a reader of the
  test report sees.
- Pure logic: call the constructor directly, no Spring context. Context needed -> narrowest
  slice: `@SpringBootTest(webEnvironment = NONE)` for non-web logic, `@WebMvcTest` for controllers.

```java
@Test
@DisplayName("빈 페이지는 항목을 반환하지 않는다")
void emptyPageReturnsNoItems() {
  ...
}
```

## Javadoc — Korean

What to write and what to delete is owned by `.claude/rules/comment.md`. This section holds only the Java notation.

Three common kinds:

- Business rules (path formats, external system contracts)
- Management location (`@see` pointing to where configuration/definition lives)
- Workaround reasons (when behavior depends on library quirks)

```java
// Business rule
/**
 * <pre>
 * 파일 저장 경로: {storage.basePath} / {category} / {yyyy} / {MM} / {dd} / {fileId}
 * </pre>
 */

// Management location
/**
 * @see com.example.config.SampleConfig 에서 관리
 */

// Workaround reason
// Spring에서 InputStream을 자동 종료해줌
```
