import copy


def find_comment(arr, comment_id):

    for comment in arr:
        if comment_id == comment["id"]:
            return comment
        if comment["comments"]:
            found = find_comment(comment["comments"], comment_id)

            if found is not None:
                return found

    return None


dummyComments = [
    {
        "id": 1,
        "content": "first comment",
        "comments": [
            {
                "id": 7,
                "content": "first reply",
                "comments": [
                    {
                        "id": 9,
                        "content": "nested reply",
                        "comments": [
                            {
                                "id": 100,
                                "content ": "nested nested reply",
                                "comments": [
                                    {
                                        "id": 40000,
                                        "content": "nested nested nestest reply",
                                        "comments": [],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    },
    {
        "id": 3,
        "content": "first comment",
        "comments": [
            {
                "id": 7,
                "content": "first reply",
                "comments": [
                    {
                        "id": 9,
                        "content": "nested reply",
                        "comments": [
                            {
                                "id": 123456789,
                                "content ": "nested nested reply",
                                "comments": [
                                    {
                                        "id": 30000,
                                        "content": "nested nested nestest reply",
                                        "comments": [],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    },
]


print(find_comment(dummyComments, 3))
