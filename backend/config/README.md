# Backend Global Configuration (`backend/config`)

This package contains cross-cutting framework configurations:
- `SecurityConfig`: Spring Security OAuth2 / JWT stateless authentication filter chains.
- `WebConfig`: CORS policy definitions, REST template / WebClient bean definitions.
- `KafkaConfig`: Producer/Consumer factory setups, topic definitions, deserializers.
- `RedisConfig`: Redis CacheManager, serialization templates.
- `SwaggerConfig`: OpenAPI 3.0 API documentation configuration.
