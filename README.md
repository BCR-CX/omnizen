# Omnizen

**Omnizen** is a Python library that provides a high-level (ORM-like) interface for working with the [Zendesk API](https://developer.zendesk.com/). The goal is to simplify the creation, retrieval, update, and deletion of Zendesk resources, with an initial focus on **Tickets** and **Custom Objects**.

---

## ✨ Purpose

To offer a simple, readable, and Pythonic way to integrate with Zendesk, abstracting the REST API behind intuitive models and methods.

---

## ⚙️ Planned Features

### 🎫 Tickets

-   [ ] Create tickets with standard and custom fields
-   [ ] Update and delete tickets
-   [ ] Filter/search tickets using query parameters
-   [ ] Support for tags, requester, and organization

### 🧱 Custom Objects

-   [ ] Define custom object models using Python classes
-   [ ] Full CRUD support for custom object records
-   [ ] Automatic field serialization
-   [ ] Support for `external_id`, `created_by`, `updated_by`, and relationships

### 🧰 Utilities

-   [ ] Built-in HTTP client with retry logic and authentication
-   [ ] Error mapping for common Zendesk API responses
-   [ ] Dynamic schema support in an ORM-like style

---

## 🚧 Work in Progress

This library is under active development. Use with caution. Contributions are welcome!
