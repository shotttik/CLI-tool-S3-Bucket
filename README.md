# AWS BTU

**_ Important Code works in windows _**

# S3 CLI

That's S3 CLI tool, created for educational purposes. Don't forget to check `.env.example` file to see all the required credentials to allow CLI script work correctly.

## Install

First install:

```
poetry install
```

or

```
python -m pip install -r requirements.txt
```

## Usage

First run in shell help command, to see the message about avaliable CLI functions, it can listen for passed `-h`, or `--help`:

```shell
python main.py -h
```

## Bucket

Commands works without `""` too.

Show buckets

```shell
python .\poetry_week3\main.py --showBuckets
```

Create bucket

```shell
python .\poetry_week3\main.py bucket --name taskbtu --createBucket
```

Delete bucket

```
python .\poetry_week3\main.py bucket --name taskbtu --deleteBucket
```

Show policy

```
python .\poetry_week3\main.py bucket --name taskbtu --showPolicy
```

Create Policy

```
python .\poetry_week3\main.py bucket --name taskbtu --createPolicy
```

Upload file

```
python .\poetry_week3\main.py bucket --name taskbtu --uploadFile https://www.coreldraw.com/static/cdgs/images/free-trials/img-ui-cdgsx.jpg --filename test.jpa -s
```

Make file public

```
python .\poetry_week3\main.py bucket --name taskbtu --makePublic --filename test.jpeg
```

List objects

```
python poetry_week3/main.py bucket --name taskbtu -lo
```

Delete file

```
python poetry_week3/main.py bucket --name taskbtu -del --filename image_file_3471b0f2503cfb73448a689aa3995df5.jp
```

Put file lifecycle policy

```
python poetry_week3/main.py bucket --name taskbtu --put_lifecycle_policy
```

## VPC

Create VPC with IGW

```shell
python poetry_week3/main.py vpc create -tag btuvpc
```
