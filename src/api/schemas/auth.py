from pydantic import BaseModel, EmailStr, Field


class EmailRequestSchema(BaseModel):
  """
  Schema for requesting a passwordless magic code.
  """

  email: EmailStr = Field(..., description="User E-mail to receive the magic code")


class VerifyRequestSchema(BaseModel):
  """
  Schema for verifying a magic code to issue JWT tokens.
  """

  email: EmailStr = Field(..., description="User E-mail for verification")
  code: str = Field(
    ...,
    min_length=6,
    max_length=6,
    description="6-digit code received by e-mail",
  )


class TokenResponseSchema(BaseModel):
  """
  Schema for returning the access token.
  """

  access_token: str = Field(..., description="Short-lived Access token JWT")
  token_type: str = Field("bearer", description="Type of the authentication token")


class MessageResponseSchema(BaseModel):
  """
  Schema for returning a generic message response.
  """

  message: str = Field(..., description="Response message detail")
