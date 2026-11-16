---
paths:
  - "**/*.java"
---
# Java Code Patterns

Reusable code skeletons applied repeatedly when writing/modifying Java files. Class/package names in examples are illustrative — substitute with the actual domain.

## Service

Business flow lives in Service. Class-level `@Transactional(readOnly = true)`; write methods override with method-level `@Transactional`.

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SampleService {

  private final SampleRepository sampleRepository;

  @Transactional
  public SampleResponseDTO create(SampleRequestDTO request) {
    Sample saved = sampleRepository.save(Sample.from(request));
    return SampleResponseDTO.from(saved);
  }

  public SampleResponseDTO get(String id) {
    return sampleRepository.findById(id)
        .map(SampleResponseDTO::from)
        .orElseThrow(() -> new SampleNotFoundException(id));
  }
}
```

## Controller

Return the DTO directly when the endpoint just needs `200 OK + JSON body`. Wrap with `ResponseEntity` only when status code, headers, or body composition must be controlled.

```java
@RestController
@RequestMapping("/api/v1/samples")
@RequiredArgsConstructor
public class SampleController {

  private final SampleService sampleService;

  // Simple API — 200 + JSON body
  @GetMapping("/{id}")
  public SampleResponseDTO get(@PathVariable String id) {
    return sampleService.get(id);
  }

  // Status / header / body composition needed
  @PostMapping
  public ResponseEntity<SampleResponseDTO> create(@Valid @RequestBody SampleRequestDTO request) {
    SampleResponseDTO response = sampleService.create(request);
    return ResponseEntity.status(HttpStatus.CREATED).body(response);
  }
}
```

```java
@Controller
@RequestMapping("/samples")
public class SamplePageController {

  @GetMapping
  public String index() {
    return "sample/index";
  }
}
```

## Repository


### JdbcTemplate

For repeated insert/update/delete, use `batchUpdate(...)` for bulk performance.

### JdbcClient

Available with Spring Framework 6.1+. Fluent API for single-statement CRUD. `JdbcClient` has no batch API — for bulk operations keep using `JdbcTemplate.batchUpdate(...)`.


```java
@Repository
@RequiredArgsConstructor
public class SampleStatRepository {

  private final JdbcClient jdbcClient;

  public Optional<SampleStatDTO> find(String key) {
    return jdbcClient.sql("""
        SELECT KEY_NAME, CNT
        FROM SAMPLE_STAT
        WHERE KEY_NAME = :key
        """)
        .param("key", key)
        .query(SampleStatDTO.class)
        .optional();
  }

  public void save(String key, long count) {
    jdbcClient.sql("""
        INSERT INTO SAMPLE_STAT (KEY_NAME, CNT, CREATED_AT)
        VALUES (:key, :count, NOW())
        """)
        .param("key", key)
        .param("count", count)
        .update();
  }
}
```
