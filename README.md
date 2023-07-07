# Gate-tg-bot
Описание:
Данный код является реализацией тестового задания, которое предполагает создание бота для упрощения коммуникации при въезде автомобилей на территорию предприятия. Бот позволяет пользователям отправлять запросы на въезд, содержащие информацию о имени, номере машины, месте назначения и контактном лице. Запросы получают ответственные лица в закрытой группе, которые могут принять решение о пропуске. Ответ одного ответственного убирает кнопки выбора у всех. При положительном ответе, информация о запросе и имени ответственного отправляется на вахту и пользователям, получившим одобрение. При отрицательном ответе, информация о отказе и комментарий отправляются пользователям и ответственным.

Используемые библиотеки:
  •	json: используется для работы с JSON-форматом данных.
  •	re: используется для работы с регулярными выражениями.
  •	telebot: библиотека для работы с Telegram Bot API.
  •	logging: используется для логирования.
Установка и настройка:
  1.	Установите необходимые библиотеки, выполнив команду pip install pyTelegramBotAPI.
  2.	Получите API-токен для вашего бота, создав его через BotFather в Telegram.
  3.	Склонируйте репозиторий или загрузите файлы проекта на вашу локальную машину.
  4.	Установите API-токен в переменную TOKEN в строке bot = telebot.TeleBot('YOUR_TOKEN').
  5.	Создайте две новые беседы в Telegram. Узнайте их идентификаторы (chat ID) с помощью бота @getidsbot или других доступных инструментов.
  6.	В файле main.py найдите переменные CLOSED_CHAT_ID_RESPONSIBLE и CLOSED_CHAT_ID_VAHTA и замените их значения на идентификаторы ваших созданных бесед.
  7.	Пригласите вашего бота в эти две беседы и предоставьте ему административные права с разрешением на отправку сообщений.
  8.	Сохраните внесенные изменения в файле main.py.
  9.	Запустите бота, выполните следующую команду: python main.py
После выполнения указанных шагов, ваш бот будет готов к использованию, и вы сможете начать тестирование и взаимодействие с ним.

Убедитесь, что вся необходимая информация, такая как API-токен бота и идентификаторы бесед, правильно введены и настроены для вашего проекта.
Основные функции:
  1.	/start - команда для начала диалога с ботом и отправки запроса на въезд.
  2.	get_name(message) - обработчик получения ФИО пользователя.
  3.	get_destination(message) - обработчик получения направления пользователя.
  4.	get_contact_person(message) - обработчик получения имени контактного лица.
  5.	get_car_number(message) - обработчик получения номера машины пользователя.
  6.	send_greeting(message) - обработчик нажатия кнопки "Отправить" для отправки запроса в закрытую группу.
  7.	handle_group_button_click(call) - обработчик нажатия кнопок "Принять" и "Отказать" в закрытой группе.
  8.	restart(message) - обработчик нажатия кнопки "Начать заново" для сброса состояний и данных.
Обработка ошибок:
В коде предусмотрены обработчики исключений для логирования ошибок, которые могут возникнуть при выполнении различных операций.
Примечание:
Данный код предоставляет основу для разработки бота, который может быть использован для упрощения коммуникации при въезде автомобилей на территорию предприятия. Код может быть доработан и расширен в соответствии с требованиями и потребностями проекта.
