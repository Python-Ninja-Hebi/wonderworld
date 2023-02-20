from wonderworld import *

@dataclass
class Component1(Component):
    pass

@dataclass
class Component2(Component):
    value:int

@dataclass
class Label(Component):
    value:str

@dataclass
class Strength(Component):
    value:int

@dataclass
class Agility(Component):
    value:int

@dataclass
class ExampleBundle(Bundle):
    a: Component1
    b: Component2


def example_system():
    commands = Commands()
    #Create a new entity with a single component.
    commands.spawn(Component1)

    #Create a new entity with a component bundle.
    commands.spawn(ExampleBundle(
        a = Component1(),
        b = Component2(value=2)
    ))

    commands \
        .spawn((Component1, Component2)) \
        .insert((Strength(1), Agility(2))) \
        .insert(Label("hello world"))

if __name__ == "__main__":
    App().add_plugins(DefaultPlugins())\
        .add_startup_system(example_system)\
        .run()