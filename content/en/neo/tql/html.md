---
title: HTML()
type: docs
weight: 53
draft: true
---

The `HTML()` SINK generates an HTML document or an element as output, using the provided template language for formatting.
This allows you to fully customize the structure and appearance of the HTML output based on your query results.

## Contexts

The template understands HTML, CSS, JavaScript and URIs. It adds sanitizing functions to each simple action pipeline, so given the excerpt.

Each `{{.Value 0}}` is overwritten to add escaping functions as necessary. In this case it becomes

```html
SCRIPT({ $.yield(`http://host/path/file`) })
HTML({ <a href="/search?q={{.Value 0}}">{{.Value 0}}</a> })

// output:
// <a href="/search?q=http%3a%2f%2fhost%2fpath%2ffile">http://host/path/file</a>
```

Assuming `{{.Value 0}}` is `O'Reilly: How are <i>you</i>?`,
the examples below shows how `{{.Value 0}}` appears when used in context.

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`{{.Value 0}}`)

// output:
// O&#39;Reilly: How are &lt;i&gt;you&lt;/i&gt;?
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a title="{{.Value 0}}">`)

// output:
// <a title="O&#39;Reilly: How are you?">
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a title="{{.Value 0 | unsafeHTML}}">`)

// output:
// O'Reilly: How are <i>you</i>?
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a href="/{{.Value 0}}">`)

// output:
// <a href="/O%27Reilly:%20How%20are%20%3ci%3eyou%3c/i%3e?">
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a href="?q={{.Value 0}}">`)

// output:
// <a href="?q=O%27Reilly%3a%20How%20are%20%3ci%3eyou%3c%2fi%3e%3f">
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a onx='f("{{.Value 0}}")'>`)

// output:
// <a onx='f("O\u0027Reilly: How are \u003ci\u003eyou\u003c\/i\u003e?")'>
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a onx='f({{.Value 0}})'>`)

// output:
// <a onx='f(&#34;O&#39;Reilly: How are \u003ci\u003eyou\u003c/i\u003e?&#34;)'>
```

```html
SCRIPT({ $.yield(`O'Reilly: How are <i>you</i>?`) })
HTML(`<a onx='pattern = /{{.Value 0}}/;'>`)

// output:
// <a onx='pattern = /O\u0027Reilly: How are \u003ci\u003eyou\u003c\/i\u003e\?/;'>
```

Non-string values can be used in JavaScript contexts. If the record is an object:

in the escaped template

```html {{linenos="table"}}
SCRIPT({
    $.yield({A: "foo", B:"bar"})
})
HTML({
    <script>var pair = {{ .Value 0 }};</script>
})
```

then template output is

```html
<script>var pair = {"A":"foo","B":"bar"};</script>
```

## Unescaped Strings

By default, the template assumes that all pipelines produce a plain text string.
It adds escaping pipline stages necessary to correctly and safely embed that plain text string in the appropriate context.

When a data value is not plain text, you can make sure it is not over-escaped by marking it with its type.

Types HTML, JS, URL, and others can carry safe content that is exempted from escaping.

The template:

```js {{linenos="table"}}
SCRIPT({
    $.yield(`<b>World</b>`)
})
HTML({
    Hello, {{ .Value 0 | unsafeHTML }}!
})
```

to produce

```
Hello, <b>World</b>!
```

instead of

```
Hello, &lt;b&gt;World&lt;b&gt;!
```

Functions:

- `unsafeHTML`
- `unsafeCSS`
- `unsafeJS`
- `unsafeURL`
- `unsafeAttr`

<!-- ## Build a To-Do List Application

- Interactive with a SQLite database using SQL().
- Render documents with HTML().

### Step 1: Creating the SQLite Database

Let's start by defining the structure of our SQLite database.  
We'll create a `tasks` table with columns to store each task's details.

Run the following DDL in the SQL Editor.

The first line, `--env: bridge=...`, specifies that the statements should execute on the SQLite in-memory database.

```sql {{hl_lines=[1]}}
-- env: bridge=sqlite,file:memory?cache=shared
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    task_name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    date_added TEXT
);

select * from tasks;
--env: reset
```

This table will hold the task ID, name, description, status (like “pending” or “complete”), and the date the task was added.

### Step 2: Add Task

- Add Task

```sql
INSERT INTO tasks (task_name, description, status, date_added)
VALUES (?, ?, 'pending', ?)
-- task_name, description, date_added
```

### Step 3: List Task

### Step 4: Update Task -->
