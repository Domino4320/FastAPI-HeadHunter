import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from users.schemas import UserRegistrationSchema
import asyncio
from core.enums import Role
from users.crud import Register
from contextlib import asynccontextmanager
from core.database import db_context


async def create_admin():
    try:
        admin = UserRegistrationSchema(
            username=input("Admin username: "),
            login=input("Admin login: "),
            email=inp if (inp := input("Admin email: ")) else None,
            password=input("Admin password: "),
        )
        local_session_manager = asynccontextmanager(db_context.get_session)
        async with local_session_manager() as session:
            await Register(admin, session).register_user(Role.ADMIN)
        return "Admin was successfully added"
    except ValueError:
        print("ValidationError. Check UserRegistrationSchema.")


if __name__ == "__main__":
    asyncio.run(create_admin())
