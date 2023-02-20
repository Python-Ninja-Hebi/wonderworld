from wonderworld import *

class MyPlugin(Plugin):
    def build(self, app: App):
        app.init_resource(MyOtherResource()) \
        .add_startup_system(plugin_init) \
        .add_system(my_system) \

def plugin_init():
    pass

def my_system():
    pass

if __name__ == "__main__":
    App().add_plugins(DefaultPlugins) \
         .add_plugin(MyPlugin) \
         .run()