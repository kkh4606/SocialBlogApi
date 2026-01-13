dummyComments = [
    {
        "id": 1,
        "content": "first comment",
        "comments": [
            {
                "id": 1,
                "content": "first reply",
                "comments": [
                    {
                        "id": 1,
                        "content": "first nested reply",
                        "comments": [],
                    }
                ],
            }
        ],
    },
]


index = 0

count = 0


for index, comment in enumerate(dummyComments):
    for reply in comment["comments"]:
        count += 1
        for nested in reply["comments"]:
            count += 1
            print(nested)


print(count)
