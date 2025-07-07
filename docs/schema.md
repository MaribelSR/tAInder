```mermaid
---
title: Schema
---
erDiagram
    PROFILE ||--o{ MESSAGE : write
    THREAD ||--|{ MESSAGE : contains
    AI |o--|| PROFILE : uses
    USER |o--|| PROFILE : uses
    MATCH }o--|| PROFILE : "do PROFILE_A"
    MATCH }o--|| PROFILE : "do PROFILE_B"

```
