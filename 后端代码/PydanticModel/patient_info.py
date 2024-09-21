from typing import Optional, List

from pydantic import BaseModel
from pydantic.validators import datetime
from sqlalchemy import DateTime, Float, Boolean


class PatientInfoSchema(BaseModel):
    """
    定义所有信息schema模型，返回json
    """
    personal_id: Optional[str] = None
    fraud_prob: Optional[float] = None
    not_fraud_prob: Optional[float] = None
    prob_res: Optional[bool] = None
    fraud_types: Optional[str] = None

    pos: Optional[List[int]] = None
    feature1: Optional[List[str]] = None
    feature2: Optional[List[str]] = None
    #允许orm模型转换为schema
    class Config:
        orm_mode = True


async def get_PatientInfoSchema(
    personal_id: Optional[str] = None,
    prob_res: Optional[bool] = None,
    fraud_prob: Optional[float] = None,
    # not_fraud_prob: Optional[float] = None,
    fraud_types: Optional[str] = None,

    pos: Optional[List[int]] = None,
    feature1: Optional[List[str]] = None,
    feature2: Optional[List[str]] = None

) -> PatientInfoSchema:
    person_info = PatientInfoSchema(
        personal_id=personal_id,
        prob_res=prob_res,
        fraud_prob=fraud_prob,
        # not_fraud_prob=not_fraud_prob,
        fraud_types=fraud_types,

        pos = pos,
        feature1 = feature1,
        feature2 = feature2
    )
    return person_info








