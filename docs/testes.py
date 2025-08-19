from typing import Any, Callable, Optional, Type, Union, Literal, Dict, List, TypedDict
from decimal import Decimal
from datetime import date, datetime
from pprint import pprint
from enum import Enum

from pydantic import BaseModel, model_validator, ConfigDict


class Action(str, Enum):
    add = "add"
    remove = "remove"


class Priority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class Status(str, Enum):
    new = "new"
    open = "open"
    pending = "pending"
    hold = "hold"
    solved = "solved"
    closed = "closed"


class TicketType(str, Enum):
    ticket = ""
    question = "question"
    incident = "incident"
    problem = "problem"
    task = "task"


class EmailCCByEmail(BaseModel):
    user_email: str
    action: Action


class EmailCCById(BaseModel):
    user_id: int
    action: Action


EmailCC = Union[EmailCCByEmail, EmailCCById]


class Requester(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None

    @model_validator(mode="before")
    def validate_contact(cls, data):
        if not data.get("email") and not data.get("phone"):
            raise ValueError("either email or phone must be provided")
        return data


class Comment(BaseModel):
    body: str
    author_id: Optional[int] = None


class Attachment(BaseModel):
    filename: str
    content_url: str


class Event(BaseModel):
    type: str
    data: dict


class CustomStatus(BaseModel):
    id: int
    name: str


class Ticket(BaseModel):
    # model config
    model_config = ConfigDict(extra="forbid")

    type: TicketType = TicketType.ticket

    # creation-only
    email_ccs: Optional[list[EmailCC]] = None
    subject: Optional[str] = None
    comment: Optional[Comment] = None
    requester: Optional[Requester] = None
    requester_id: Optional[int] = None
    custom_status_id: Optional[Union[int, str]] = None

    # common
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    brand_id: Optional[int] = None
    group_id: Optional[int] = None
    assignee_id: Optional[int] = None

    # read-only
    id: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    external_id: Optional[str] = None

    @property
    def events(self):
        return []

    @property
    def attachments(self):
        return self.attachments or []

    @property
    def comments(self):
        return []

    @property
    def custom_status(self):
        return None

    @property
    def tags(self):
        return self._tags or []

    @tags.setter
    def tags(self, value):
        self._tags = value

    @model_validator(mode="before")
    def validate_creation_fields(cls, values):
        if "id" not in values:
            if not values.get("requester") and not values.get("requester_id"):
                raise ValueError("either requester or requester_id must be provided")
            if not values.get("status") and not values.get("custom_status_id"):
                raise ValueError("either status or custom_status_id must be provided")
            if values.get("type") == "incident" and not values.get("problem_id"):
                raise ValueError("problem_id is required when type is incident")

        return values


try:
    ticket = Ticket(
        email_ccs=[EmailCCByEmail(user_email="example@example.com", action=Action.add)],
        subject="Test Ticket",
        comment=Comment(body="This is a test comment"),
        requester=Requester(email="example@example.com"),
        requester_id=123,
        priority=Priority.normal,
        status=Status.new,
        type=TicketType.question,
    )
except ValueError:
    print("Primeiro deu erro")

try:
    ticket = Ticket(
        email_ccs=[EmailCCByEmail(user_email="example@example.com", action=Action.add)],
        subject="Test Ticket",
        comment=Comment(body="This is a test comment"),
        requester=Requester(email="example@example.com"),
        requester_id=123,
        priority=Priority.normal,
    )
except ValueError:
    print("Segundo deu erro")


class Problem(Ticket):
    type: TicketType = TicketType.problem

    @property
    def incidents(self):
        return []


class Incident(Ticket):
    type: TicketType = TicketType.incident

    problem_id: Optional[int] = None


ALLOWED_FILTER_OPERATORS_BY_TYPE = {
    str: ["$eq", "$ne", "$in", "$nin", "$contains"],
    int: ["$eq", "$ne", "$gt", "$gte", "$lt", "$lte"],
    float: ["$eq", "$ne", "$gt", "$gte", "$lt", "$lte"],
    bool: ["$eq", "$ne"],
    date: ["$eq", "$ne", "$gt", "$gte", "$lt", "$lte"],
    Decimal: ["$eq", "$ne", "$gt", "$gte", "$lt", "$lte"],
}


class Teste(BaseModel):
    name: str
    status: str
    age: int
    role: str = ""

    @classmethod
    def filter(cls, operator: Literal["$and", "$or"] = "$and"):
        return FilterBuilder(filter_method=cls._filter, model=cls, operator=operator)

    @classmethod
    def _filter(cls, query):
        print(f"filtering with: {query}")
        return []

    @classmethod
    def map_fields_types(cls):
        return {name: f.annotation for name, f in cls.model_fields.items()}


class FilterBuilder:
    def __init__(
        self,
        *,
        model: Optional[Type[BaseModel]] = None,
        operator: Literal["$and", "$or"] = "$and",
        filter_method: Callable | None = None,
    ):
        self.operator = operator
        self.conditions: list[Union["FilterBuilder", dict]] = []
        self.model = model
        self.filter_method = filter_method

        self._page_size: int | None = None
        self._after_cursor: str | None = None
        self._before_cursor: str | None = None
        self._order_by: list[dict[str, str]] = []

    def _add_condition(self, cond: Union["FilterBuilder", dict]):
        if self.model and isinstance(cond, dict):
            map_field_type = self.model.map_fields_types()
            for key in cond.keys():
                if key not in map_field_type.keys():
                    raise ValueError(f"Invalid field: {key}")
                if isinstance(cond[key], dict):
                    for operator in cond[key].keys():
                        allowed_ops = ALLOWED_FILTER_OPERATORS_BY_TYPE.get(
                            map_field_type.get(key, str), []
                        )
                        if operator not in allowed_ops:
                            raise ValueError(
                                f"Invalid operator '{operator}' for field '{key}'"
                            )
        self.conditions.append(cond)
        return self

    def eq(self, key, value):
        return self._add_condition({key: {"$eq": value}})

    def ne(self, key, value):
        return self._add_condition({key: {"$ne": value}})

    def gt(self, key, value):
        return self._add_condition({key: {"$gt": value}})

    def gte(self, key, value):
        return self._add_condition({key: {"$gte": value}})

    def lt(self, key, value):
        return self._add_condition({key: {"$lt": value}})

    def lte(self, key, value):
        return self._add_condition({key: {"$lte": value}})

    def contains(self, key, value):
        return self._add_condition({key: {"$contains": value}})

    def and_(self):
        fb = FilterBuilder(
            model=self.model, operator="$and", filter_method=self.filter_method
        )
        fb.add(self)
        return fb

    def or_(self):
        fb = FilterBuilder(
            model=self.model, operator="$or", filter_method=self.filter_method
        )
        fb.add(self)
        return fb

    def add(self, builder: Union["FilterBuilder", dict]):
        self.conditions.append(builder)
        return self

    def page_size(self, size: int):
        self._page_size = size
        return self

    def after_cursor(self, cursor: str):
        self._after_cursor = cursor
        return self

    def before_cursor(self, cursor: str):
        self._before_cursor = cursor
        return self

    def order_by(
        self, field: Literal["created_at"], direction: Literal["asc", "desc"] = "asc"
    ):
        self._order_by.append({"field": field, "direction": direction})
        return self

    def build(self):
        and_acc = []
        or_acc = []

        def walk(node, current_op="$and"):
            if isinstance(node, FilterBuilder):
                op = node.operator
                for cond in node.conditions:
                    walk(cond, op)
            elif isinstance(node, dict):
                if current_op == "$and":
                    and_acc.append(node)
                else:
                    or_acc.append(node)
            else:
                raise ValueError("invalid condition type in build")

        walk(self)

        filter_dict = {}
        if and_acc:
            filter_dict["$and"] = and_acc
        if or_acc:
            filter_dict["$or"] = or_acc

        result: dict = {"filter": filter_dict}
        if self._page_size is not None:
            result["page_size"] = self._page_size
        if self._after_cursor is not None:
            result["after_cursor"] = self._after_cursor
        if self._before_cursor is not None:
            result["before_cursor"] = self._before_cursor
        if self._order_by:
            result["order_by"] = self._order_by

        return result

    def exec(self):
        q = self.build()
        return self.filter_method(q) if self.filter_method else q


f = (
    Teste.filter()
    .and_()
    .eq("status", "asd")
    .lt("age", "as")
    .or_()
    .eq("role", "user")
    .lt("age", 20)
    .add(Teste.filter().eq("name", "John").ne("status", "inactive"))
    .add(Teste.filter(operator="$or").eq("role", "admin").gt("age", 25))
    .add(Teste.filter().or_().eq("name", "Alice").eq("name", "Bob"))
    .add(Teste.filter().and_().eq("status", "active").gte("age", 18))
)

pprint(f.build())
print()

f = (
    Teste.filter()
    .or_()
    .eq("status", "active")
    .lt("age", 30)
    .and_()
    .eq("role", "user")
    .lt("age", 20)
    .or_()
    .eq("name", "John")
    .ne("status", "inactive")
)

pprint(f.build())
print()


f = (
    Teste.filter()
    .or_()
    .lt("age", 30)
    .and_()
    .lt("age", 20)
    .add(Teste.filter(operator="$or").eq("name", "John"))
    .eq("status", "active")
)
pprint(f.build())
print()

f = (
    Teste.filter()
    .or_()
    .lt("age", 30)
    .and_()
    .lt("age", 20)
    .add(Teste.filter(operator="$or").eq("name", "John"))
    .eq("status", "active")
    .page_size(100)
    .after_cursor("cursor_value")
    .before_cursor("cursor_value")
    .order_by("created_at", "desc")
)
pprint(f.build())
print()


Operator = Literal[
    "lt",
    "lte",
    "gt",
    "gte",
    "eq",
    "neq",
    "in",
    "not_in",
    "contains",
]

OperatorDict = TypedDict(
    "OperatorDict",
    {
        "$lt": Any,
        "$lte": Any,
        "$gt": Any,
        "$gte": Any,
        "$eq": Any,
        "$neq": Any,
        "$in": List[Any],
        "$not_in": List[Any],
        "$contains": Any,
        "$starts_with": Any,
        "$ends_with": Any,
    },
    total=False,
)


class FilterData(TypedDict, total=False):
    AND: Union[Dict[str, Any], List[Dict[str, Any]]]
    OR: Union[Dict[str, Any], List[Dict[str, Any]]]


class PrismaFilterBuilder:
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        *,
        model: Optional[Type[BaseModel]] = None,
    ):
        self.conditions: Dict[str, List[Dict[str, Any]]] = {"AND": [], "OR": []}
        self.others: Dict[str, Any] = {}
        self.model = model
        if data:
            self._parse(data)

    def _parse(self, data: Dict[str, Any]):
        where = data.get("where")
        if where:
            self._validate_data(where)
            for key, val in where.items():
                if key.upper() in ("AND", "OR"):
                    if isinstance(val, dict):
                        self.conditions[key.upper()].extend(
                            [{k: v} for k, v in val.items()]
                        )
                    elif isinstance(val, list):
                        self.conditions[key.upper()].extend(val)
                    else:
                        raise ValueError(f"{key} must be dict or list")
                else:
                    self.others[key] = val

        for key, val in data.items():
            if key != "where":
                self.others[key] = val

    def _validate_data(self, cond: Dict[str, Any]):
        if isinstance(cond, dict):
            for item in cond.values():
                if isinstance(item, list):
                    for value in item:
                        if not isinstance(value, dict):
                            raise ValueError(
                                "Invalid condition in list, expected dict but got: "
                                f"{type(value).__name__}"
                            )
                        self._validate_condition(value)

                elif isinstance(item, dict):
                    self._validate_condition(item)

                else:
                    raise ValueError(
                        "Invalid condition, expected dict or list but got: "
                        f"{type(item).__name__}"
                    )

    def _validate_condition(self, cond: Dict[str, Any]):
        print("Validating condition: ", cond)
        if self.model and isinstance(cond, dict):
            map_field_type = self.model.map_fields_types()
            for key in cond.keys():
                if key not in map_field_type.keys():
                    raise ValueError(f"Invalid field: {key}")
                if isinstance(cond[key], dict):
                    for operator in cond[key].keys():
                        allowed_ops = ALLOWED_FILTER_OPERATORS_BY_TYPE.get(
                            map_field_type.get(key, str), []
                        )
                        if operator not in allowed_ops:
                            raise ValueError(
                                f"Invalid operator '{operator}' for field '{key}'"
                            )

    def build(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.conditions["AND"]:
            result["AND"] = self.conditions["AND"]
        if self.conditions["OR"]:
            result["OR"] = self.conditions["OR"]
        result.update(self.others)
        return result


query_params = {}


f = PrismaFilterBuilder(
    {
        "where": query_params,
    }
)
Teste.filter().add(query_params)

f = PrismaFilterBuilder(
    {
        "where": {
            "OR": [
                {"status": "active"},
                {"status": "inactive"},
                {"role": "user", "age": {"$lt": 30}},
            ],
            "AND": {
                "age": {"$gt": 18},
                "role": "BRAZIL",
            },
        },
        "page_size": 100,
        "after_cursor": "cursor_value",
        "before_cursor": "cursor_value",
        "order_by": {"created_at": "desc"},
    },
    model=Teste,
)
pprint(f.build())


query = {"name": "teste"}
if "a" != "b":
    query.update({"status": "teste"})
