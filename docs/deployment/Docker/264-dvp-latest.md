url: https://docs.docker.com/reference/api/dvp/latest/
----

[](/reference)

* API

  * Authentication Endpoints

    * postCreate an authentication token
    * postSecond factor authentication

  * Discovery

    * getGet namespaces and repos
    * getGet user's namespaces
    * getGet namespace

  * Namespace data

    * getGet pull data
    * getGet pull data
    * getGet years with data
    * getGet timespans with data
    * getGet namespace metadata for timespan
    * getGet namespace data for timespan
    * getGet pull data for multiple repos

* Models

  * ResponseDataFile
  * Year Data Model
  * Month Data Model
  * Week Data Model

[API docs by Redocly](https://redocly.com/redoc/)

# DVP Data API (1.0.0)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/dvp/latest.yaml)

The Docker DVP Data API allows [Docker Verified Publishers](https://docs.docker.com/docker-hub/publish/) to view image pull analytics data for their namespaces. Analytics data can be retrieved in a CSV as raw data, or in a summary format.

#### Summary data

In your summary data CSV, you will have access to the data points listed below. You can request summary data for a complete week (Monday through Sunday) or for a complete month (available on the first day of the following month).

There are two levels of summary data:

* Repository-level, a summary of every namespace and repository
* Tag- or digest-level, a summary of every namespace, repository, and reference (tag or digest)

The summary data formats contain the following data points:

* Unique IP address count
* Pulls by tag count
* Pulls by digest count
* Version check count

#### Raw data

In your raw data CSV you will have access to the data points listed below. You can request raw data for a complete week (Monday through Sunday) or for a complete month (available on the first day of the following month). **Note:** each action is represented as a single row.

* Type (industry)

* Host (cloud provider)

* Country (geolocation)

* Timestamp

* Namespace

* Repository

* Reference (digest is always included, tag is provided when available)

* HTTP request method

* Action, one of the following:

  * Pull by tag
  * Pull by digest
  * Version check

* User-Agent

## [](#tag/authentication)Authentication Endpoints

## [](#tag/authentication/operation/PostUsersLogin)Create an authentication token

Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs.

The returned token is used in the HTTP Authorization header like `Authorization: Bearer {TOKEN}`.

Most Docker Hub APIs require this token either to consume or to get detailed information. For example, to list images in a private repository.

##### Request Body schema: application/jsonrequired

Login details.

|                  |                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| usernamerequired | stringThe username of the Docker Hub account to authenticate with.                                |
| passwordrequired | stringThe password or personal access token (PAT) of the Docker Hub account to authenticate with. |

### Responses

/v2/users/login

### Request samples

* Payload

Content type

application/json

`{
"username": "myusername",
"password": "hunter2"

## [](#tag/authentication/operation/PostUsers2FALogin)Second factor authentication

When a user has 2FA enabled, this is the second call to perform after `/v2/users/login` call.

Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs.

The returned token is used in the HTTP Authorization header like `Authorization: Bearer {TOKEN}`.

Most Docker Hub APIs require this token either to consume or to get detailed information. For example, to list images in a private repository.

##### Request Body schema: application/jsonrequired

Login details.

|                           |                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------- |
| login\_2fa\_tokenrequired | stringThe intermediate 2FA token returned from `/v2/users/login` API.                  |
| coderequired              | stringThe Time-based One-Time Password of the Docker Hub account to authenticate with. |

### Responses

/v2/users/2fa-login

## [](#tag/discovery)Discovery

## [](#tag/discovery/operation/getNamespaces)Get namespaces and repos

Gets a list of your namespaces and repos which have data available.

##### Authorizations:

*Docker Hub Authentication*

### Responses

/api/publisher/analytics/v1/

### Response samples

* 200

Content type

application/json

`{
"namespaces": [
"string"
]
}`

## [](#tag/discovery/operation/getUserNamespaces)Get user's namespaces

Get metadata associated with the namespaces the user has access to, including extra repos associated with the namespaces.

##### Authorizations:

*Docker Hub Authentication*

### Responses

/api/publisher/analytics/v1/namespaces

### Response samples

* 200

Content type

application/json

`[
{
"namespace": "string",
"extraRepos": [
"string"
],
"datasets": [
{
"name": "pulls",
"views": [
"raw"
],
"timespans": [
"months"
]
}
]
}
]`

## [](#tag/discovery/operation/getNamespace)Get namespace

Gets metadata associated with specified namespace, including extra repos associated with the namespace.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                   |                                   |
| ----------------- | --------------------------------- |
| namespacerequired | stringNamespace to fetch data for |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}

### Response samples

* 200

Content type

application/json

`{
"namespace": "string",
"extraRepos": [
"string"
],
"datasets": [
{
"name": "pulls",
"views": [
"raw"
],
"timespans": [
"months"
]
}
]
}`

## [](#tag/namespaces)Namespace data

## [](#tag/namespaces/operation/getNamespacePulls)Get pull data

Gets pulls for the given namespace.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                   |                                   |
| ----------------- | --------------------------------- |
| namespacerequired | stringNamespace to fetch data for |

##### query Parameters

|          |                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| timespan | string (TimespanType)Enum: "months" "weeks"Timespan type for fetching data                                                           |
| period   | string (PeriodType)Enum: "last-2-months" "last-3-months" "last-6-months" "last-12-months"Relative period of the period to fetch data |
| group    | string (GroupType)Enum: "repo" "namespace"Field to group the data by                                                                 |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}/pulls

### Response samples

* 200

Content type

application/json

`{
"pulls": [
{
"start": "string",
"end": "string",
"repo": "string",
"namespace": "string",
"pullCount": 0,
"ipCount": 0,
"country": "string"
}
]
}`

## [](#tag/namespaces/operation/getRepoPulls)Get pull data

Gets pulls for the given repo.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                   |                                    |
| ----------------- | ---------------------------------- |
| namespacerequired | stringNamespace to fetch data for  |
| reporequired      | stringRepository to fetch data for |

##### query Parameters

|          |                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| timespan | string (TimespanType)Enum: "months" "weeks"Timespan type for fetching data                                                           |
| period   | string (PeriodType)Enum: "last-2-months" "last-3-months" "last-6-months" "last-12-months"Relative period of the period to fetch data |
| group    | string (GroupType)Enum: "repo" "namespace"Field to group the data by                                                                 |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}/repos/{repo}/pulls

### Response samples

* 200

Content type

application/json

`{
"pulls": [
{
"start": "string",
"end": "string",
"repo": "string",
"namespace": "string",
"pullCount": 0,
"ipCount": 0,
"country": "string"
}
]
}`

## [](#tag/namespaces/operation/getNamespaceYears)Get years with data

Gets a list of years that have data for the given namespace.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                   |                                   |
| ----------------- | --------------------------------- |
| namespacerequired | stringNamespace to fetch data for |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}/pulls/exports/years

### Response samples

* 200

Content type

application/json

`{
"years": [
{
"year": 0
}
]
}`

## [](#tag/namespaces/operation/getNamespaceTimespans)Get timespans with data

Gets a list of timespans of the given type that have data for the given namespace and year.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                      |                                                                               |
| -------------------- | ----------------------------------------------------------------------------- |
| namespacerequired    | stringNamespace to fetch data for                                             |
| yearrequired         | integerYear to fetch data for                                                 |
| timespantyperequired | string (TimespanType)Enum: "months" "weeks"Type of timespan to fetch data for |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}/pulls/exports/years/{year}/{timespantype}

### Response samples

* 200

Content type

application/json

Example

MonthData

`{
"months": [
{
"month": 0
}
]
}`

## [](#tag/namespaces/operation/getNamespaceTimespanMetadata)Get namespace metadata for timespan

Gets info about data for the given namespace and timespan.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                      |                                                                               |
| -------------------- | ----------------------------------------------------------------------------- |
| namespacerequired    | stringNamespace to fetch data for                                             |
| yearrequired         | integerYear to fetch data for                                                 |
| timespantyperequired | string (TimespanType)Enum: "months" "weeks"Type of timespan to fetch data for |
| timespanrequired     | integerTimespan to fetch data for                                             |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}/pulls/exports/years/{year}/{timespantype}/{timespan}

### Response samples

* 200

Content type

application/json

Example

MonthModel

`{
"month": 0
}`

## [](#tag/namespaces/operation/getNamespaceDataByTimespan)Get namespace data for timespan

Gets a list of URLs that can be used to download the pull data for the given namespace and timespan.

##### Authorizations:

*Docker Hub Authentication*

##### path Parameters

|                      |                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| namespacerequired    | stringNamespace to fetch data for                                                                  |
| yearrequired         | integerYear to fetch data for                                                                      |
| timespantyperequired | string (TimespanType)Enum: "months" "weeks"Type of timespan to fetch data for                      |
| timespanrequired     | integerTimespan to fetch data for                                                                  |
| dataviewrequired     | string (DataviewType)Enum: "raw" "summary" "repo-summary" "namespace-summary"Type of data to fetch |

### Responses

/api/publisher/analytics/v1/namespaces/{namespace}/pulls/exports/years/{year}/{timespantype}/{timespan}/{dataview}

### Response samples

* 200

Content type

application/json

`{
"data": [
{
"url": "string",
"size": 0
}
]
}`

## [](#tag/namespaces/operation/getManyReposPulls)Get pull data for multiple repos

Gets pull for the given repos.

##### Authorizations:

*Docker Hub Authentication*

##### query Parameters

|               |                                                                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| reposrequired | Array of stringsRepositories to fetch data for (maximum of 50 repositories per request).                                             |
| timespan      | string (TimespanType)Enum: "months" "weeks"Timespan type for fetching data                                                           |
| period        | string (PeriodType)Enum: "last-2-months" "last-3-months" "last-6-months" "last-12-months"Relative period of the period to fetch data |
| group         | string (GroupType)Enum: "repo" "namespace"Field to group the data by                                                                 |

### Responses

/api/publisher/analytics/v1/repos/pulls

### Response samples

* 200

Content type

application/json

`{
"repos": {
"property1": {
"pulls": [
{
"start": "string",
"end": "string",
"repo": "string",
"namespace": "string",
"pullCount": 0,
"ipCount": 0,
"country": "string"
}
]
},
"property2": {
"pulls": [
{
"start": "string",
"end": "string",
"repo": "string",
"namespace": "string",
"pullCount": 0,
"ipCount": 0,
"country": "string"
}
]
}
}
}`

## [](#tag/responseDataFile)ResponseDataFile

|      |                  |
| ---- | ---------------- |
| url  | string           |
| size | integer \<int64> |

`{
"url": "string",
"size": 0
}`

## [](#tag/yearModel)Year Data Model

|      |         |
| ---- | ------- |
| year | integer |

`{
"year": 0
}`

## [](#tag/monthModel)Month Data Model

|       |         |
| ----- | ------- |
| month | integer |

`{
"month": 0
}`

## [](#tag/weekModel)Week Data Model

|      |         |
| ---- | ------- |
| week | integer |

`{
"week": 0
}`

----
