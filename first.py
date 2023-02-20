from wonderworld import *

PADDLE_VELOCITY: float = 180.0

@dataclass
class Paddle(Component):
    pass


def setup():
    commands = get_commands()
    assets = get_resource(Assets)

    # asset_server = get_resource(AssetServer)
    # image_handle = asset_server.load("box.png");

    image_handle = assets.add(create_image(color=pygame.Color('white'),
                                           size=Vector2(10.0, 100.0)))

    # camera
    commands.spawn(Camera2dBundle(camera=Camera(),
                                  transform=Transform(translation=Vector2(0,0),
                                                      rotation=0,
                                                      scale=Vector2(0, 0))))

    # paddle
    commands.spawn(SpriteBundle(sprite=Sprite(image=image_handle),
                                transform=Transform(translation=Vector2(100, 100),
                                                    rotation=0,
                                                    scale=Vector2(0, 0)),
                                visibility=Visibility(True))) \
        .insert(Paddle())


def input():
    time = get_resource(Time)
    keyboard_input = get_resource(Keyboard)

    for transform, in Query(Transform, With(Paddle)):
        paddle_move = time.delta_seconds * PADDLE_VELOCITY
        if keyboard_input.pressed(K_UP):
            transform.translation.y = transform.translation.y - paddle_move

        if keyboard_input.pressed(K_DOWN):
            transform.translation.y = transform.translation.y + paddle_move


if __name__ == "__main__":
    App().insert_resource(ClearColor(pygame.Color('black'))) \
        .add_plugins(DefaultPlugins()) \
        .add_startup_system(setup) \
        .add_system(input) \
        .run()
