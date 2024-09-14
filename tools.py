
tools = [
    {
        "type": "function",
        "function": {
            "name": "user_authentication",
            "description": "Authenticate an user given an username and password. "
                           "Call this whenever you need to authenticate an user, "
                           "for example when an user says 'I would like to login'",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The user's username needed to login."
                    },
                    "password": {
                        "type": "string",
                        "description": "The user's password needed to login."
                    }
                },
                "required": ["username", "password"],
                "additionalProperties": False
            }
        }
    }
]
