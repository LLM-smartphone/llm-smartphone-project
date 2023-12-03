from device_manager import DeviceManager
from actions import ActionManager
from prompts import HistoryPrompt
from llm_utils import LLMUtils
import signal
import sys
import shutil
from pathlib import Path
import os

def handler(signal_num, frame):
    global step_count
    print(f"SIGINT signal captured. Step count: {step_count}")
    sys.exit(1)

step_count = 0
signal.signal(signal.SIGINT, handler)

output_path = "./outputs"
Path(output_path).mkdir(parents=True, exist_ok=True)

device_manager = DeviceManager()
action_manager = ActionManager(device_manager=device_manager)
action_prompt = action_manager.build_action_prompt()
llm = LLMUtils()

task_prompt = "Open settings and check battery usage"

prompt_helper = HistoryPrompt(task_prompt, action_prompt)

# go to home screen and prepare the task
# device_manager.go_home()
# device_manager.sleep()

while not action_manager.finished:
    print("*" * 60)
    ui_list = device_manager.annotate_ui()
    prompt = prompt_helper.generate_prompt_with_history(ui_list)
    print("========== prompt ==========")
    print(prompt)
    screenshot_name = device_manager.save_annotated_screenshot(ui_list)
    shutil.copyfile(screenshot_name, os.path.join(output_path, f"{step_count}.jpg"))
    response = llm.chat_with_image(prompt, screenshot_name)
    prompt_helper.append_response(response)
    print("========== response ==========")
    print(response)
    code_list = llm.extract_python_code(response)
    print("========== code ==========")
    print(code_list)
    for code in code_list:
        action_manager.execute_action(code, ui_list)
        device_manager.sleep()
        step_count += 1

# Subtract done() action from step count
print(f"Job finished. Step count: {step_count - 1}")