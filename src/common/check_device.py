from user_agents.parsers import UserAgent

from src.common.tracer import trace_request as trace
from src.db.db_models import DeviceType


@trace("check_device_type")
def check_device_type(user_agent: UserAgent):
    if user_agent.is_pc:
        return DeviceType.WEB.value
    if user_agent.is_mobile:
        return DeviceType.MOBILE.value
    if user_agent.is_tablet:
        return DeviceType.TABLET.value

    return DeviceType.UNKNOWN.value
