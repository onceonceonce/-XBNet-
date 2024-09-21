from io import StringIO
import pandas as pd
from fastapi import APIRouter, UploadFile


from Utils.write_data_database import write_data_into_database, write_patient_info_into_database

upload_router = APIRouter(prefix="/upload")

@upload_router.post("/uploadfile")
async def uploadfile(file: UploadFile):
    """
    post请求，上传csv文件,
    包括上传 原始数据文件，同时也包括处理之后的病人信息，将它们存储到数据库中去
    :return: 数据上传是否成功
    """
    #读取的是字节流
    file_byte = await file.read()
    # print(type(file_byte))
    # print(type(file.file))
    csv_string = file_byte.decode('utf-8')
    #转换成字符串流
    df = pd.read_csv(StringIO(csv_string))
    print("df")
    msg = await write_data_into_database(df)

    return msg




