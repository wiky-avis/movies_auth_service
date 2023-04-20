from src.db.db_models import RoleType


ROLES = (
    ("3f50d257-66da-4532-b64f-f4999282f4d0", RoleType.ROLE_PORTAL_ADMIN),
    ("5eff1f88-8f2b-40c5-a4d0-85893cb7071b", RoleType.ROLE_PORTAL_USER),
)

GET_ALL_ROLES_RESPONSE = {
    "error": None,
    "result": [
        {
            "name": "ROLE_PORTAL_ADMIN",
            "role_id": "3f50d257-66da-4532-b64f-f4999282f4d0",
        },
        {
            "name": "ROLE_PORTAL_USER",
            "role_id": "5eff1f88-8f2b-40c5-a4d0-85893cb7071b",
        },
    ],
    "success": True,
}
