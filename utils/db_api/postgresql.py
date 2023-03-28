from typing import Union
import asyncio
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(user=config.DB_USER, password=config.DB_PASS, database=config.DB_NAME, host=config.DB_HOST, , port=6233)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS phone_numbers (
                id SERIAL,
                phone_number TEXT PRIMARY KEY,
                telegram_id INTEGER,
                datetime TIMESTAMP,
                paid BOOLEAN,
                donate BOOLEAN
            );
        CREATE TABLE IF NOT EXISTS temp (
                id SERIAL PRIMARY KEY,
                phone_number TEXT,
                telegram_id INTEGER,
                member_id INTEGER,
                taken BOOLEAN,
                donate BOOLEAN,
                code INTEGER
            );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_number(self, phone_number, telegram_id, datetime, paid, donate):
        sql = "INSERT INTO phone_numbers (phone_number, telegram_id, datetime, paid, donate) VALUES ($1, $2, $3, $4, $5)"
        return await self.execute(sql, phone_number, telegram_id, datetime, paid, donate, execute=True)

    async def update_payment(self, phone_number):
        sql = "UPDATE phone_numbers SET paid=True where phone_number=$1"
        return await self.execute(sql, phone_number, execute=True)

    async def select_all_not_paid_numbers_with_time(self):
        sql = "SELECT phone_number, datetime FROM phone_numbers where donate=False and paid=False"
        return await self.execute(sql, fetch=True)

    async def select_all_not_paid_numbers(self):
        sql = "SELECT phone_number, datetime FROM phone_numbers where donate=False and paid=False"
        return await self.execute(sql, fetch=True)

    async def select_all_paid_numbers(self):
        sql = "SELECT phone_number FROM phone_numbers where donate=False and paid=True"
        return await self.execute(sql, fetch=True)

    async def count_all_numbers(self):
        sql = "SELECT COUNT(*) FROM phone_numbers"
        return await self.execute(sql, fetchval=True)

    async def count_all_not_paid_numbers(self):
        sql = "SELECT COUNT(*) FROM phone_numbers where paid=False and donate=False"
        return await self.execute(sql, fetchval=True)

    async def count_all_paid_numbers(self):
        sql = "SELECT COUNT(*) FROM phone_numbers where paid=True"
        return await self.execute(sql, fetchval=True)

    async def count_savobga_numbers(self):
        sql = "SELECT COUNT(*) FROM phone_numbers where donate=True"
        return await self.execute(sql, fetchval=True)

    async def count_paynetga_numbers(self):
        sql = "SELECT COUNT(*) FROM phone_numbers where donate=False"
        return await self.execute(sql, fetchval=True)

    async def add_temp(self, phone_number, telegram_id, donate, member_id=None, code=None, taken=False):
        sql = "INSERT INTO temp (phone_number, telegram_id, donate, member_id, code, taken) VALUES ($1, $2, $3, $4, $5, $6)"
        return await self.execute(sql, phone_number, telegram_id, donate, member_id, code, taken, execute=True)

    async def update_me(self, member_id, phone_number):
        sql = "UPDATE temp SET member_id=$1, taken=True where phone_number=$2"
        return await self.execute(sql, member_id, phone_number, execute=True)

    async def update_code(self, code, user_id):
        sql = "UPDATE temp SET code=$1 where id=(select max(id) from temp where telegram_id=$2)"
        return await self.execute(sql, code, user_id, execute=True)

    async def get_user_id(self, member_id, phone_number):
        sql = "SELECT telegram_id FROM temp where member_id=$1 AND phone_number=$2 order by id desc"
        return await self.execute(sql, member_id, phone_number, fetchval=True)

    async def get_member_id(self, telegram_id):
        sql = "SELECT member_id FROM temp where telegram_id=$1 order by id desc"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def get_user_id_temp(self, phone_number):
        sql = "SELECT telegram_id FROM temp where id=(select max(id) from temp where phone_number=$1)"
        return await self.execute(sql, phone_number, fetchval=True)

    async def get_user_id_using_code(self, code):
        sql = "SELECT telegram_id FROM temp where id=(select max(id) from temp where code=$1)"
        return await self.execute(sql, int(code), fetchval=True)

    async def get_user_id_using_phone(self, phone_number):
        sql = "SELECT telegram_id FROM temp where id=(select max(id) from temp where phone_number=$1)"
        return await self.execute(sql, phone_number, fetchval=True)

    async def get_phone_number_using_code(self, code):
        sql = "SELECT phone_number FROM temp where id=(select max(id) from temp where code=$1)"
        return await self.execute(sql, int(code), fetchval=True)

    async def get_donate_using_code(self, code):
        sql = "SELECT donate FROM temp where id=(select max(id) from temp where code=$1)"
        return await self.execute(sql, int(code), fetchval=True)

    async def get_phone_number_using_user_id(self, user_id):
        sql = "SELECT phone_number FROM temp where id=(select max(id) from temp where telegram_id=$1)"
        return await self.execute(sql, user_id, fetchval=True)

    async def is_taken(self, phone_number):
        sql = "SELECT taken FROM temp where id=(select max(id) from temp where phone_number=$1)"
        return await self.execute(sql, phone_number, fetchval=True)

    async def is_taken_using_code(self, code):
        sql = "SELECT taken FROM temp where id=(select max(id) from temp where code=$1)"
        return await self.execute(sql, code, fetchval=True)

    # async def get_temp_row(self, code):
    #     sql = "SELECT * FROM temp where id=(select max(id) from temp where code=$1)"
    #     return await self.execute(sql, code, fetchrow=True)

    # async def delete_users(self):
    #     await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    # async def drop_users(self):
    #     await self.execute("DROP TABLE Users", execute=True)
