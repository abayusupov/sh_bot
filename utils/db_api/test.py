from postgresql import Database
import asyncio
from datetime import datetime

db = Database()


async def test():

    await db.create()
    await db.create_table()
    # print('jadval yaratildi')
    # raqamlar = await db.count_all_voted_numbers()
    # print(raqamlar)
    hoz_vaqt = datetime.now()
    formatted_date = hoz_vaqt.strftime("%Y-%m-%d %H:%M:%S")
    # try:
    #     await db.add_number('+998907894785', 131455345,
    #                         datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S'), False, True)
    #     print('added successfully')
    # except Exception as e:
    #     print(f'xatolik {e}')

    # await db.update_payment('+998907894785')

    # not_paid_numbers = await db.select_all_not_paid_numbers()
    # data = [dict(row) for row in not_paid_numbers]
    # print(data)

    # paid_numbers = await db.select_all_paid_numbers()
    # data = [dict(row)['phone_number'] for row in paid_numbers if row]
    # print(data)

    # all = await db.count_all_numbers()
    # print(all)

    # all_paynet = await db.count_paynetga_numbers()
    # print(all_paynet)

    # all_savob = await db.count_savobga_numbers()
    # print(all_savob)

    # all_not_paid = await db.count_all_not_paid_numbers()
    # print(all_not_paid)

    # all_paid = await db.count_all_paid_numbers()
    # print(all_paid)

    # await db.add_temp('+998901234578', 21585545, False)

    # await db.update_me(564524548, '+998901234578')

    # await db.update_code(786786, 21585543)

    # mem_id = await db.get_member_id(21585542)
    # print(mem_id)

    is_taken = await db.is_taken_using_code(786786)
    print(is_taken)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
