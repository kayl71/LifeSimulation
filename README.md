# Life Simulation project

### Coders: [Тимлид](https://github.com/kayl71),     [Ведомый](https://github.com/Midyadi)

### Structure:

    Source:       
          Code_source:
                     Creatures:
                              creatures.py - создание классов животных
                     Managers:   - обработчики появления и действий объектов
                             food_manager.py - обработчик еды
                             genome_manager.py - обработчик животных
                     Visuals:     - визуализаторы
                            display.py - отрисовщик объектов симуляции
                            menus.py - создание и обработка меню
          Data_source:
                     Pictures - картинки-лого    
    core.py - основная программа симуляции
    README.md - инфо  (вы здесь)
    requirements.txt - ПО, рекомендуемое для корректного запуска (использовалось при разработке)
         
### Info:
    
    Симуляция включает в себя 3 типа объектов:
                                             1. Хищники
                                             2. Травоядные
                                             3. Трава
    Первые едят вторых, вторые - третьих.
    Изменяя параметры симуляции в стартовом меню можно добиваться разных её исходов.

### Help:
    
    Чтобы открыть программу, запустите core.py.
    
    Поиграйте с настройками, нажав кнопку Options в главном меню.
    
    Запустите симуляцию кнопкой Play и наслаждайтесь массовым геноцидом, вымиранием или 
    стабильным развитием (смотря какие настройки выберете).
    
    Поставить симуляцию на паузу (кнопка Pause), возобновить её (кнопка Play) и выйти 
    в главное меню (кнопка End) можно, нажав кнопку Options в верхнем левом углу экрана.

    Приближаться и отдаляться можно колесиком мышки, перемещаться по карте - 
    стрелочками или WASD.
    
    
