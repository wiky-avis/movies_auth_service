from user_agents.parsers import UserAgent

from src.db.db_models import DeviceType


def check_device_type(user_agent: UserAgent):
    if user_agent.is_pc:
        return DeviceType.WEB.value
    if user_agent.is_mobile:
        return DeviceType.MOBILE.value
    if user_agent.is_tablet:
        return DeviceType.TABLET.value

    return DeviceType.UNKNOWN.value
