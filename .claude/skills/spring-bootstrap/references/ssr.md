# SSR Defaults

## Architecture rules

- Include `thymeleaf`
- Propose `thymeleaf-layout-dialect` in the dependency decision
- Create server-rendered template/static structure
- Create error pages during bootstrap

## Default bootstrap artifacts

- `src/main/resources/templates/{layout,fragments,error}`
- `src/main/resources/static/{css,js,images}`
- view/error-page bootstrap structure

## Example resource structure

```text
src/main/resources
├─ templates
│  ├─ layout
│  ├─ fragments
│  └─ error
└─ static
   ├─ css
   ├─ js
   └─ images
```

## Verification focus

- `templates/{layout,fragments,error}` exists
- `static/{css,js,images}` exists
- error pages are present
