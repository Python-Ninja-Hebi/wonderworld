from wonderworld import *

HEIGHT = 600
WIDTH = 800

PADDLE_WIDTH: float = 10.0
PADDLE_HEIGHT: float = 100.0
PADDLE_VELOCITY: float = 180.0
PADDLE_MAX_MOVE: float = HEIGHT - PADDLE_HEIGHT
PADDLE_MIN_MOVE: float = 0

BALL_WIDTH: float = 10.0
BALL_VELOCITY: Vector3 = Vector3(160.0, 160.0, 0.0)

LINE_WIDTH: float = 2.0;


@dataclass
class Score(Resource):
    left: int
    right: int


@dataclass
class Ball(Component):
    pass


@dataclass
class Paddle(Component):
    up_key: int
    down_key: int


@dataclass
class Velocity(Component):
    value: Vector3


@dataclass
class LeftText(Component):
    pass


@dataclass
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
                                transform=Transform(translation=Vector3(100, 100, 0)),
                                visibility=Visibility(True))) \
        .insert(Velocity(BALL_VELOCITY.copy())) \
        .insert(Ball())

    # line
    line_handle = assets.add(create_image(color=pygame.Color('white'),
                                          size=Vector2(LINE_WIDTH, HEIGHT)))
    commands.spawn(SpriteBundle(sprite=Sprite(image=line_handle),
                                transform=Transform(translation=Vector2(WIDTH / 2, 0)),
                                visibility=Visibility(True)))
    # paddle_left
    left_handle = assets.add(create_image(color=pygame.Color('white'),
                                          size=Vector2(PADDLE_WIDTH, PADDLE_HEIGHT)))
    commands.spawn(SpriteBundle(sprite=Sprite(image=left_handle),
                                transform=Transform(translation=Vector2(0.0,
                                                                        HEIGHT / 2.0 - PADDLE_HEIGHT / 2)),
                                visibility=Visibility(True))) \
        .insert(Paddle(up_key=K_w, down_key=K_a))

    # paddle_right
    right_handle = assets.add(create_image(color=pygame.Color('white'),
                                           size=Vector2(PADDLE_WIDTH, PADDLE_HEIGHT)))
    commands.spawn(SpriteBundle(sprite=Sprite(image=right_handle),
                                transform=Transform(translation=Vector2(WIDTH - PADDLE_WIDTH,
                                                                        HEIGHT / 2.0 - PADDLE_HEIGHT / 2)),
                                visibility=Visibility(True))) \
        .insert(Paddle(up_key=K_UP, down_key=K_DOWN))

    # score
    # commands.spawn(Text2dBundle {
    #    text: Text::from_section(
    #        "0",
    #        TextStyle {
    #            font: asset_server.load("fonts/FiraSans-Bold.ttf"),
    #            font_size: 64.0,
    #            color: Color::WHITE,
    #        }),
    #    transform: Transform::from_xyz(-WIDTH/4.0,200.,1.),
    #    ..Default::default()
    # })
    #    .insert(LeftText{});
    # commands.spawn(Text2dBundle {
    #    text: Text::from_section(
    #        "0",
    #        TextStyle {
    #            font: asset_server.load("fonts/FiraSans-Bold.ttf"),
    #            font_size: 64.0,
    #            color: Color::WHITE,
    #        }),
    #    transform: Transform::from_xyz(WIDTH/4.0,200.,1.),
    #    ..Default::default()
    # })
    #    .insert(RightText{});


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


#
# fn score(
#    mut score:ResMut<Score>,
#    mut query: Query<&mut Transform,With<Ball>>,
# )
# {
#    for mut transform in query.iter_mut() {
#        if transform.translation.x < -WIDTH / 2.0 {
#            score.right += 1;
#            transform.translation = Vec3::ZERO;
#        }
#        if transform.translation.x > WIDTH / 2.0 {
#            score.left += 1;
#            transform.translation = Vec3::ZERO;
#        }
#    }
# }

# fn show_score(
#    score:Res<Score>,
#    mut left_query: Query<&mut Text,(With<LeftText>,Without<RightText>)>,
#    mut right_query: Query<&mut Text,(With<RightText>,Without<LeftText>)>,
# ){
#    for mut text in left_query.iter_mut() {
#        text.sections[0].value = format!("{}", score.left);
#    }
#   for mut text in right_query.iter_mut() {
#        text.sections[0].value = format!("{}", score.right);
#    }
# }

if __name__ == "__main__":
    App() \
        .insert_resource(ClearColor(pygame.Color('black'))) \
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
        .run()
    #  .add_system(score) \
    #  .add_system(show_score)
