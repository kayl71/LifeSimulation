Life Simulation project

Coders: [Тимлид](https://github.com/kayl71),     [Ведомый](https://github.com/Midyadi)

Structure:

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
         
Info:
    
    Симуляция включает в себя 3 типа объектов: 
                                             хищники 
                                             травоядные
                                             трава
    Первые едят вторых, вторые - третьих.
    Изменяя параметры симуляции в стартовом меню можно добиваться разных её исходов.
