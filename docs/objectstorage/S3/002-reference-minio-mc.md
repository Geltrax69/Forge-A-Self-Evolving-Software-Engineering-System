url: https://docs.min.io/community/minio-object-store/reference/minio-mc/
----

# MinIO Client (mc) CLI Reference — Command Overview

`mc` is the command-line client for managing S3-compatible object storage (MinIO or any other S3-compatible endpoint registered as an alias).

## Alias Commands (connection profiles)

```sh
mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc alias list
mc alias remove myminio
```

## Bucket and Object Management

```sh
mc mb myminio/mybucket           # create bucket
mc rb myminio/mybucket           # remove bucket
mc ls myminio/mybucket           # list contents
mc cp file.txt myminio/mybucket  # copy/upload
mc cp myminio/mybucket/file.txt . # download
mc get myminio/mybucket/file.txt local.txt
mc put file.txt myminio/mybucket
mc mv myminio/mybucket/a.txt myminio/mybucket/b.txt
mc rm myminio/mybucket/file.txt
mc cat myminio/mybucket/file.txt
mc stat myminio/mybucket/file.txt
```

## Search and Discovery

```sh
mc find myminio/mybucket --name "*.log"
mc du myminio/mybucket
mc tree myminio/mybucket
```

## Data Sync / Transfer

```sh
mc mirror ./localdir myminio/mybucket   # one-way sync
mc diff myminio/bucket1 myminio/bucket2
mc watch myminio/mybucket               # monitor for changes
```

## Versioning

```sh
mc version enable myminio/mybucket
mc version suspend myminio/mybucket
mc version info myminio/mybucket
```

## Retention / Legal Hold / Object Lock

```sh
mc retention set GOVERNANCE 30d myminio/mybucket/file.txt
mc retention info myminio/mybucket/file.txt
mc legalhold set myminio/mybucket/file.txt
mc legalhold clear myminio/mybucket/file.txt
```

## Object Lifecycle Management (ILM)

```sh
mc ilm rule add myminio/mybucket --expiry-days 90
mc ilm rule ls myminio/mybucket
mc ilm rule rm myminio/mybucket --id <rule-id>
```

## Event Notifications

```sh
mc event add myminio/mybucket arn:minio:sqs::_:webhook --event put
mc event list myminio/mybucket
mc event remove myminio/mybucket arn:minio:sqs::_:webhook
```

## Encryption

```sh
mc encrypt set sse-s3 myminio/mybucket
mc encrypt info myminio/mybucket
mc encrypt clear myminio/mybucket
```

## Tags

```sh
mc tag set myminio/mybucket/file.txt "key1=value1&key2=value2"
mc tag list myminio/mybucket/file.txt
mc tag remove myminio/mybucket/file.txt
```

## Sharing (presigned URLs)

```sh
mc share download myminio/mybucket/file.txt   # generate a temporary download URL
mc share upload myminio/mybucket/file.txt      # generate a temporary upload URL
mc share list
```

## Anonymous / Public Access

```sh
mc anonymous set download myminio/mybucket    # make bucket publicly readable
mc anonymous set public myminio/mybucket      # public read/write
mc anonymous get myminio/mybucket
```

## Quotas

```sh
mc quota set myminio/mybucket --size 10GiB
mc quota info myminio/mybucket
mc quota clear myminio/mybucket
```

## CORS

```sh
mc cors set myminio/mybucket cors-config.json
mc cors get myminio/mybucket
mc cors remove myminio/mybucket
```

## Admin (server-side administration)

```sh
mc admin info myminio                 # cluster status/diagnostics
mc admin user add myminio newuser newuserpassword
mc admin policy attach myminio readwrite --user newuser
mc admin config get myminio
mc admin service restart myminio
mc admin heal myminio/mybucket
mc admin trace myminio                # live request tracing
```

## Utility

```sh
mc ping myminio
mc ready myminio
mc version
mc update
```

----
