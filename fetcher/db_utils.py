"""
Модуль, содержащий утилиты для работы с базой: запись и чтение
"""
from asyncio import sleep

from typing import Tuple, AsyncIterable

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from custom_types import PermissionsType

client = AsyncIOMotorClient('mongo')
db = client.AppFollow


async def permission_requests() -> AsyncIterable[Tuple[ObjectId, str, str]]:
    """
    Генератор, следящий за изменениями в коллекции и возвращающий данные запроса разрешений
    """
    query = {'permissions': {'$exists': False}, 'error': {'$exists': False}}
    while True:
        async for document in db.application_data.find(query):
            id_ = document['_id']
            application_id = document['application_id']
            language = document['language']
            yield (id_, application_id, language)
        await sleep(1)


async def save_permission(id_: ObjectId, permissions: PermissionsType):
    """
    Добавляет разрешение приложения к запросу
    """
    await db.application_data.update_one(
        {'_id': id_},
        {'$set': {'permissions': permissions}},
    )


async def set_error(id_: ObjectId):
    """
    Помечает запрос ошибочным
    """
    await db.application_data.update_one(
        {'_id': id_},
        {'$set': {'error': True}},
    )
