from wonderworld import *

HEIGHT = 600
WIDTH = 800

PADDLE_WIDTH: float = 10.0
PADDLE_HEIGHT: float = 100.0
PADDLE_VELOCITY: float = 180.0
PADDLE_MAX_MOVE: float = HEIGHT - PADDLE_HEIGHT
PADDLE_MIN_MOVE: float = 0

BALL_WIDTH: float = 10.0
BALL_VELOCITY: Vector2 = Vector2(160.0, 160.0)

LINE_WIDTH: float = 2.0;


class Score(Resource):
    left: int
    right: int


class Ball(Component):
    pass


class Paddle(Component):
    up_key: int
    down_key: int


class Velocity(Component):
    value: Vector2


class LeftText(Component):
    pass


class RightText(Component):
    pass


def setup():
    commands = get_commands()
    assets = get_resource(Assets)

    # camera
    commands.spawn(Camera2dBundle(camera=Camera(),
                                  transform=Transform()))

    # ball
    ball_handle = assets.add(create_image(color=pygame.Color('white'),
                                          size=Vector2(BALL_WIDTH, BALL_WIDTH)))

    commands.spawn(SpriteBundle(sprite=Sprite(image=ball_handle),
                                transform=Transform(translation=Vector2(100, 100)),
                                visibility=Visibility(visible=True))) \
        .insert(Velocity(value=BALL_VELOCITY.copy())) \
        .insert(Ball())

    # line
    line_handle = assets.add(create_image(color=pygame.Color('white'),
                                          size=Vector2(LINE_WIDTH, HEIGHT)))
    commands.spawn(SpriteBundle(sprite=Sprite(image=line_handle),
                                transform=Transform(translation=Vector2(WIDTH / 2, 0)),
                                visibility=Visibility(visible=True)))
    # paddle_left
    left_handle = assets.add(create_image(color=pygame.Color('white'),
                                          size=Vector2(PADDLE_WIDTH, PADDLE_HEIGHT)))
    commands.spawn(SpriteBundle(sprite=Sprite(image=left_handle),
                                transform=Transform(translation=Vector2(0.0,
                                                                        HEIGHT / 2.0 - PADDLE_HEIGHT / 2)),
                                visibility=Visibility(visible=True))) \
        .insert(Paddle(up_key=K_w, down_key=K_a))

    # paddle_right
    right_handle = assets.add(create_image(color=pygame.Color('white'),
                                           size=Vector2(PADDLE_WIDTH, PADDLE_HEIGHT)))
    commands.spawn(SpriteBundle(sprite=Sprite(image=right_handle),
                                transform=Transform(translation=Vector2(WIDTH - PADDLE_WIDTH,
                                                                        HEIGHT / 2.0 - PADDLE_HEIGHT / 2)),
                                visibility=Visibility(visible=True))) \
        .insert(Paddle(up_key=K_UP, down_key=K_DOWN))

    # score
    asset_server = get_resource(AssetServer)
    font_size = 64
    commands.spawn(Text2dBundle(
        text =  Text(text="0",
                font =  asset_server.load("fonts/FiraSans-Bold.ttf",AssetType.FONT,size=font_size),
                font_size = font_size,
                color = Color('white')
            ),
        transform = Transform(translation=Vector2(WIDTH/4.0,200.)
    ))).insert(LeftText())
    commands.spawn(Text2dBundle(
        text=Text(text="0",
                  font=asset_server.load("fonts/FiraSans-Bold.ttf", AssetType.FONT, size=font_size),
                  font_size=font_size,
                  color=Color('white')
                  ),
        transform=Transform(translation=Vector2(3 *WIDTH / 4.0, 200.)
                            ))).insert(RightText())


def input():
    time = get_resource(Time)
    keyboard = get_resource(Keyboard)

    for (paddle, transform) in Query((Paddle, Transform)):
        paddle_move = time.delta_seconds * PADDLE_VELOCITY
        if keyboard.pressed(paddle.up_key):
            transform.translation.y = max(PADDLE_MIN_MOVE, transform.translation.y - paddle_move)
        if keyboard.pressed(paddle.down_key):
            transform.translation.y = min(PADDLE_MAX_MOVE, transform.translation.y + paddle_move)


def move_ball():
    time = get_resource(Time)
    for (transform, velocity) in Query((Transform, Velocity), With(Ball)):
        transform.translation += velocity.value * time.delta_seconds

        if transform.translation.y <= 0 or transform.translation.y + BALL_WIDTH >= HEIGHT:
            velocity.value.y = - velocity.value.y


def collides():
    for ball_transform, velocity in Query((Transform, Velocity), With(Ball)):
        ball_size = Vector2(BALL_WIDTH, BALL_WIDTH)
        for paddle_transform, in Query(Transform, With(Paddle)):
            paddle_size = Vector2(PADDLE_WIDTH, PADDLE_HEIGHT)
            if collide_aabb(ball_transform.translation, ball_size,
                            paddle_transform.translation, paddle_size):
                velocity.value.x = - velocity.value.x


def score():

    score = get_resource(Score)

    for transform, in Query(Transform,With(Ball)):
        if transform.translation.x < 0:
            score.right += 1
            transform.translation = Vector2(WIDTH/2,HEIGHT/2)
        elif transform.translation.x > WIDTH:
            score.left += 1
            transform.translation = Vector2(WIDTH/2,HEIGHT/2)

def show_score():
    score = get_resource(Score)

    for text, in Query(Text,With(LeftText)):
        text.text =  f"{score.left}"

    for text, in Query(Text,With(RightText)):
        text.text = f"{score.right}"

if __name__ == "__main__":
    App() \
        .insert_resource(ClearColor(color=pygame.Color('black'))) \
        .insert_resource(WindowDescriptor(
        title="wonderworld ping",
        width=WIDTH,
        height=HEIGHT,
        resizable=False)) \
        .insert_resource(Score(left=0, right=0)) \
        .add_plugins(DefaultPlugins()) \
        .add_startup_system(setup) \
        .add_system(input) \
        .add_system(move_ball) \
        .add_system(collides) \
        .add_system(score) \
        .add_system(show_score) \
        .run()

