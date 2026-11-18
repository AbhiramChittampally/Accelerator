
from app import application_v1, application_v2


def blue_green_router(active_environment):
    if active_environment == "blue":
        return application_v1()

    if active_environment == "green":
        return application_v2()

    raise ValueError("Invalid environment")


def canary_router(request_number):
    if request_number <= 1:
        return application_v2()

    return application_v1()
