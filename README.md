# wonderworld - Dataoriented Python Game Engine

<img src="img/logo.png" width="128" align="left"><br><br><br><br><br><br>

* **Game Engine** implemented on **Database Engine (in memory with pandas)**
* **world** is a **database**
* **archetype** is a **table**
* **entity** is a **row(id)**
* **componenten** is one **column**
* **system** is a **function**
* **query** is a **database query**

*I have long wanted to program games in Pygame using the Entity Component System (ECS) game design pattern. Once when I looked at the Bevy game framework in Rust, I was hooked. I wanted something like that in Python too.
Since I couldn't find such a framework anywhere, I started developing a Python ECS framework myself -* **wonderworld**

## Entity Component System ECS

The data-oriented programming (DOP) approach tries to strictly separate data and program from each other.

One way to do this is with the **Entity Component System** (ECS) design pattern.

A **component** in the ECS design pattern contains only data.

Examples:

* Transform(x,y) - TransformComponent
* Speed (x,y) - SpeedComponent
* Sprite(image) - ImageComponent

A component does not contain any processing logic.

An **entity** is a game object, such as the knight. It consists of any number of components and does not itself contain any data or program logic. A unique ID linked to the components via an internal data structure is sufficient for the implementation of an entity.

A **system** contains the complete processing logic, but no own data. A game can consist of any number of systems. A system reads components and transforms their current state into another.

For example, the **Movement system** retrieves all speed components (SpeedComponents) and transform components (PositionComponent) in order to calculate the new position from them.

<img src="img/system.png" width="512"  hspace=20 align="left"><br><br><br><br><br><br>

## Bevy

<img src="https://bevyengine.org/assets/bevy_logo_dark.svg" width="256" style="background-color:black;" hspace=20 align="left"><br><br><br><br><br><br>

https://bevyengine.org

## pygame

<img src="https://www.pygame.org/images/logo_lofi.png" width="256" style="background-color:black;" hspace=20 align="left"><br><br><br><br><br><br>

https://www.pygame.org

## Example first.py

<img src="img/first.gif" width="256" align="left"><br><br><br><br><br><br><br><br>


```python
%gui qt
from wonderworld import *

PADDLE_VELOCITY:float = 180.0

@dataclass
class Paddle(Component):
    pass


def setup():
    commands = get_commands()
    assets = get_resource(Assets)

    image_handle = assets.add(create_image(color=pygame.Color('white'),
                                              size=Vector2(10.0, 100.0)))

    #camera
    commands.spawn(Camera2dBundle(camera=Camera(),
                                  transform=Transform(translation=Vector3(0,0,0),
                                                      rotation=0,
                                                      scale=Vector2(0,0))))

    #paddle
    commands.spawn(SpriteBundle(sprite = Sprite (image=image_handle),
                                transform = Transform(translation=Vector3(100,100,0),
                                                      rotation=0,
                                                      scale=Vector2(0,0)),
                                visibility=Visibility(True)))\
        .insert(Paddle())


def input():
    time = get_resource(Time)
    keyboard_input = get_resource(Keyboard)

    for transform, in Query(Transform, With(Paddle)):
        paddle_move = time.delta_seconds * PADDLE_VELOCITY
        if keyboard_input.pressed(K_UP):
            transform.translation.y = transform.translation.y - paddle_move

        if keyboard_input.pressed(K_DOWN):
            transform.translation.y =transform.translation.y + paddle_move


if __name__ == "__main__":
    App().insert_resource(ClearColor(pygame.Color('black')))\
        .add_plugins(DefaultPlugins())\
        .add_startup_system(setup)\
        .add_system(input)\
        .run()
```

    pygame 2.1.2 (SDL 2.0.18, Python 3.9.16)
    Hello from the pygame community. https://www.pygame.org/contribute.html


## Example ping.py


```python

```


```python

```

* Let's build an Entity Component System from scratch (part 1) https://devlog.hexops.com/2022/lets-build-ecs-part-1/
* Let's build an Entity Component System (part 2): databases https://devlog.hexops.com/2022/lets-build-ecs-part-2-databases/


```python

```
