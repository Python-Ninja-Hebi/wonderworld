from wonderworld import *

class MyPluginGroup(PluginGroup):
    def build(self) -> List[Plugin]:
        return [FooPlugin(),BarPlugin()]

if __name__ == "__main__":
    App().add_plugins(DefaultPlugins) \
        .add_plugins(MyPluginGroup) \
        .run()