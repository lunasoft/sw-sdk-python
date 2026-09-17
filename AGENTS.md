# Agent Guide for sw-sdk-python

This repository contains a pure-Python SDK for the SW sapien® (SmarterWeb) web services and a `unittest`-based test suite that hits the live test environment. Use the guidance below when acting as an automated coding agent.

## Repository Overview
- Package name: `sw-sdk-python`, version declared in `setup.py` (`0.0.14.1`).
- The repository root **is** the importable source tree: every service is a top-level package directory (`Stamp/`, `Issue/`, `Cancelation/`, ...). There is no `src/` layout.
- Shared infrastructure lives in `Utils/`:
  - `Utils/Services.py` — `Services` base class (URL + credential/token handling, lazy token retrieval).
  - `Utils/requestHelper.py` — `RequestHelper`, all HTTP verbs and content types.
  - `Utils/response.py` — `Response` base class (`status`, `status_code`, `message`, `message_detail`, `data`, `response`).
  - `Utils/response_version.py` — `ResponseVersion` enum (`V1`–`V4`) used only by the V4 services.
- Service packages (one directory each):
  `AcceptReject`, `AccountUser`, `Auth`, `Balance`, `Cancelation`, `CancelationRetentions`, `Csd`, `Issue`, `Pdf`, `Pendings`, `Relations`, `Stamp`, `StampRetentions`, `StatusCfdi`, `Storage`, `Validate`.
- Tests: `Test/` (one `test_<service>.py` per service) plus `Test/config.py`, `Test/base.py` and fixtures in `Test/resources/`.
- Docs: `README.md` is the user-facing manual, organized per service with runnable snippets. It is large (~2600 lines) and is the de-facto API reference. `MIGRACION.md` lists every rename the 1.0 introduced.
- No `requirements.txt`, no lockfile, no CI workflow, no linter/formatter config. The only third-party runtime dependency is `requests` (declared in `setup.py` as `install_requires`), plus `setuptools` for packaging.

### The 3-files-per-service pattern (mandatory)
Every service package follows the same layout:

```
<Servicio>/
  __init__.py            # empty, or a one-line module docstring
  <Servicio>.py          # public class, extends Utils.Services.Services
  <Servicio>Request.py   # static methods: build endpoint + payload, call RequestHelper
  <Servicio>Response.py  # class extending Utils.response.Response, parses requests.Response
```

Responsibilities are strictly separated:
- `<Servicio>.py` — the only class the consumer instantiates. Its `__init__` calls `super().__init__(url, token, user, password)` and every public method is a one-liner delegating to `<Servicio>Request`, passing `self.get_url()` and `self.get_token()`.
- `<Servicio>Request.py` — a plain class (not a `Services` subclass) whose members are all `@staticmethod`. It concatenates `url + path`, builds the `payload` dict, calls a `RequestHelper` helper, and wraps the raw `requests.Response` in `<Servicio>Response(response)`.
- `<Servicio>Response.py` — subclasses `Response`; the constructor takes the raw `requests.Response` and populates the inherited attributes.

Variants of the same service live in the same package as extra files rather than new directories — e.g. `Stamp/StampV4.py` + `Stamp/StampRequestV4.py` reuse `Stamp/StampResponse.py`, and `Issue/IssueV4.py` + `Issue/IssueRequestV4.py` reuse `Issue/IssueResponse.py`.

Documented deviations that exist today (do not "fix" them as a side effect of another change):
- `StatusCfdi/StatusCfdi.py` does **not** extend `Services` (no auth token needed; the URL of the SOAP service is a parameter, and the test environment exposes it at `https://api.test.sw.com.mx/ConsultaCFDIService.svc`) and `StatusCfdiResponse` does **not** extend `Response`; it parses the SAT SOAP envelope by string splitting and exposes `status_code_sat`, `is_cancelable`, `state`, `cancelation_status`.
- `StatusCfdi/StatusCfdiRequest.py` builds its own `requests.Session` instead of using `RequestHelper`, and calls with `verify=False`.
- `Balance/BalanceResponse.py` declares two response classes (`BalanceResponse`, `AccountBalanceResponse`) in one file, plus the `Data` / `LastTransaction` payload DTOs.
- `Pdf/RegeneratePdfResponse.py` adds no attributes or getters of its own: it only sets the inherited
  `status` / `message` / `message_detail`, unlike `PdfResponse`, which exposes uuid, content and dates.
  Filling that gap is pending confirmation that the service actually returns those fields.

### Base classes

`Utils.Services.Services` — every service class extends it:
- Constructor signature: `__init__(self, url, token=None, user=None, password=None)`. The four services that also take the API host (`AccountUser`, `Balance`, `Pdf`, `Storage`) take `url_api` as the second parameter, before `token`.
- Precedence: if `user` **and** `password` are given they win and `token` is ignored; otherwise `token` is stored with `expiration_date = 9999999999`. If neither is supplied it only `print`s `"Se debe definir user y password o token"` — it does not raise.
- `get_token()` lazily authenticates via `AuthRequest.authenticate(url, user, password)` when there is no token or the stored `expiration_date` has passed, then caches `token` and `expiration_date`.
- Accessors: `get_url()`, `get_user()`, `get_password()`, `get_token()`.
- Attributes are declared as class-level attributes (`url = None`, `token = None`, ...) and assigned on the instance in `__init__`.

`Utils.response.Response` — every response class extends it (except `StatusCfdiResponse`):
- Attributes: `status`, `status_code`, `message`, `message_detail`, `data`, `response`.
- Getters: `get_status()`, `get_status_code()`, `get_message()`, `get_message_detail()`, `get_data()`, `get_response()`.
- Subclasses add their own attributes and getters when the payload deserves them (`AuthResponse.get_token()` / `get_time_expire()`, `PdfResponse.get_uuid()` / `get_content_b64()` / ..., `PendingsResponse.get_uuids()`).

### Services that take two URLs
`AccountUser`, `Balance`, `Pdf` and `Storage` take `(url, url_api, token=None, user=None, password=None)`. `url` (the services host) is passed to `Services` and is used only to obtain the token; the actual requests are issued against `self.url_api`. Their `__init__` stores `url_api` and `print`s `"Debe especificar la url_api"` when it is missing.

### RequestHelper (`Utils/requestHelper.py`)
All helpers are `@staticmethod`, use `RequestHelper._get_session()` (a `requests.Session` with an `HTTPAdapter` mounted on `https://`), and pass `verify=True, timeout=300` — except the two V4 helpers, which call `requests.post` directly with no session, no explicit `verify` and no timeout.

| Helper | Verb | Content-Type | Notes |
| --- | --- | --- | --- |
| `post_json_request_without_headers(endpoint, payload, headers=None)` | POST | caller-supplied | Used by `AuthRequest` (no bearer token yet). |
| `post_json_request(endpoint, token, payload=None)` | POST | `application/json` | Adds `Authorization: bearer <token>`, `Cache-Control: no-cache`. |
| `post_jsontoxml_request(endpoint, token, payload=None)` | POST | `application/jsontoxml; charset=utf-8` | Sends `payload.encode('utf-8')`; used by the v3 JSON issue. |
| `get_json_request(endpoint, token, payload=None)` | GET | `application/json` | |
| `delete_json_request(endpoint, token, payload=None)` | DELETE | `application/json` | |
| `put_json_request(endpoint, token, payload=None)` | PUT | `application/json` | |
| `post_multipart_request(endpoint, token, xml_data)` | POST | `multipart/form-data; boundary=<30 random chars>` | Standard path for XML stamping/cancelling/validating. Uses `Authorization: Bearer <token>`. |
| `post_v4(endpoint, content, token=None, headers=None)` | POST | multipart, boundary generated | V4 XML services; merges caller `headers` over the defaults. |
| `post_v4_json(endpoint, content, token=None, headers=None)` | POST | `application/jsontoxml; charset=utf-8` | V4 JSON services; `dict` content is `json.dumps(..., ensure_ascii=False)`-ed. |
| `_create_multipart_body(content, boundary)` | — | — | Private; builds the `name="xml"; filename="xml"` part and returns `bytes`. |

`Validate/headers_validator.py` provides `HeaderValidator` with `validate_custom_id`, `validate_email`, `validate_extra` and `get_headers(custom_id, email, extra)`; it returns a dict with the keys `customid`, `email`, `pdf` and raises `ValueError` on invalid input. Note that nothing in the project uses it today, and the V4 tests build these header dicts by hand.

## Build, Test, and Lint Commands

### Prereqs
- Python 3.11 or newer (`README.md` declares 3.11+; development and testing happen on 3.14). `setup.py` sets `python_requires=">=3.8"`, which is the install floor, not the supported range.
- `pip install requests` — the only runtime dependency actually imported.
- `setuptools` for packaging. It is **not** bundled with Python 3.12+, so `python setup.py ...` needs it installed explicitly in the environment.

There is no virtualenv, `requirements.txt` or environment bootstrap script committed. Install dependencies manually.

### Build / packaging
- Packaging is declared in `setup.py` with `setuptools.find_packages(exclude=["Test"])`; `README.md` is read as `long_description` through a `with open(...)` block.
- `setup.py` declares `install_requires=["requests"]`, `python_requires=">=3.8"`, `license="MIT"` and the author/contact fields. There is no `License ::` classifier — the deprecated one was removed in favour of the `license` field.
- `python setup.py sdist bdist_wheel` is the only build entry point. The package is **not** published to PyPI; consumers clone the repository or copy the service directories they need.
- `.gitignore` covers `*.pyc`, `*.pyo`, `dist/`, `build/`, `MANIFEST`, `pytest_cache/`, `unittest_cache/`, `.vscode/`, `.idea/`, `sw_sdk_python.egg-info/`, `Test/resources/filePdf.pdf`.

### Tests
Tests are `unittest.TestCase` classes. **They are integration tests: every one performs a real HTTP call against the SW test environment.**

All environment reading happens in `Test/config.py`. Required variables:
- `SDKTEST_USER` — test-account user/email.
- `SDKTEST_PASSWORD` — test-account password.
- `SDKTEST_TOKEN` — a valid bearer token for the same account.

Optional variables, also read in `Test/config.py`:
- `SDKTEST_CSD_PASSWORD` — overrides the default password of the SAT public test CSD.
- `SDKTEST_USER_LIFECYCLE` — enables the destructive user create/update/delete tests.
- `SDKTEST_CSD_DELETE` — enables the destructive certificate-disable test.

`Test/base.py` defines `SdkTestCase`, which raises `ValueError("Falta la variable de entorno <NOMBRE>")` in `setUpClass` when a required one is missing.

Set them before running (PowerShell):
```powershell
$env:SDKTEST_USER="<user>"; $env:SDKTEST_PASSWORD="<password>"; $env:SDKTEST_TOKEN="<token>"
```

Run from the **repository root** — fixtures are opened with root-relative paths such as `Test/resources/xml40Stamp.xml`:

- Single test file:
  - `python Test/test_stamp.py`
  - `python Test/test_v4_services.py`
- Discovery over the whole suite:
  - `python -m unittest discover -s Test -p "test_*.py"`
- Single test case / method:
  - `python -m unittest Test.test_auth.TestAuth.testAuth_success`

Every test module guards its runner with `if __name__ == '__main__':` and exits with `sys.exit(not result.wasSuccessful())`, so importing a module does not run its tests.

A full run takes roughly 5–10 minutes and depends on the load of the test environment. Some tests are inherently timing-dependent — `test_issue_json_with_pdf` waits up to 300 s for the ADT to generate a PDF — and can fail on a loaded environment while passing in isolation. Re-run before treating such a failure as a regression.

### Test configuration and helpers
- `Test/config.py` holds the URLs, the environment reading and the test data (RFC, certificate number, UUIDs, invalid identifiers). **Do not hard-code any of this in a test module.** Its docstring explains why the UUIDs are tied to the test account: the datawarehouse is partitioned per account, so a comprobante stamped elsewhere does not resolve with this token.
- `Test/base.py` holds `SdkTestCase`, which every credential-using test class extends. It provides `expected` / `expectedError`, the URLs and credentials, the environment validation, `open_file(pathFile)`, `search_cfdi(filtro)` (walks the datawarehouse backwards in 28-day windows and returns the first record matching `filtro`), `stamped_uuid()` and `stamped_cfdi(cancelado)` (both built on it: the UUID of a recent comprobante, and the whole record of a vigente or cancelled one) and `first_user()` (the account's first child user).
- Per-class knobs instead of duplicated code: `exigePdf = True` makes `stamped_uuid()` require a comprobante that has a PDF (`TestPdf`), and `requeridas` narrows the required environment variables (`TestAuth` does not use a token).
- `Test/test_statusCfdi.py` needs no credentials for the SOAP call itself, but extends `SdkTestCase` with `requeridas = ("SDKTEST_TOKEN",)`: it builds the expresión impresa from a comprobante of the account through `stamped_cfdi()`, instead of hard-coding someone else's.
- Each test module still starts with the `sys.path` bootstrap:
  ```python
  PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
  sys.path.append(PROJECT_ROOT)
  ```
  **This cannot be moved into the `Test` package.** It is what puts the repository root on `sys.path`, so it has to run before any `from Test import ...`. Removing it breaks `python Test/test_auth.py`. Keep it identical in all modules.

### Lint
- No linting or formatting tooling is configured (no `flake8`, `ruff`, `black`, `pylintrc`, `pyproject.toml`, `setup.cfg`, pre-commit hooks or GitHub Actions). Match the surrounding code style.

## Coding Style and Conventions

### Language and Runtime
- Python 3, standard library + `requests`. No async, no dataclasses, no ABCs, no external HTTP wrappers.
- Type hints are used only in the newer code (`Utils/requestHelper.py` V4 helpers, `Utils/response_version.py`, `Validate/headers_validator.py`, `Stamp/StampV4.py`, `Issue/IssueV4.py`, `Issue/IssueRequestV4.py`, `Stamp/StampRequestV4.py`). The older services have no annotations. Follow whichever convention the file you are editing already uses.

### Formatting
- 4 spaces indentation, no tabs.
- Files end without a trailing newline in many cases; do not reformat files you are not otherwise changing.
- Spacing around `=` in keyword defaults is inconsistent (`def stamp_v1(self, xml, b64 = False)` in older files, `def stamp(self, xml: str, headers: dict = None)` in V4 files). Match the file.
- Argument lists in older `Request` classes are frequently written without spaces after commas.
- Conditions are often parenthesized (`if(self.status_code == 200):`) in response constructors.
- Keep classes small: service classes are typically 10–30 lines of pure delegation.
- Comments are in Spanish, accented, written as `#Texto` without a space after the `#`. Test files group their cases under `#UT <área>` headings.

### File and Module Organization
- One class per file, file name == class name (`Stamp/Stamp.py` → `class Stamp`), except where noted above.
- Packages are top-level and named after the service in `PascalCase`, with no underscores.
- `__init__.py` is either empty or a single triple-quoted docstring. Nothing is re-exported from `__init__.py`, so consumers import the full path: `from Stamp.Stamp import Stamp`.
- Helper/DTO classes that shape a JSON payload live next to the response that builds them (`Data`, `LastTransaction` in `Balance/BalanceResponse.py`; `DataItem`, `DataList` in `AccountUser/AccountUserResponse.py`).

### Naming
- Classes: `PascalCase` (`Stamp`, `StampRequest`, `StampResponse`, `RequestHelper`, `HeaderValidator`).
- Modules mirror class names, so module names are `PascalCase` too — except `Utils/requestHelper.py`, `Utils/response.py`, `Utils/response_version.py`, `Validate/headers_validator.py`, `Test/config.py` and `Test/base.py`, which are lowercase/snake_case.
- **Methods and attributes of the public API are `snake_case`, in English, with no exceptions.** The 1.0 removed every `PascalCase`, `camelCase` and Spanish name from the public surface, without keeping aliases. `MIGRACION.md` has the full old → new table; consult it before assuming a name.
- Payload-facing values follow the API's JSON casing where they mirror the wire (`b64Cer`, `b64Key`, `b64Pfx`, `idUser`, `taxId`, `notificationEmail`, `isUnlimited`, `foliosustitucion`). **The JSON keys themselves are never renamed**: `self.response["messageDetail"]` and `data['contentB64']` keep the service's spelling even though the attributes they feed are `message_detail` and `content_b64`.
- Private helpers are prefixed with a single underscore (`RequestHelper._get_session`, `RequestHelper._create_multipart_body`, `AccountUserRequest._pathBase`).
- Test classes: `Test<Service>` (`TestStamp`, `TestAuth`, `TestAccountUser`, `TestV4Basic`). Test methods: `test<Service>_<scenario>` or `test_<scenario>`; the service part is the method name in `PascalCase` (`testAcceptRejectCsd_auth` tests `accept_reject_csd`). Suffix `_auth` marks the user/password variant, no suffix marks the token variant.

### Imports
- Absolute imports rooted at the repository top level; no relative imports anywhere.
- Order used in service files: the sibling `Request`/`Response` module first, then `Utils`:
  ```python
  from Stamp.StampRequest import StampRequest
  from Utils.Services import Services
  ```
  Newer V4 files put `Utils` first; either is acceptable, match the file.
- Standard-library imports (`json`, `traceback`, `typing`) go at the top of response/helper modules.
- Test modules import `from Test import config` and `from Test.base import SdkTestCase` after the `sys.path` bootstrap, before the SDK imports.

### Error Handling
- **Responses never raise.** Every `<Servicio>Response.__init__` wraps its whole body in `try: ... except: traceback.print_exc()`. Parsing failures are printed, not propagated, so the caller may receive a response object with `None` attributes.
- The standard response-parsing shape, replicated in nearly every response class:
  ```python
  self.status_code = response.status_code
  if(bool(response.text and response.text.strip())):
      self.response = json.loads(response.text.encode().decode('utf8'))
      if(self.status_code == 200):
          self.data = self.response["data"]
          self.status = self.response["status"]
      else:
          self.status = self.response["status"]
          self.message = self.response["message"]
          if "messageDetail" in self.response:
              self.message_detail = self.response["messageDetail"]
  else:
      self.status = "error"
      self.message = response.reason
      self.message_detail = response.request
  ```
  `messageDetail` is always read defensively with `if "messageDetail" in self.response`.
- Special cases: `AccountUserResponse` handles `204 No Content` by setting `status = "success"`, `status_code = 200`, `data = "Usuario Eliminado con exito"`; `PdfResponse` and `ValidateResponse` use an inner `try/except` around the success branch and fall back to just setting `status`.
- Configuration problems in `Services` / `AccountUser` / `Balance` / `Pdf` / `Storage` constructors are reported with `print(...)` in Spanish, not exceptions. This is a known defect scheduled for the next PR — do not rely on it, and do not extend the pattern to new code.
- `HeaderValidator` is the only component that raises (`ValueError`) as its documented contract.
- Callers therefore check `response.get_status() == "success" | "error"` rather than catching exceptions.

### HTTP and Serialization
- All HTTP goes through `requests`, funnelled through `Utils/requestHelper.py` (the sole exception is `StatusCfdiRequest`).
- Auth header casing is inconsistent by design of the existing code: `bearer {token}` (lowercase) for the JSON/GET/PUT/DELETE helpers, `Bearer {token}` for multipart and V4 helpers.
- XML payloads are sent as `multipart/form-data` with a 30-character random boundary and the part named `xml`; the body is encoded to UTF-8 bytes.
- JSON payloads are passed as plain `dict`s to `requests`' `json=` argument; `json.dumps(..., ensure_ascii=False)` is only used where the API expects `application/jsontoxml`.
- Responses are deserialized with `json.loads(response.text.encode().decode('utf8'))` — keep this idiom for consistency.
- Endpoints are built by string concatenation or f-strings inside the `Request` class. There is no URL normalization helper; the caller's URL is used verbatim.
- V4 paths embed the response version through the enum: `f"/v4/cfdi33/stamp/{str(version)}"` — `ResponseVersion.__str__` returns `"v1"`..`"v4"`.
- Base64 variants are selected by appending `/b64` to the path when the `b64`/`base64` flag is `True` (see `StampRequest.stamp`, `IssueRequest.issue`).

### Optional Parameters and Defaults
- **All fifteen service constructors have the same shape**: `(url, token=None, user=None, password=None)`, with `url_api` inserted second for the four API-host services. No service takes a positional-required `token` any more, so `Service(url, user="...", password="...")` works everywhere.
- `Auth` accepts a `token` parameter for signature consistency but ignores it: it passes `None` to `Services` and authenticates with user/password.
- V4 service methods default to `headers: dict = None` and `version: ResponseVersion = ResponseVersion.V1`.
- Keep new overload-style methods consistent with the existing pair (token vs user/password) so both auth modes remain usable.

## Tests
- Framework: `unittest` from the standard library. No pytest, no mocks, no fixtures framework, no VCR/cassettes — all calls go to the live test environment. **Do not add simulated responses**; fakes are for verifying locally, never for committing.
- One test module per service in `Test/`, named `test_<service>.py` (camelCase kept where the service uses it: `test_acceptReject.py`, `test_accountUser.py`, `test_statusCfdi.py`).
- Each module defines a `Test<Service>(SdkTestCase)` class. `expected = "success"` and `expectedError = "error"` are inherited, not redeclared.
- Assertions are mostly `assertTrue(self.expected == response.get_status())` plus `assertIsNotNone(...)`; the newer modules use `assertEqual`, `assertIn`, `assertIsNone`. An error case must assert the error, not merely that a field is not `None`.
- Fixture files are read with the inherited `open_file(pathFile)`, always UTF-8, always with root-relative paths under `Test/resources/`.
- Data the test needs from the account (a stamped UUID, a child user) is looked up at run time through `stamped_uuid()` / `first_user()` — never hard-coded.
- `test_v4_services.py` rewrites the `Fecha` attribute/key of `xml40.xml` and `cfdi.json` to *now minus one hour* before sending, and generates unique `customid` values via `generate_custom_id(prefix)`. `test_issue.py` makes each emission unique through its `Folio`.
- Destructive tests are gated with `@unittest.skipUnless(config.USER_LIFECYCLE, ...)` / `@unittest.skipUnless(config.CSD_DELETE, ...)` rather than an unconditional skip, so they can be run deliberately. Keep them gated.
- Idempotency is handled by accepting the known error: stamping the same XML twice returns `"307. El comprobante contiene un timbre previo."`, and tests assert either success or that message.
- `Test/resources/` holds the shared fixtures: `xml40.xml`, `xml40Stamp.xml`, `cfdi.json`, `retenciones20.xml`, `cancelByXml.xml`, `cancelRetByXml.xml`, `fileAcceptReject.xml`, `fileRelations.xml`, `filePdf.xml`, `b64CSD.txt`, `b64Key.txt`, `b64Pfx.txt`. `Test/resources/filePdf.pdf` is written by `test_pdf.py` at runtime and is ignored by git.
- `Test/resources/fileRelations.xml` is not used by any test today; it is pending a decision to wire it up or delete it.

## Repository-Specific Notes
- The repository root doubles as the package root, so imports are `from <Servicio>.<Servicio> import <Servicio>`. Anything that changes directory names is a breaking change for consumers and belongs in `MIGRACION.md`.
- Credentials are never committed; the only supported way to run the suite is via the `SDKTEST_*` variables.
- Token lifetime: `Auth` issues a 2-hour token (documented in `README.md`); `Services.get_token()` re-authenticates automatically only when it holds `user`/`password`. A token supplied directly is treated as never expiring (`expiration_date = 9999999999`).
- `README.md` is the product documentation and mirrors the code closely: when you add or change a public method, the matching README section is expected to change with it. Its `:pushpin:` notes are for prerequisites, roughly one per section — not for describing the shape of the response.
- `StatusCfdi` calls the SOAP service with `verify=False` and parses XML by string splitting — this is intentional in the current code, not an oversight to be silently refactored. The TLS verification is under review with infrastructure.
- There is no logging framework: diagnostics are `print()` and `traceback.print_exc()`.
- TLS failures with `CERTIFICATE_VERIFY_FAILED` while running the suite usually come from a local antivirus intercepting TLS, not from the library. Retry before investigating.
- No Cursor rules found in `.cursor/rules/` or `.cursorrules`. No GitHub Copilot instructions found in `.github/copilot-instructions.md`. There is no `.github/` directory at all.

## Adding New Code

To add a new service:
1. Create a top-level directory named after the service in `PascalCase`, without underscores.
2. Add `__init__.py` (empty, or a one-line docstring in the style of `Stamp/__init__.py`).
3. Add `<Servicio>.py` with a class extending `Services`:
   ```python
   from <Servicio>.<Servicio>Request import <Servicio>Request
   from Utils.Services import Services

   class <Servicio>(Services):
       def __init__(self, url, token = None, user = None, password = None):
           super(<Servicio>, self).__init__(url, token, user, password)

       def my_operation(self, arg):
           return <Servicio>Request.my_operation(self.get_url(), self.get_token(), arg)
   ```
   Use `super(<Servicio>, self).__init__(...)` — the old-style form is what the whole repo uses. If the service targets the API host, take `url_api` as the second constructor parameter and mirror `Balance` / `Pdf` / `AccountUser` / `Storage`.
4. Add `<Servicio>Request.py` with `@staticmethod`s only: build `endpoint`, build `payload`, call the appropriate `RequestHelper` helper, return `<Servicio>Response(response)`. Do not call `requests` directly — add a helper to `RequestHelper` if no existing one fits.
5. Add `<Servicio>Response.py` extending `Response`, following the standard parsing shape above (including the bare `except: traceback.print_exc()`), and add getters only for the extra attributes you introduce. Name the attributes in `snake_case` even when the JSON key they read is not.
6. Add `Test/test_<servicio>.py` with a `Test<Servicio>(SdkTestCase)` class and the `sys.path` bootstrap, one test per auth mode (`_auth` for user/password, plain for token) and at least one error case. Put URLs and test data in `Test/config.py`, not in the module. Put any fixture under `Test/resources/`.
7. Document the service in `README.md` in the same style as the surrounding sections (description, code snippet, sample response).

To extend an existing service:
- Add the public method to `<Servicio>.py` and the matching `@staticmethod` to `<Servicio>Request.py`; reuse the existing `<Servicio>Response`.
- For a whole new API version, add `<Servicio>V4.py` + `<Servicio>RequestV4.py` inside the existing package and reuse the existing response class, following `Stamp/StampV4.py` and `Issue/IssueV4.py`.
- Do not add dependencies: `requests` and the standard library are the whole toolbox today.
- If you rename anything on the public surface, add the old → new row to `MIGRACION.md` in the same change.

## Example Paths to Reference
- Canonical 3-file service: `Stamp/Stamp.py`, `Stamp/StampRequest.py`, `Stamp/StampResponse.py`
- V4 variant inside an existing package: `Stamp/StampV4.py`, `Stamp/StampRequestV4.py`, `Issue/IssueV4.py`, `Issue/IssueRequestV4.py`
- Base service and auth/token flow: `Utils/Services.py`, `Auth/Auth.py`, `Auth/AuthRequest.py`, `Auth/AuthResponse.py`
- Response base class and getters: `Utils/response.py`, `Pdf/PdfResponse.py`
- HTTP helpers: `Utils/requestHelper.py`
- Response version enum: `Utils/response_version.py`
- Two-URL service (services host + API host): `Balance/Balance.py`, `AccountUser/AccountUser.py`, `Pdf/Pdf.py`, `Storage/Storage.py`
- Nested payload DTOs: `Balance/BalanceResponse.py`, `AccountUser/AccountUserResponse.py`
- Header validation: `Validate/headers_validator.py`
- Non-`Services` service (SOAP/SAT): `StatusCfdi/StatusCfdi.py`, `StatusCfdi/StatusCfdiRequest.py`, `StatusCfdi/StatusCfdiResponse.py`
- Test configuration and shared helpers: `Test/config.py`, `Test/base.py`
- Test style: `Test/test_stamp.py`, `Test/test_pdf.py`, `Test/test_v4_services.py`
- Gated destructive tests: `Test/test_accountUser.py`, `Test/test_csd.py`
- Rename log: `MIGRACION.md`
