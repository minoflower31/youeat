# API-Only Defaults

## Architecture rules

- Exclude `thymeleaf` by default
- Do not create `templates/` unless the user explicitly asks for mixed rendering
- Do not create SSR-oriented view placeholders by default
- Focus on API response / exception handling bootstrap structure

## Default bootstrap artifacts

- `common.response.ApiResponse<T>`
- `common.exception.ErrorCode`
- `common.exception.CommonErrorCode`
- `common.exception.BusinessException`
- `common.exception.ApiExceptionHandler`
- `common.web.ApiController`

## Example API bootstrap structure

```text
common
├─ exception
│  ├─ ErrorCode
│  ├─ CommonErrorCode
│  ├─ BusinessException
│  └─ ApiExceptionHandler
├─ response
│  └─ ApiResponse<T>
└─ web
   └─ ApiController
```

## Verification focus

- API bootstrap classes compile
- `/api/**` error handling returns JSON response shape
- No unnecessary template/view artifacts are added by default
