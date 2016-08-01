# Tetra

`tetra` is a test result aggregator designed to make test result analysis
faster, easier, and more automated.

## How to use Tetra

- Run a test suite, like a suite of unit tests
- Create a `build` in `tetra`'s REST API for your test suite
- Post your test results to your created build. `tetra` accepts
  XUnit-compatible XML to make this step easy
- Explore test results...
    * in the dashboard,
    * in the REST API,
    * or use the REST API to build custom tools

## REST API Documentation

The `tetra` API consists of the following basic resources:

- `Project` - a project is the top-level container for all other resources
- `Build` - a build groups results together
- `Result` - a result of a single test case

**This is a JSON-based API:** Unless indicated otherwise, all requests and
responses are in JSON format. All requests should have the `Content-type` and
`Accept` headers set to `application/json`.

### Projects

A project is the top-level container for all other resources.

#### POST /projects

Create a new project

**Request body**

```JSON
{
    "name": "my-project"
}
```

**Response body**

```JSON
{
    "id": 1,
    "name": "my-project"
}
```

#### GET /projects

List all projects

**Response body**

```JSON
[
    {
        "id": 1,
        "name": "my-project"
    }
]
```

## Architecture

`tetra` consists of:

- API nodes
- Worker nodes
- A database
- A queue
- A dashboard
