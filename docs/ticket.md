# Ticket

In Omnizen, a Ticket represents a support request or issue that can be created, updated, and managed. Tickets can be of different types such as `Ticket`, `Incident`, or `Problem`. Each type has its own specific fields and properties.

## Ticket

### Creation Fields

-   email_ccs: {"user_email": str, "action": Enum} | {"user_id": int, action: Enum}
-   subject: str
-   comment: Comment
-   priority: Enum
-   type: Enum
-   tags: list[str]
-   requester: {"email": str, "name": str, "phone": str} # passar email ou telefone obrigatoriamente / passar requester ou requester_id
-   requester_id: int # passar requester ou requester_id
-   status: Enum # passar custom_status_id ou status
-   custom_status_id: Optional[str] # passar custom_status_id ou status
-   brand_id: Optional[int]
-   group_id: Optional[int]
-   assignee_id: Optional[int]

### Default Fields

-   id: int
-   requester_id: int
-   description: str
-   created_at: datetime
-   updated_at: datetime
-   priority: Enum
-   status: Enum
-   custom_status_id: int
-   type: Enum
-   brand_id: int
-   assignee_id: Optional[int]
-   external_id: Optional[str]
-   group_id: Optional[int]

### Default Properties

-   attachments: list[Attachment]
-   comments: list[Comment]
-   events: list[Event]
-   custom_status: {"id": int, "name": str}
-   tags: list[str]

## Incident(Ticket)

### Creation Fields

-   problem_id: Optional[int]

### Default Fields

-   problem_id: Optional[int]

## Problem(Ticket)

### Default Properties

-   incidents: list[Incident]

## CRUD Methods

-   save: Create or update
-   delete: Delete
-   refresh: Refresh the ticket
-   get: Get by id
-   all: Get all
-   search: Search tickets
-   filter: Filter tickets
-   count: Count tickets
-   bulk_create: Create multiple tickets
-   bulk_update: Update multiple tickets
-   bulk_delete: Delete multiple tickets

### NOTE: All methods had a async version, e.g., `save_async`, `delete_async`, etc.

## Filter

The `filter` method allows you to build queries using conditions like `eq`, `ne`, `lt`, `gt`, etc. You can chain these methods to create a comprehensive filter for your ticket queries.

### Example

```python
    Teste.filter()
    .eq("status", "active")
    .lt("age", 30)
    .eq("role", "user")
    .lt("age", 20)
    .add(Teste.filter().eq("name", "John").ne("status", "inactive"))
    .page_size(100)
    .after_cursor("cursor_value")
    .before_cursor("cursor_value")
    .order_by({"created_at": "desc"})
```

```python
    Teste.filter(
        "where": [
                {"status": "active"},
                {"status": "inactive"},
                {"role": "user"},
                {"age": {"$lt": 30}}
                {"age": {"$gt": 18}},
                {"role": "admin"},
        ],
        "page_size": 100,
        "after_cursor": "cursor_value",
        "before_cursor": "cursor_value",
        "order_by": {"created_at": "desc"}
        )
```
