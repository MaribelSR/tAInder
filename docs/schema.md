```mermaid
---
title: Schema
---
erDiagram
    PROFILE ||--o{ MESSAGE : write
    MESSAGE |o..o| MESSAGE : reply
    AI |o--|| PROFILE : uses
    USER |o--|| PROFILE : uses
    MATCH }o--|| PROFILE : "links to user Profile"
    MATCH }o--|| PROFILE : "links to ai Profile"
    MATCH ||--o{ MESSAGE : contains
    TAG }o..o{ PROFILE : have
    TAG }o--|| TAG_CATEGORY : contain

    PROFILE {
        int id PK
        string(150) username
        string(150) first_name
        string(150) last_name
        int height
        date birthday
        string(1024) description
        datetime last_access
        int[] tags
    }

    USER {
        int id PK
        string(254) email UK
        string(128) password
        int profile_id
    }

    AI {
        int id PK
        int profile_id
        datetime last_execution
    }

    MATCH {
        int id PK
        int ai_profile_id FK
        int user_profile_id FK
        boolean do_match
        string(1024) summary
    }

    MESSAGE {
        int id PK
        string msg
        datetime published
        boolean deleted
        int replied_message_id FK
        int profile_id FK
        int match_id FK
        boolean summarized
    }

    TAG {
        int id PK
        string name UK "UK with tag_category id"
        int tag_category_id FK,UK "UK with name"
    }

    TAG_CATEGORY {
        int id PK
        string name UK
    }
```
