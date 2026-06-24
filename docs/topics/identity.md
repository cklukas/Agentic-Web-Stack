# Identity

## Topic Summary

The identity layer controls how agents authenticate, receive authorization, and act with scoped permissions on behalf of users, organizations, or services.

## Stack Level

Identity is Layer 2 of the Agentic Web Stack. It decides who is calling, which user or organization is being represented, which scopes or policies apply, and how an agent proves that it is allowed to access a protected resource.

## Goals

- Demonstrate secure access to protected resources.
- Preserve user identity and permission boundaries during delegated agent actions.
- Explain how identity standards constrain agent access.

## Common Tech Stack

| Technology | Role in identity |
| --- | --- |
| OAuth2 | Delegated authorization for scoped access to APIs and agent services |
| OpenID Connect | Authentication and identity claims on top of OAuth2 |
| JWT | Token format commonly used for access tokens, ID tokens, and signed claims |
| JWK and JWKS | Public key publishing and token signature validation |
| API gateways | Central enforcement for auth, rate limits, routing, and audit logging |
| mTLS | Mutual service identity for high-trust internal or enterprise environments |
| OPA or policy engines | Externalized authorization policy and decision logging |

## Reference Scenario

The Literature Review Assistant uses OpenID Connect for user sign-in and OAuth2 scopes for delegated API access. The agent receives `research:read` for document retrieval and `drafts:write` only when it needs to create a human-reviewed draft.

## Related Materials

- [Security and Trust](/guides/security-trust)
- [End-to-End Demo](/guides/end-to-end-demo)
- [Specifications](/specifications/)

## Standards and Protocols

- OAuth 2.0
- OpenID Connect
- JSON Web Token
- Bearer token usage
- Scoped authorization and delegated access

## Example Use Case

An enterprise agent retrieves customer tickets and drafts a support summary. The human user signs in through OpenID Connect. The agent receives only the delegated scopes needed for ticket reading and draft creation, not broad administrative access.

## Example Authorization Specification

```yaml
identityProvider:
  issuer: https://auth.example.com/
  discoveryUrl: https://auth.example.com/.well-known/openid-configuration
client:
  name: support-summary-agent
  grantType: authorization_code
  redirectUris:
    - https://agents.example.com/oauth/callback
resourceServer:
  audience: https://api.example.com
  requiredClaims:
    - sub
    - aud
    - exp
    - scope
scopes:
  tickets:read: Read support tickets visible to the signed-in user.
  drafts:write: Create draft responses that still require human approval.
  customers:read: Read customer profile fields allowed by policy.
exampleAccessTokenClaims:
  iss: https://auth.example.com/
  aud: https://api.example.com
  sub: user_123
  azp: support-summary-agent
  scope: tickets:read drafts:write
  tenant: acme
```

Example artifact: [oidc-client.example.json](/specs/demo/oidc-client.example.json).

## Reference Links and Papers

- [Technology Origins](/references/technology-origins) - Local reference page with historical context for OAuth2, OpenID Connect, JWT, and policy technologies.
- [RFC 6749: OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749) - Core IETF OAuth2 specification for delegated authorization.
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750) - IETF specification for using bearer tokens in HTTP requests.
- [RFC 7519: JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519) - IETF specification for compact signed claims used in access tokens, ID tokens, and assertions.
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) - OpenID Foundation specification that adds identity and ID tokens on top of OAuth2.
- [OAuth 2.0 overview](https://oauth.net/2/) - Practical OAuth community overview and entry point for related specs.
- [Open Policy Agent](https://www.openpolicyagent.org/) - Open-source policy engine commonly used for authorization decisions and governance.

## Design Considerations

- Validate issuer, audience, expiry, signature, scopes, tenant, and authorized party.
- Prefer user-delegated access when an agent acts on behalf of a person.
- Use service accounts only for system-owned tasks with explicit policy boundaries.
- Keep tokens and secrets out of prompts, logs, artifacts, and retrieved memory.
