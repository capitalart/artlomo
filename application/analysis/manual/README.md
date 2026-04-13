# Manual Workflow

Purpose: handle manual analysis of uploaded artwork while respecting workflow isolation and service-first design.

## v1 Scope (Foundation Phase)

- Create manual workflow structure (routes, services, UI placeholder, errors).

- Provide entrypoint from Upload gallery via `/manual/process/<slug>`.

- Render a workspace page for a given slug with placeholder preview and metadata form.

- Stub service methods for promotion, loading, saving metadata, and mockup enqueueing without heavy side effects.

## v2 Scope (Deferred)

- Locking, deletion, and bulk navigation.

- Cross-workflow mutations beyond minimal registry/mockup integration.

- Full legacy parity and deeper persistence flows.

## Explicit Non-Goals

- No business logic in routes; services own behavior.

- No cross-workflow imports; depend only on `application/common`, `application/utils`, and configuration.

- No filesystem writes or irreversible actions beyond validated placeholders in this phase.
