import asyncio

from binance.client import Client, AsyncClient



async def find_user_transaction(expected_amount: float = 1, target_pay_id=389555070, target_coin: str = 'USDT'):
    """Проверяем поступление средств"""
    client = await AsyncClient.create(api_key=API_KEY, api_secret=BINANCE_SECRET)
    # Получаем текущее время и вычисляем начало интервала последнего часа
    import time
    now = int(time.time() * 1000)
    one_hour_ago = now - 3600000  # 1 час в миллисекундах
    try:

        # Получаем все депозиты за последний час
        deposits = await client.get_pay_trade_history()
        print(deposits)
        # Ищем депозиты, совпадающие с target_pay_id, target_coin и суммой expected_amount USDT
        target_deposits = []
        for deposit in deposits:
            if deposit['status'] == 1:  # 1 - успешный депозит
                if deposit['address'] == target_pay_id and deposit['asset'] == target_coin:
                    # Проверка точной суммы депозита
                    if float(deposit['amount']) == expected_amount:
                        target_deposits.append(deposit)
        print(target_deposits)
        if target_deposits:
            # Если найдены депозиты, выводим информацию о них
            for deposit in target_deposits:
                print(f"Найден успешный депозит от пользователя {target_pay_id}:")
                print(f"Дата: {deposit['insertTime']}")
                print(f"Сумма: {deposit['amount']} {deposit['asset']}")
        else:
            # Если не найдены подходящие депозиты, выводим сообщение
            print(
                f"Успешные депозиты от пользователя {target_pay_id} в {target_coin} за последний час не найдены.")
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем соединение с Binance API
        await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(find_user_transaction())