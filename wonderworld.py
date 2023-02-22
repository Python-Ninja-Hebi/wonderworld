from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type, Callable, Dict, Any, List, Tuple, Union, Set, FrozenSet

import pandas as pd

import pygame
from pygame import *
from pygame import Color
from pygame.math import Vector2, Vector3
from pygame.surface import Surface

from todo import todo
from enum import Enum

# ---- Entity Component System ECS ----

@dataclass
class Component:
    pass

@dataclass
class Bundle:
    pass

unique_entity_id = 0
def get_unique_entity_id()->int:
    global unique_entity_id
    unique_entity_id+=1
    return unique_entity_id

class Plugin:
    def build(self, app: App):
        pass


class PluginGroup:
    def build(self) -> List[Plugin]:
        pass

# ---- Resources ----

@dataclass
class Resource:
    pass

class Resources:
    """all resources"""

    def __init__(self):
        self._resources: Dict[Type, Any] = {}

    def add(self, resource: Any) -> None:
        if type(resource) in self._resources:
            raise Exception(f'Resource with type {type(resource)} already exits.')
        self._resources[type(resource)] = resource

    def __getitem__(self, item: Type) -> Resource:
        return self._resources[item]

def get_resource(t: Type) -> Resource:
    return _app.resources[t]

def in_resource(t: Type) -> bool:
    return t in _app.resources._resources.keys()

# ---- Commands ----

class EntityCommand:
    def execute(self):
        pass

class InsertCommand(EntityCommand):
    def __init__(self,component:Component):
        self.component = component

class EntityCommands:
    def __init__(self):
        self.entity_id = get_unique_entity_id()
        self.commands:List[EntityCommand] = []

    def insert(self, components: Union[Tuple[Component], Component]) -> EntityCommands:
        if isinstance(components,Component):
            self.commands.append(InsertCommand(components))
        elif isinstance(components,Tuple):
            for i in components:
                if not isinstance(i,Component):
                    raise Exception("Component expected")
                self.commands.append(InsertCommand(components))
        else:
            raise Exception("Component or Tuple of Components expected")
        return self

    def apply(self)->None:
        component_list = []
        for i in self.commands:
            if isinstance(i,InsertCommand):
                component_list.append(i.component)
        _app.world.entities.add(self.entity_id,component_list)
        self.commands = []


class Commands:
    def __init__(self):
        self.commands: List[EntityCommands] = []

    def spawn(self, bundle: Union[Bundle, Tuple[Component]]) -> EntityCommands:
        result = EntityCommands()
        self.commands.append(result)
        if isinstance(bundle,Bundle):
            for field in bundle.__class__.__dataclass_fields__:
                value = getattr(bundle, field)
                result.insert(value)
        elif isinstance(Tuple):
            result.insert(Bundle)
        else:
            raise Exception("Bundle or Tuple of Components expected")
        return result

    def apply(self) -> None:
        for i in self.commands:
            i.apply()
        self.commands = []

def get_commands() -> Commands:
    return _app.commands

# ---- Assets ----

class AssetType(str, Enum):
    IMAGE = 'image'
    FONT = 'font'

class AssetServer:
    def load(self, file_name: str, asset_type:AssetType=AssetType.IMAGE,size:int=8) -> int:
        asset = None
        if asset_type == AssetType.IMAGE:
            asset = pygame.image.load(f"assets/{file_name}")
        elif asset_type == AssetType.FONT:
            asset = pygame.font.Font(f"assets/{file_name}",size)
        return get_resource(Assets).add(asset)


@dataclass
class Assets(Resource):
    _assets: List[Surface] = field(default_factory=list)

    def add(self, item: Surface) -> int:
        self._assets.append(item)
        return len(self._assets) - 1

    def get(self, id: int) -> Surface:
        return self._assets[id]

def create_image(color=pygame.Color('white'),
                 size=Vector2(10.0, 10.0)) -> Surface:
    image = pygame.Surface(size)
    image.fill(color)
    return image

# ---- Standard Components ----

@dataclass()
class Camera2dBundle(Bundle):
    camera: Camera
    transform: Transform

@dataclass()
class Camera(Component):
    pass

@dataclass()
class SpriteBundle(Bundle):
    sprite: Sprite
    transform: Transform
    visibility: Visibility


@dataclass()
class Visibility(Component):
    visible: bool


@dataclass()
class Sprite(Component):
    image: int
    # flip_x: bool
    # flip_y: bool
    # custom_size: Vector2
    # rect: Rect
    # anchor: Anchor


@dataclass
class Transform(Component):
    translation: Vector2 = Vector2 (0,0)
    rotation: float = 0
    scale: Vector2 = Vector2(0,0)

@dataclass
class Text2dBundle(Bundle):
    text: Text
    transform: Transform

@dataclass
class Text(Component):
    text: str = ""
    font: int = -1
    font_size: float = 8
    color: Color = None
    _text: str = field(init=False, repr=False, default='<empty>')
    _image:surface = None

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if type(value) is property:
            # initial value not specified, use default
            value = Text._text
        if self._text != value:
            self._update_image(value)
        self._text = value

    def _update_image(self, value:str)->None:
        if self.font > -1:
            self._image = get_resource(Assets).get(self.font).render(value,
                                                                     True,
                                                                     self.color,
                                                                     None)


# ---- Standard Resources ----
@dataclass
class ClearColor(Resource):
    color: Color

@dataclass
class WindowDescriptor(Resource):
    title:str =  "wonderworld"
    width:int = 800
    height:int = 400
    resizable:bool =  True

@dataclass
class Time(Resource):
    delta_seconds: float = 0.0


class Keyboard(Resource):
    def pressed(self,key)->bool:
        keys = pygame.key.get_pressed()

        return keys[key]

# ---- Standard Systems and Plugins
class CorePlugin(Plugin):
    def build(self, app: App):
        app.insert_resource(Time())
        app.insert_resource(Assets())
        app.insert_resource(AssetServer())
        app.insert_resource(Keyboard())
        app.add_system_to_stage(Stage.RENDER,render_core)


class DefaultPlugins(PluginGroup):
    def build(self) -> List[Plugin]:
        return [CorePlugin()]

def render_core():
    camera_transform = None
    for transform, in Query(Transform, With(Camera)):
        camera_transform = transform
        break

    for transform, sprite in Query((Transform, Sprite)):
        _app.screen.blit(get_resource(Assets).get(sprite.image),
                         (transform.translation.x+camera_transform.translation.x,
                          transform.translation.y+camera_transform.translation.y))

    for transform, text in Query((Transform, Text)):
        if text._image is None:
            text._update_image(text._text)
        _app.screen.blit(text._image,
                         (transform.translation.x + camera_transform.translation.x,
                          transform.translation.y + camera_transform.translation.y))


# ---- Standard Funtions ----
def collide_aabb(position_1:Vector2,size_1:Vector2, position_2:Vector2, size_2:Vector2)->bool:
    return Rect(position_1.x, position_1.y, size_1.x, size_1.y).colliderect(Rect(position_2.x,
                                                                                 position_2.y,
                                                                                 size_2.x,
                                                                                 size_2.y))
# ---- Application ----

class Stage(str, Enum):
    PRE_UPDATE = 'pre-update'
    POST_UPDATE = 'post-update'
    LAST = 'last'
    UPDATE = 'update'
    RENDER = 'render'

_app: App = None


class App:
    """
       First: Runs first before startup stage
       Pre-startup: runs before startup
       Startup: runs only once at startup
       Post-startup: after startup
       Pre-update: before update stage
       Update: default stage runs every frame.
       Post-update: after update
       Last: Runs before ende of frame.
       """

    def __init__(self):
        self.world = World()
        self.resources = Resources()
        self.commands = Commands()
        self.screen:Surface = None
        self._schedule: Dict[str:List[Callable]] = {
            "first": [],
            "pre-startup": [],
            "startup": [],
            "post-startup": [],
            "pre-update": [],
            "update": [],
            "post-update": [],
            "last": [],
            Stage.RENDER: []
        }
        global _app
        _app = self

    def run(self):
        once = ["first", "pre-startup", "startup", "post-startup"]
        every_frame = ["pre-update", "update", "post-update", "last"]
        render = ["render"]

        # -- startup
        pygame.init()

        for i in once:
            for j in self._schedule[i]:
                j()
                self.commands.apply()

        running = True

        SIZE = 320, 240
        NAME = 'wonderworld'
        if in_resource(WindowDescriptor):
            descriptor:WindowDescriptor = get_resource(WindowDescriptor)
            SIZE = descriptor.width, descriptor.height
            NAME = descriptor.title
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(NAME)

        clock = pygame.time.Clock()  # create clock object

        FRAMES_PER_SECOND = 30  # who many pictures per second should pygame generate?

        BACKCOLOR = pygame.Color("black")
        if in_resource(ClearColor):
            BACKCOLOR = get_resource(ClearColor).color
        # ---- Game loop ----

        while running:

            # ---- input ----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # ---- update ----
            delta_time = clock.tick(FRAMES_PER_SECOND)  # time since last frame
            get_resource(Time).delta_seconds = delta_time / 1000.0

            for i in every_frame:
                for j in self._schedule[i]:
                    j()
                    self.commands.apply()

            # ---- draw ----
            self.screen.fill(BACKCOLOR)

            for i in render:
                for j in self._schedule[i]:
                    j()

            pygame.display.flip()

        # ---- Quit ----
        pygame.quit()


    def insert_resource(self, resource: Resource) -> App:
        self.resources.add(resource)
        return self

    def add_plugins(self, plugin_group: PluginGroup) -> App:
        for i in plugin_group.build():
            i.build(self)
        return self

    def add_plugin(self, plugin: Plugin) -> App:
        plugin.build(self)
        return self

    def add_startup_system(self, fn: Callable) -> App:
        self._schedule['startup'].append(fn)
        return self

    def add_system(self, fn: Callable) -> App:
        self._schedule['update'].append(fn)
        return self

    def add_system_to_stage(self,stage:Stage, fn: Callable) -> App:
        self._schedule[stage].append(fn)
        return self


# ---- database ----

class World:
    """game database"""

    def __init__(self):
        self.entities = Entities()


class Entities:
    """database of tables - “tables” (or “archetypes”) will store entities component data"""

    def __init__(self):
        self.tables:Dict[FrozenSet[str],Archetype] = {}

    def add(self, id:int, components:List[Component])->None:
        s = set()
        for i in components:
            s.add(type(i))
        table = None
        s = frozenset(s)
        if s in self.tables:
            table = self.tables[s]
        else:
            table = Archetype(components)
            self.tables[s] = table
        table.add(id, components)

class Archetype:
    """table that stores components"""

    def __init__(self,components:List[Component]):
        l = []
        for i in components:
            l.append(i.__class__.__name__)
        self.df = pd.DataFrame(columns = l)

    def add(self,id,components):
        d = {}
        for i in components:
            #d[str(type(i))] = i
            self.df.loc[id,i.__class__.__name__]=i


        #self.df.loc[id] = d

class With:
    def __init__(self,t:Type):
        self.t = t

class Query:
    def __init__(self, column: Union[Tuple[Type], Type], select:Union[Tuple[Type], Type]=None):
        self.column = column
        if not type(self.column) is tuple:
            self.column=(self.column,)
        l = []
        for i in self.column:
            l.append(i.__name__)

        self.column = frozenset(self.column)
        self.column_list = l

        self.select = select
        if not self.select is None:
            if type(self.select)!= Tuple:
                self.select=(self.select,)
            s = set()
            for i in self.select:
                if isinstance(i,With):
                    s.add(i.t)
            self.select = frozenset(s)

    def __iter__(self):
        for key in _app.world.entities.tables.keys():
            if self.column.issubset(key):
                if self.select is None or self.select.issubset(key):
                    x = _app.world.entities.tables[key].df
                    df = x[self.column_list]
                    for index, row in df.iterrows():
                        yield tuple(row)

