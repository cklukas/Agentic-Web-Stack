# Trust Model

The trust model defines what evidence is required before an agent, tool, or service is allowed to participate in a workflow.

Trust is not binary. A public Agent Card may be discoverable, but production use often requires stronger evidence from identity, registry, policy, evaluation, and operations layers.

## Trust Levels

| Level | Meaning | Typical evidence |
| --- | --- | --- |
| Public | Metadata can be read, but use is not approved by default | Agent Card, public docs |
| Verified | Domain, version, and ownership are checked | HTTPS origin, signed or cached metadata, known provider |
| Organization-approved | Use is allowed under local policy | Registry entry, required scopes, review status |
| Restricted | Use requires extra approval or environment controls | Human review, private catalog, policy gateway |

## Trust Evidence

- Discovery evidence: Agent Card, OpenAPI, well-known metadata.
- Identity evidence: issuer, subject, audience, scopes, expiry.
- Registry evidence: approved domain, version, trust level, review metadata.
- Runtime evidence: trace ID, audit events, policy decisions, artifact references.
- Evaluation evidence: scenarios for happy path, auth denial, prompt injection, tool failure, and stale discovery metadata.

## Related Pages

- [Agent Registry](./agent-registry.md)
- [Identity Delegation](./identity-delegation.md)
- [Evaluation](./evaluation.md)
- [Security and Trust](/guides/security-trust)
