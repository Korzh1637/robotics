# Команды и наблюдения ПР02

## Условия опыта

Ubuntu 26.04 / ROS 2 Lyrical, `ROS_DOMAIN_ID=43`.
Настоящий turtlesim работал с `QT_QPA_PLATFORM=offscreen`, без видимого окна.
В контейнер смонтирован репозиторий как `/repos`, команды выполнялись от
пользователя хоста. Teleop не запускался. Среда подключена в каждом терминале:

```bash
source /opt/ros/lyrical/setup.bash
source /work/install/setup.bash  # после сборки
export ROS_DOMAIN_ID=43
```

## Linux на файлах этой работы

| Выполненная команда | Назначение | Наблюдение |
|---|---|---|
| `pwd` | Текущий каталог | `/repos`, корень workspace |
| `printenv ROS_DISTRO ROS_DOMAIN_ID` | Вывод id и названия дистрибутива | `lyrical`, `43` |
| `mkdir -p src evidence/pr02` | Создание новой директории | Отсутствует |

`>` записывает stdout в файл, заменяя его прежнее содержимое; `|` передаёт
stdout следующему процессу.
`source` выполняет файл в текущей оболочке и сохраняет изменения её окружения.
Запуск новой программы создаёт дочерний процесс: его изменения окружения
не возвращаются в родительский терминал. Ни сборка, ни source сами не запускают ноду.

## Запуск и остановка

В A: `ros2 launch turtle_bringup sim.launch.py`.
В B: `ros2 node list --no-daemon --spin-time 2`.
В [nodes-running.txt](nodes-running.txt) есть `/turtlesim`.
После SIGINT группе launch (эквивалент Ctrl+C в терминале) launch завершился
с кодом 0; в [nodes-stopped.txt](nodes-stopped.txt) ноды нет.
Launch запущен повторно; [nodes-restarted.txt](nodes-restarted.txt) подтверждает граф.
[launch-first.txt](launch-first.txt) и [launch-experiment.txt](launch-experiment.txt)
содержат реальные журналы обоих запусков, включая завершение дочернего процесса.

## Правильное имя, сбой, исправление

Правильное имя, сбой, исправление

В эксперименте проверялось, какое имя топика необходимо использовать для
передачи команд скорости узлу turtlesim.

Состояние до исправления

Сначала была проверена информация о топике /cmd_vel.

Команда
```ros2 topic info /cmd_vel --verbose```
Вывод
```
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: _ros2cli_437
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.70.b7.b5.01.5b.83.00.00.00.00.00.00.07.03
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (10)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

Subscription count: 0
```

Топик /cmd_vel имеет одного издателя, но подписчиков на него нет.

После этого была проверена информация о топике /turtle1/cmd_vel, который
использует turtlesim.

Команда
```ros2 topic info /turtle1/cmd_vel --verbose```
Вывод
```
Type: geometry_msgs/msg/Twist

Publisher count: 0

Subscription count: 1

Node name: turtlesim
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: SUBSCRIPTION
GID: 01.0f.70.b7.e7.00.05.f7.00.00.00.00.00.00.1c.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (7)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite
```

Таким образом, /cmd_vel и /turtle1/cmd_vel являются разными топиками,
несмотря на то, что имеют одинаковый тип сообщения
geometry_msgs/msg/Twist.

turtlesim подписан именно на /turtle1/cmd_vel.

Публикация в неправильный топик

Для проверки была запущена публикация сообщений в /cmd_vel.

Команда
```
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

После этого снова была проверена информация о /cmd_vel.

Команда
```ros2 topic info /cmd_vel --verbose```
Вывод
```Unknown topic '/cmd_vel'```

При этом проверка /turtle1/cmd_vel показала, что именно этот топик
соединён с turtlesim.

Исправление имени топика

После исправления имени на /turtle1/cmd_vel была повторно проверена
информация о топике.

Команда
```ros2 topic info /turtle1/cmd_vel --verbose```
Вывод
```
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: _ros2cli_224
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.eb.7d.e0.00.b1.0a.00.00.00.00.00.00.07.03
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (10)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC

Subscription count: 1

Node name: turtlesim
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: SUBSCRIPTION
GID: 01.0f.eb.7d.57.00.13.f7.00.00.00.00.00.00.1c.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (7)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite
```

После исправления имени топика появился один издатель и один подписчик.

Издателем является _ros2cli_224, а подписчиком — turtlesim.

## Вывод

В ходе эксперимента было проверено взаимодействие издателя и подписчика
ROS 2 через топики типа geometry_msgs/msg/Twist.

Изначально топик /cmd_vel имел одного издателя, но не имел подписчиков.
В то же время /turtle1/cmd_vel имел одного подписчика — узел turtlesim.

Таким образом, /cmd_vel и /turtle1/cmd_vel являются разными топиками.
Совпадение типа сообщения geometry_msgs/msg/Twist не создаёт соединение
между топиками с разными именами.

Публикация сообщения в /cmd_vel не привела к появлению связи с
turtlesim, поскольку turtlesim подписан на /turtle1/cmd_vel.

После исправления имени топика на /turtle1/cmd_vel была установлена связь:

Publisher count: 1
Subscription count: 1

Издателем стал _ros2cli_224, а подписчиком — turtlesim.

Следовательно, для взаимодействия узлов ROS 2 необходимо совпадение имени
топика и совместимого типа сообщения. В данном эксперименте ошибка была
связана именно с использованием /cmd_vel вместо /turtle1/cmd_vel.