from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

	app_name: str = "Oakfolio API"
	api_v1_prefix: str = "/api/v1"
	debug: bool = True

	database_url: str
	secret_key: str

	algorithm: str
	access_token_expire_minutes: str

	frontend_url: str

	model_config = SettingsConfigDict(
		env_file=".env",
		extra="ignore",
	)

settings = Settings()