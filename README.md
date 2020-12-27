# T-Mobile Bill Generator

## Configuration Files

- ### input.json

  - File that contains input variables for [main.py](src/main.py)

    ```(json)
    {
        "path":"Path to T-Mobile pdf bill",
        "email":"True for sending email | False to skip",
        "sender":"Email of bill generating member",
        "venmo":"True for using Venmo feature | False to skip",
        "user": "Name of the sender",
        "test": "True for testing | False for actual run"
    }
    ```

  - Execute [main.py](src/main.py) with `--help` option for more details

- ### credentials.json

  - This file can be generated via enabling gmail API client
  - It then generate a one-time `configs/token.pickle` and uses it when sending email
  - Follow steps mentioned [here](https://developers.google.com/gmail/api/quickstart/python?authuser=2) as intial setup

    ```(json)
    {
        "installed":{
            "client_id":"",
            "project_id":"",
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":"",
            "redirect_uris":[
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }
    }

    ```

- ### users.json

  - This file store information about the users in the plan
  - Folllowing is the format:

    ```(json)
    {
        "123456789" = {
            "name": "Abcd", 
            "email": "abcd@gmail.com"
        },
        "234567891" = {
            "name": "Efgh",
            "email": "efgh@gmail.com"
        },
        "Phone Number" = {
            "name": "name of the person",
            "email": "email address"
        }
        ...
        ...
    }
    ```

- ### venmo.json

  - This file stores venmo user id information
  - Follow steps mentioned [here](https://github.com/mmohades/Venmo) as intial setup
  - Following is the format:
  
    ```(json)
    {
        "users": {
            "(123)345-3211": {
                "venmo_username": "Venmo User ID",
                "additional_note": "Note in additon to Tmobile Month",
                "additional_amount": Negative or Additional amount
            },
            ...
            ...
        },
        "token": <<Token generated using Venmo API>>
    },
    ```

## Contributing

Contributions are appreciated. You can help with application documentation in [README.md](src/README.md). You can also help by [reporting bugs](https://github.com/dbcoder22/tmobile/issues/new)
