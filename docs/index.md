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

The `tetra` API consists of the following resources:

- `Project` - a project is the top-level container for all other resources
- `Build` - a build groups results together
- `Result` - a result of a single test case

**This is a JSON-based API:** Unless indicated otherwise, all requests and
responses are in JSON format. All requests should have the `Content-type` and
`Accept` headers set to `application/json`.

### Response Codes

These are the response codes used by Tetra.

Error Code | Meaning | Definition
---------- | ------- | ----------
200        | OK      | The request handled successfully and information was returned in the body.
201        | Created | The request successfully and a resource was created. Check the response body for the resource id.
204        | No Content | The request was handled successfuly and the response body is empty.
400        | Bad Request | The request could not be parsed or the request data was invalid.
404        | Not Found | The requested resource was not found.
500        | Server Error | The API server encountered an error while handling the request.

## Projects

A Project is the top-level container for all other resources.

Field | Type | Description
----- | ---- | -----------
`name` | string | The name of the project. This does not need to be unique.
`id` | int | The unique project id.

### Create a Project

```.http
POST /projects HTTP/1.1
...

{
    "name": "my-project"
}


HTTP/1.1 201 Created
...

{
    "id": 5,
    "name": "my-project"
}
```

### List Projects

```.http
GET /projects HTTP/1.1
...


HTTP/1.1 200 OK
...

[
    {
        "id": 1,
        "name": "my-project"
    },
    {
        "id": 2,
        "name": "my-other-project"
    }
]
```

### Fetch a Project

```.http
GET /projects/1 HTTP/1.1
...


HTTP/1.1 200 OK
...

{
    "id": 1,
    "name": "test-project"
}
```

### Delete a Project

This deletes the project and all the project's builds and results.

```.http
DELETE /projects/9 HTTP/1.1
...


HTTP/1.1 204 No Content
```


## Builds

A Build is a container for Results.

(A Build typically corresponds to a job on some automation server, like
[Jenkins](https://jenkins.io/).)

Field          | Type   | Required | Description
-------------- | ------ | -------- | -----------
`name`         | string | yes      | A descriptive name. This does not need to be unique.
`build_url`    | string | no       | A link for your own usage, like to logs or to a Jenkins job url.
`region`       | string | no       | The region being tested (e.g. US East, US West, IAD, DFW, ...)
`environment`  | string | no       | The environment being tested (e.g. preprod, staging, prod)
`status`       | string | no       | The status of the build (like `passed`, `failed`, `error`, ...)

### Create a Build

```.http
POST /projects/1/builds HTTP/1.1
...

{
    "build_url": "http://jenkins.example.com/job/my-unit-tests/22",
    "environment": "preprod",
    "name": "my-unit-tests",
    "region": "US East",
    "status": "passed"
}


HTTP/1.1 201 Created
...

{
    "build_url": "http://jenkins.example.com/job/my-unit-tests/22",
    "environment": "preprod",
    "id": 1,
    "name": "my-unit-tests",
    "project_id": 1,
    "region": "US",
    "status": "passed",
    "tags": null
}
```

### List Builds

```.http
GET /projects/1/builds HTTP/1.1
...


HTTP/1.1 200 OK
...

[
    {
        "build_url": "http://jenkins.example.com/job/my-unit-tests/22",
        "environment": "preprod",
        "id": 1,
        "name": "my-unit-tests",
        "project_id": 1,
        "region": "US",
        "status": "passed"
    },
    {
        "build_url": null,
        "environment": "preprod",
        "id": 2,
        "name": "my-unit-tests",
        "project_id": 1,
        "region": "US",
        "status": null
    }
]
```

### Fetch a Build

```.http
GET /projects/1/builds/2 HTTP/1.1
...


HTTP/1.1 200 OK
...

{
    "build_url": null,
    "environment": "preprod",
    "id": 2,
    "name": "my-unit-tests",
    "project_id": 1,
    "region": "US"
    "status": "passed"
}
```

## Results

A Result corresponds to an individual test case.

Field            | Type   | Required | Description
---------------- | ------ | -------- | -----------
`test_name`      | string | yes      | The name of the result. This is typically the name of a test case.
`result`         | string | yes      | The test case result. This should be one of: `passed`, `failed`, `skipped`, `error`.
`result_message` | string | no       | Any additional text you would like to store, like test logs or tracebacks.
`timestamp`      | int    | no       | The timestamp test was run (seconds from epoch time). Defaults to the API server time.

### Create a Result

```.http
POST /projects/1/builds/1/results HTTP/1.1
...

{
    "result": "passed",
    "result_message": "Traceback ... <some long traceback>",
    "test_name": "designate_tempest_plugin.tests.scenario.v2.test_zones.ZonesTest.test_create_and_delete_zone"
}

HTTP/1.1 201 Created
...

{
    "build_id": 1,
    "id": 352,
    "project_id": 1,
    "result": "passed",
    "result_message": "Traceback ... <some long traceback>",
    "test_name": "designate_tempest_plugin.tests.scenario.v2.test_zones.ZonesTest.test_create_and_delete_zone",
    "timestamp": 1470079231.426697
}
```

### Import Results from XUnit XML

This allows you to send XUnit-style XML directly to Tetra. Tetra will create
one result per `<testcase>`.

**Notes**

- This requires the request header `Content-type: application/xml`
- Tetra only supports XML containing a single `<testsuite>` tag within the
  `<testsuites>` tag.

```.http
POST /projects/1/builds/2/results HTTP/1.1
Accept: application/json
Content-Type: application/xml

<?xml version="1.0" ?>
<testsuites errors="100" failures="100" skipped="100" tests="400" time="25109.651362">
    <testsuite errors="100" failures="100" name="fake-junit-xml-suite" skipped="100" tests="400" time="25109.651362">
        <testcase classname="generated.xml.test.case.passes" name="TestPassed0" time="91.617842" />
        <testcase classname="generated.xml.test.case.passes" name="TestPassed1" time="5.880439" />
        ...
        <testcase classname="generated.xml.test.case.errors" name="TestErrored98" time="100.621474">
            <error message="error! xXFrXlfHQjKUQevMahHnS gRctLqwOKwDzyRXSHl" type="error" />
        </testcase>
        <testcase classname="generated.xml.test.case.errors" name="TestErrored99" time="44.525510">
            <error message="error! uxYVqAN XRJZUdgXzyMgxImOCoEBDndjE YJj gb" type="error" />
        </testcase>
    </testsuite>
</testsuites>

HTTP/1.1 201 Created
...

{
    "metadata": {
        "success_rate": 33.33,
        "total_errors": 100,
        "total_failures": 100,
        "total_passed": 100,
        "total_results": 400,
        "total_skipped": 100
    }
}
```

### List Results

There are two ways to list Results, which give responses in the same format:

Method | Path | Description
------ | ---- | -----------
GET    | `/projects/{project_id}/builds/{build_id}/results` | List Results for the Build `build_id` and Project `project_id`
GET    | `/projects/{project_id}/results` | List all Results for the Project `project_id`. This is useful for filtering across all builds.



```.http
GET /projects/1/builds/2/results HTTP/1.1
...


HTTP/1.1 200 OK
...

{
    "metadata": {
        "success_rate": 33.33,
        "total_errors": 100,
        "total_failures": 100,
        "total_passed": 100,
        "total_results": 400,
        "total_skipped": 100
    },
    "results": [
        {
            "build_id": 2,
            "id": 353,
            "project_id": 1,
            "result": "passed",
            "result_message": null,
            "test_name": "generated.xml.test.case.passes.TestPassed0",
            "timestamp": 1470079711
        },
        ...
    ]
}
```

# Architecture

`tetra` consists of:

- API nodes
- Worker nodes
- A database
- A queue
- A dashboard
