from utils.config_reader import get_base_url


class EnvironmentManager:

    SUPPORTED_ENVIRONMENTS = ("qa", "uat", "prod")

    @staticmethod
    def validate_environment(environment: str) -> str:
        environment = environment.lower()

        if environment not in EnvironmentManager.SUPPORTED_ENVIRONMENTS:
            raise ValueError(
                f"Unsupported environment: {environment}. "
                "Use qa, uat or prod."
            )

        return environment

    @staticmethod
    def get_application_url(environment: str) -> str:
        environment = EnvironmentManager.validate_environment(environment)
        return get_base_url(environment)