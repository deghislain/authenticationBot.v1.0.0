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
    },
    {
        "type": "function",
        "function": {
            "name": "create_new_account",
            "description": "Create a new user account given an username, first name, last name,"
                           "email, phone number, home address, password"
                           "Call this whenever you need to create a new user account, "
                           "for example when an user says 'I would like to register'",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The user's username needed to create a new account."
                    },
                    "first_name": {
                        "type": "string",
                        "description": "The user's first name needed to create a new account."
                    },
                    "last_name": {
                        "type": "string",
                        "description": "The user's last name needed to create a new account."
                    },
                    "email": {
                        "type": "string",
                        "description": "The user's email needed to create a new account."
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "The user's phone number needed to create a new account."
                    },
                    "home_address": {
                        "type": "string",
                        "description": "The user's phone number needed to create a new account."
                    },

                    "password": {
                        "type": "string",
                        "description": "The user's password needed to create a new account."
                    }
                },
                "required": ["username", "first_name", "last_name", "email", "phone_number",
                             "home_address", "password"],
                "additionalProperties": False
            }
        }
    }
]
