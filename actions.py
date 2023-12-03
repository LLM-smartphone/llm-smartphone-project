from device_manager import DeviceManager
import copy

def make_action(desc):
    def inner(func):
        func.action_desc = desc
        return func
    return inner

@make_action("`click(id)`, click an UI element with the id number")
def click(id):
    ui_list = ActionManager.shared.ui_list
    ActionManager.shared.device_manager.click_ui(id, ui_list)

@make_action("`long_press(id)`, long press an UI element with the id number to reveal additional options or actions related to the UI element being pressed, if available")
def long_press(id):
    ui_list = ActionManager.shared.ui_list
    ActionManager.shared.device_manager.long_press_ui(id, ui_list)

@make_action("`scroll_down()`, scroll to show more content from bottom")
def scroll_down():
    ActionManager.shared.device_manager.scroll(DeviceManager.ScrollDirection.DOWN)

@make_action("`scroll_up()`, scroll to show more content from top")
def scroll_up():
    ActionManager.shared.device_manager.scroll(DeviceManager.ScrollDirection.UP)

@make_action("`scroll_left()`, scroll to show more content from left")
def scroll_left():
    ActionManager.shared.device_manager.scroll(DeviceManager.ScrollDirection.LEFT)

@make_action("`scroll_right()`, scroll to show more content from right")
def scroll_right():
    ActionManager.shared.device_manager.scroll(DeviceManager.ScrollDirection.RIGHT)

@make_action("`home()`, press home button and go to the home screen")
def home():
    ActionManager.shared.device_manager.go_home()

@make_action("`back()`, press the back button and go to the previous page")
def back():
    ActionManager.shared.device_manager.go_back()

@make_action("`enter()`, press the enter button on keyboard")
def enter():
    ActionManager.shared.device_manager.enter()

@make_action("`type_to(id, str)`, type string `str` to UI element with the id number")
def type_to(id, str):
    ui_list = ActionManager.shared.ui_list
    ActionManager.shared.device_manager.type_to(id, str, ui_list)

@make_action("`wait()`, wait for a while, for example, wait for loading")
def wait():
    ActionManager.shared.device_manager.sleep(5)

@make_action("`done()`, indicate your task is finished, no more actions required")
def done():
    ActionManager.shared.done()

class ActionManager:
    shared = None
    def __init__(self, device_manager: DeviceManager) -> None:
        self.device_manager = device_manager
        self.ui_list = None
        self.finished = False
        if ActionManager.shared is None:
            ActionManager.shared = self
        else:
            raise RuntimeError("Use shared to access ActionManager")
    
    def build_action_prompt(self):
        prompt = ''
        global_variables = copy.copy(globals())
        for k in global_variables:
            each = global_variables[k]
            if callable(each) and hasattr(each, "action_desc"):
                prompt += each.action_desc + '; '
        return prompt

    def execute_action(self, python_code, ui_list=None):
        self.ui_list = ui_list
        exec(python_code)

    def done(self):
        self.finished = True