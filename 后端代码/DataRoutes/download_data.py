from fastapi import APIRouter
import pandas as pd
import io

from pandas import DataFrame
from starlette.responses import StreamingResponse

from Utils.read_data_from_database import read_patient_data

download_router = APIRouter(prefix="/download")

class NumberGenerator:
    """
    自动生成递增的数字
    """
    def __init__(self, start=0):
        self.current = start - 1

    def next_number(self):
        self.current += 1
        return self.current
gen = NumberGenerator(start=1)  # 从1开始

# 将DataFrame写入BytesIO缓冲区，模拟生成CSV文件

async def create_csv_from_dataframe(df: DataFrame):
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer

# 注意：在实际应用中，你可能不会在每次请求时都重新生成DataFrame，
# 而是根据需要计算或读取数据，然后一次性生成CSV内容并提供下载
@download_router.get("/download-csv")
async def downloadfile():
    """
    下载文件
    :return:
    """
    # 得到dataframe
    try:
        df = await read_patient_data()
        buffer = await create_csv_from_dataframe(df)
        # filename = "data" + gen.next_number() + ".csv"
        
        filename = "data.csv"

        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv",
        }
        return StreamingResponse(iter([buffer.getvalue()]), headers=headers, media_type="text/csv")
    except Exception as e:
        return "下载失败"