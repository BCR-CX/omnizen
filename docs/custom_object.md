# Custom Object

In Omnizen, a Custom Object is a flexible data structure that allows you to define and manage custom data types. This is particularly useful for applications that require dynamic and user-defined data models.

## Custom Object

### Default Fields

-   id: str
-   name: str
-   created_at: datetime
-   created_at_user_id: str
-   updated_at: datetime
-   updated_at_user_id: str
-   photo: Optional[Photo]
-   external_id: Optional[str]

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

The `filter` method allows you to build complex queries using logical operators like `and`, `or`, and conditions like `eq`, `ne`, `lt`, `gt`, etc. You can chain these methods to create a comprehensive filter for your ticket queries.

### Example

```python
    Teste.filter()
    .and_()
    .eq("status", "active")
    .lt("age", 30)
    .or_()
    .eq("role", "user")
    .lt("age", 20)
    .add(Teste.filter().eq("name", "John").ne("status", "inactive"))
    .add(Teste.filter(operator="$or").eq("role", "admin").gt("age", 25))
    .add(Teste.filter().or_().eq("name", "Alice").eq("name", "Bob"))
    .add(Teste.filter().and_().eq("status", "active").gte("age", 18))
```

```python
    Teste.filter({
        "where": {
            "OR": [
                {"status": "active"},
                {"status": "inactive"},
                {"role": "user", "age": {"$lt": 30}},
            ],
            "AND": {
                "age": {"$gt": 18},
                "role": "admin",
            },
        },
        "page_size": 100,
        "after_cursor": "cursor_value",
        "before_cursor": "cursor_value",
        "order_by": {"created_at": "desc"}
        }
        )
```
