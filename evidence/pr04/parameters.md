## Стадия 1 — Объявленные параметры и дефолты

| Параметр       | Дефолт | 
|----------------|--------|
| linear_speed   | 0.5    | 
| turn_rate      | 0.3    | 
| publish_hz     | 10.0   |

Команда проверки списка параметров:
```
root@be2b72369ede:/repos# ros2 param list /patrol
  linear_speed
  publish_hz
  start_type_description_service
  turn_rate
  use_sim_time
```

Частота до поломки:
```
root@be2b72369ede:/repos# ros2 param get /patrol publish_hz
Double value is: 10.0
```

## Стадия 2 — Сломать (проверка publish_hz отключена)

Запуск ноды:
`ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel`

Устанавливаем недопустимую частоту:
`ros2 param set /patrol publish_hz 0.0`

Команда зависла — нода упала с `ZeroDivisionError`.   

### Проверка, что нода мертва:
`ros2 node list`
```
    /sim
```
`/patrol` отсутствует — нода уничтожена.

### Вывод ноды в момент падения:
```
^C[ros2run]: Received signal:  Interrupt
Traceback (most recent call last):
  File "/repos/install/patrol/lib/patrol/patrol", line 33, in <module>
    sys.exit(load_entry_point('patrol', 'console_scripts', 'patrol')())
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/repos/build/patrol/patrol/patrol.py", line 96, in main
    node.destroy_node()
    ~~~~~~~~~~~~~~~~~^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 2702, in destroy_node
    self.destroy_publisher(self._publishers[0])
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 2609, in destroy_publisher
    publisher.destroy()
    ~~~~~~~~~~~~~~~~~^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/publisher.py", line 101, in destroy
    self._destroy()
    ~~~~~~~~~~~~~^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/publisher.py", line 189, in _destroy
    super()._destroy()
    ~~~~~~~~~~~~~~~~^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/publisher.py", line 104, in _destroy
    self.handle.destroy_when_not_in_use()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
KeyboardInterrupt
[ros2run]: Interrupt
root@be2b72369ede:/repos# ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
Traceback (most recent call last):
  File "/repos/install/patrol/lib/patrol/patrol", line 33, in <module>
    sys.exit(load_entry_point('patrol', 'console_scripts', 'patrol')())
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/repos/build/patrol/patrol/patrol.py", line 92, in main
    rclpy.spin(node)
    ~~~~~~~~~~^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/__init__.py", line 324, in spin
    executor.spin_once()
    ~~~~~~~~~~~~~~~~~~^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 1020, in spin_once
    self._spin_once_impl(timeout_sec)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 1012, in _spin_once_impl
    raise exception
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/task.py", line 343, in _execute_coroutine_step
    result = coro.send(None)
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 670, in handler
    await call_coroutine()
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 604, in _execute
    response = await await_or_execute(srv.callback, request, srv.srv_type.Response())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 139, in await_or_execute
    return callback(*args)
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/parameter_service.py", line 142, in _set_parameters_callback
    result = node.set_parameters_atomically([param])
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 820, in set_parameters_atomically
    return self._set_parameters_atomically(parameter_list)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 840, in _set_parameters_atomically
    return self._set_parameters_atomically_common(parameter_list)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 890, in _set_parameters_atomically_common
    result = callback(parameter_list)
  File "/repos/build/patrol/patrol/patrol.py", line 80, in _on_set_parameters
    self.timer = self.create_timer(1.0 / self._publish_hz, self._on_timer)
                                   ~~~~^~~~~~~~~~~~~~~~~~
ZeroDivisionError: division by zero
[ros2run]: Process exited with failure 1
```

Недопустимое значение `0.0` прошло через отсутствующую валидацию, привело к делению на ноль и уничтожило ноду.

## Стадия 3 · Исправление (проверка восстановлена)

Успешная смена частоты с 10 до 5 Гц:
```
root@be2b72369ede:/repos# ros2 param set /patrol publish_hz 5.0
Set parameter successful
```

В логе ноды:
```
[INFO] [1791707288.038794983] [patrol]: timer rebuilt, period=0.2000s
```

Измерение реальной частоты публикации:
```
root@be2b72369ede:/repos# ros2 topic hz /turtle1/cmd_vel -w 20
average rate: 5.002
        min: 0.199s max: 0.200s std dev: 0.00040s window: 4
average rate: 5.001
        min: 0.199s max: 0.201s std dev: 0.00042s window: 9
```
Старый таймер остановлен, новый таймер работает с периодом 0.2 с.

Отклонение нуля:
```
root@be2b72369ede:/repos# ros2 param set /patrol publish_hz 0.0
Setting parameter failed: publish_hz 0.0 out of [1, 30]
```

Проверка, что старое значение сохранено:
```
root@be2b72369ede:/repos# ros2 param get /patrol publish_hz
Double value is: 5.0
```
Значение и поток команд остались прежними.

Отрицательная скорость:
```
root@be2b72369ede:/repos# ros2 param set /patrol linear_speed -0.5
Setting parameter failed: linear_speed -0.5 out of [0, 1]
```