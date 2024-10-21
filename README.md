Эта программа выполняет проверку USDT TRC20-адресов, сгенерированных из мнемонических фраз, на наличие транзакций и баланса. Программа выводит системные метрики (использование ЦП, оперативной памяти и жесткого диска) в реальном времени, и сохраняет результаты в файлы:

	Found_USDT_TRC20.txt — адреса, у которых есть транзакции.
	BAD_USDT_TRC20.txt — адреса без транзакций.

Инструкция по использованию:
Сначала установите все необходимые зависимости. 
Создайте файл requirements.txt с таким содержимым:

    requests
    blessed
    psutil
    rich
    cryptofuzz
    mnemonic

Далее выполните команду:

	pip install -r requirements.txt

Запустите скрипт в консоли командой:

	python Mnemonic USDT TRC20.py
 
 Для поддержки автора: TFbR9gXb5r6pcALasjX1FKBArbKc4xBjY8
--------------------------------------------------------------------------------------
This program performs a check of USDT TRC20 addresses generated from mnemonic phrases for transactions and balances. It also displays real-time system metrics (CPU, RAM, and disk usage), and saves the results to files:

	Found_USDT_TRC20.txt — contains addresses with transactions.
	BAD_USDT_TRC20.txt — contains addresses without transactions.
 
Usage Instructions:
First, install all necessary dependencies. Create a requirements.txt file with the following content:

    requests
    blessed
    psutil
    rich
    cryptofuzz
    mnemonic
 
Then, run the command:

	pip install -r requirements.txt
 
Start the script by running the following command in the console:

	python Mnemonic USDT TRC20.py

To support the author: TFbR9gXb5r6pcALasjX1FKBArbKc4xBjY8
