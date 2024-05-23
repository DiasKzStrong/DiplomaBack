class ErrorDetail:
    AUTHENTICATION_REQUIRED = "Authentication required."
    USER_NOT_FOUND = "User not found."
    AUTHENTICATION_FAILED = "Incorrect username or password"
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    ACCESS_TOKEN_EXPIRED = "Access token has expired."
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."
