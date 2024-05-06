import re
from datetime import datetime
from typing import List

from pydantic import EmailStr, BaseModel, ConfigDict, Field, field_validator

phone_number_regex = r"^\+[1-9]\d{1,14}$"
password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"


class UserRead(BaseModel):
    """
    Represents a user retrieval model that includes detailed user information.
    This model is used for reading user data with comprehensive details such as
    full name, contact info, and status flags indicating activity and staff roles.
    """

    model_config = ConfigDict(
        title="UserRead",
        from_attributes=True,
    )
    id: int = Field(..., alias="user_id", title="User ID", description="The user ID", example=1)
    first_name: str = Field(..., title="First Name", description="The user first name", example="John")
    last_name: str = Field(..., title="Last Name", description="The user last name", example="Doe")
    email: EmailStr = Field(..., title="Email", description="The user email", example="user@example.com")
    phone_number: str = Field(
        ...,
        title="phoneNumber",
        description="The user phone number in iso format E.164",
        example="+380501234567",
        pattern=phone_number_regex,
    )
    hashed_password: str = Field(..., title="Hashed Password", description="The user hashed password", exclude=True)
    is_active: bool = Field(
        ...,
        title="isActive",
        description="The user status",
        example=True,
    )
    is_superuser: bool = Field(..., title="Is Superuser", description="The user role", example=False)
    registration_datetime: datetime = Field(
        ...,
        title="registrationDatetimeUTC",
        description="The user registration datetime",
        example="2021-10-01T00:00:00",
    )
    last_login_datetime: None | datetime = Field(
        ...,
        title="lastLoginDatetimeUTC",
        description="The user last login datetime",
        example="2021-10-01T00:00:00",
        nullable=True,
    )


class UserCreate(BaseModel):
    """
    Represents a user creation model used to collect all necessary data to register a new user.
    It ensures that all required fields such as first and last names, email, phone number, and
    password are provided with proper validations like minimum length and format restrictions.
    """

    model_config = ConfigDict(
        title="UserCreate",
    )
    first_name: str = Field(
        ...,
        title="firstName",
        description="The user first name",
        example="John",
        min_length=2,
    )
    last_name: str = Field(
        ...,
        title="lastName",
        description="The user last name",
        example="Doe",
        min_length=2,
    )
    email: EmailStr = Field(..., title="Email", description="The user email", example="user@example.com")
    phone_number: str = Field(
        ...,
        title="phoneNumber",
        description="The user phone number in iso format E.164",
        example="+380501234567",
        pattern=phone_number_regex,
    )
    password: str = Field(
        ...,
        title="password",
        description="The user password. Minimum eight characters, at least one uppercase letter, one lowercase letter and one number",
        example="Password1",
    )

    @field_validator("password")
    def validate_password(cls, value):
        if not re.match(password_regex, value):
            raise ValueError(
                "Password must be minimum eight characters, at least one uppercase letter, one lowercase letter and one number"
            )
        return value


class JWTToken(BaseModel):
    """
    Represents an authentication token used in API security. This model provides the access token and its type,
    typically used for bearer authentication. The default token type is 'Bearer', which is commonly used in
    OAuth 2.0 and JWT (JSON Web Tokens) systems.
    """

    model_config = ConfigDict(title="Token", arbitrary_types_allowed=True)
    access_token: str = Field(
        ...,
        title="accessToken",
        description="The access token",
    )
    token_type: str = Field(
        title="tokenType",
        description="The token type",
        example="Bearer",
        default_factory=lambda: "Bearer",
    )
    expires_in: int = Field(
        title="expiresIn",
        description="The token expiration time in seconds, default is 3600 seconds (1 hour)",
        example=3600,
        default_factory=lambda: 3600,
    )


class TokenPayload(BaseModel):
    """
    Represents a token payload model that contains the user ID and email address.
    This model is used to extract the user information from the token payload
    to authenticate and authorize the user in the system.
    """

    model_config = ConfigDict(title="TokenPayload")
    sub: str = Field(..., title="subject", description="The subject of the token (email)")
    user_id: int = Field(..., title="id", description="The user ID")
    exp: int = Field(..., title="expiration", description="The token expiration datetime")


class HTTPExceptionModel(BaseModel):
    """
    Represents an HTTP exception model that provides detailed information about an error.
    """

    model_config = ConfigDict(title="HTTPException")
    error: str = Field(title="error", description="The error message", example="Bad Request")
    message: List[str] | str = Field(
        title="messages", description="The error description", example="[Error message1, Error message2]"
    )
