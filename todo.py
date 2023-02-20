import sys

def todo(text:str='')->None:
    frame = sys._getframe(1)
    class_name = ""
    try:
        self_obj = frame.f_locals['self']
        class_name = type(self_obj).__name__ + '.'
    except KeyError:
        pass
    print(f'todo {class_name}{frame.f_code.co_name} {text}')