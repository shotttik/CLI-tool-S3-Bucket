## სკრიპტის ჩართვის მაგალითები

`poetry run python .\poetry_week3\main.py --showBuckets`

`poetry run python .\poetry_week3\main.py bucket --name taskbtu --createBucket`

`poetry run python .\poetry_week3\main.py bucket --name taskbtu --deleteBucket`

`poetry run python .\poetry_week3\main.py bucket --name taskbtu --showPolicy`

`poetry run python .\poetry_week3\main.py bucket --name taskbtu --createPolicy`

`poetry run python .\poetry_week3\main.py bucket --name taskbtu --uploadFile https://www.coreldraw.com/static/cdgs/images/free-trials/img-ui-cdgsx.jpg --filename test.jpa -s`

`poetry run python .\poetry_week3\main.py bucket --name taskbtu --makePublic --filename test.jpeg `

`poetry run python poetry_week3/main.py bucket --name taskbtu -lo`

`poetry run python poetry_week3/main.py bucket --name taskbtu -del --filename image_file_3471b0f2503cfb73448a689aa3995df5.jpg`

`poetry run python poetry_week3/main.py bucket --name taskbtu --put_lifecycle_policy `

### for other command see python main.py -h/--help
