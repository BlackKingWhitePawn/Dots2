# Игра в точки.

Точки - логическая пошаговая игра для двух (в нашей реализации и более) человек.
Игровое поле разлиновано на клетки, игроки ставят точки в перекрестия линий.
Размер поля произвольный, но как правило это прямоугольник 39 на 32.
Каждый игрок имеет свой цвет. Цель игры - окружать непрерывным рядом своих точек точки соперника(-ов).
Окруженные точки закрашиваются, а игроку, окружившему их, начисляются очки.
Игру можно провести по разному: немедленная победа при наборе некоторого количества очков,
до окончания места на поле, на время и многими другими способами.

Удачи!

***

- Точка входа - __main__.py, инициализация стартового окна StartWindow(), запуск, сохранение параметров запуска для Game
                - размеры, игроки, или загрузка сохраненных ранее, инициализация игры (Game()) и запуск (Game.run())
- Основной цикл - startWindow, game -> run()
- Обработка событий - run() -> handle_events()
- Отрисовка run() - draw()
- Служебная информация о текущей игре - gameInfo
- Параметры запуска игры - startWindow.data
- Система сохранений - saveLoad
- Объекты кнопок - button
- Объекты игроков - player -> playerMan / playerBot / playerBotRandom
- Логика ботов - playerBot -> make_move()
- Юнит-тесты - testGame
- Изображения - Images
- Цвета (rgb) - Colors