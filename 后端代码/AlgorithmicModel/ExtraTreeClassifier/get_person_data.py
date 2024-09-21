
from typing import Any, Dict

from sqlalchemy import select, inspect

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord


async def get_one_person(person_id: str):
    """

    :param person_id:
    :return:
    """
    try:
        stmt = select(MedicalRecord).where(MedicalRecord.personal_id == person_id)
        async with managed_async_session() as session:
            res = await session.execute(stmt)
            person: MedicalRecord = res.scalars().first()

            person_dict: Dict[str, Any] = {c.key: getattr(person, c.key) for c in inspect(person).mapper.column_attrs}
            # print(person_dict)
            # print("hlsdfsldfksldf")
            return person_dict
    except Exception as e:
        return "失败"
