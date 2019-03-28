# diary
Это приложение создано для того чтобы заменить им ваш личный дневник.

Для того чтобы начать пользоваться своим дневником, его необходимо завести (или же зарегистрироваться)
Если у вас уже есть дневник необходимо его открыть (или же залогиниться)
Для вышеперечисленного существуют соответствующие формы и обработчики


# функционал
- Здесь предусмотрена возможность добавления "Ноутов"(записей), для этого достаточно нажать на зелёную кнопку с буквой "A" на стартовой странице приложения (/index). Откроется форма для создания записи. Заголовок записи - обязательный атрибут. Создать или изменить запись с пустым заголовком нельзя.
- После создания записи вас перекинет на главную страницу (/index) где отображаются все записи пользователя.
- Предусмотренна возможность сортировки записей по дате(значение по умолчанию) и по алфавиту для более удобного поиска. (необходимо нажать на кнопку с надписью "S" (/index) для изменения фильтра)
- Также есть возможность удалить запись, для этого необходимо нажать на значок ведра на соответствующем ноуте. После этого запись будет удалена.

- У каждого пользователя есть свой профиль в котором можно поменять логин и пароль (при условии если пользователь знает текущий пароль на аккаунте). Также можно удалить свой аккаунт, для этого нужно нажать на красную кнопку в профиле.
- Будьте осторожны, если нажмёте на кнопку "Удалить аккаунт", то вернуть его уже не получится))
- В профиле нельзя изменять привелегии(пользователь/админ)(читайте далее). Это делается непосредственно при обращении к БД

- Ну и весь этот функционал имеет своеобразный внешний вид (На мой взгляд не самый плохой)


# аккаунт для мониторинга активности
- В базе данных по умолчанию существует аккаунт администратора(Логин: root, Пароль: toor)
- Пароли и логины можно изменять в профиле аккаунта
- На данном аккаунте есть дополнительная ссылка на навигационной панели, которая ведёт на страницу, содержащую информацию о кол-ве пользователей данного приложения (аккаунтов) и количества записей каждого из пользователей (текст и заголовки записей хранятся в секрете))
- ВНИМАНИЕ: доступ к данной странице есть только на аккаунте администратора.


