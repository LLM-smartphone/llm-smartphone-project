from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.uiautomator import uiautomatorhelper
import cv2
import numpy as np
import random
import time
from enum import Enum

# start emulator: 
# /Users/luyuan/Library/Android/sdk/emulator/emulator @Pixel_3a_API_34_extension_level_7_arm64-v8a
# start adb:
# adb -e shell

class DeviceManager:
    class ScrollDirection(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    def __init__(self) -> None:
        device, serialno = ViewClient.connectToDeviceOrExit()
        #TODO: ideally we should use https://github.com/dtmilano/CulebraTester2-public
        # as the backend. UIAutomator has a drawback of cannot dump video / animatiion.
        # However, using CulebraTester2, there are too many views showing, we 
        # need to develop a smart filtering algorithm
        self.vc = ViewClient(device, serialno, useuiautomatorhelper=False, autodump=False)
        self.display_info = self.vc.device.getDisplayInfo()

    def go_home(self):
        self.vc.device.press("HOME")
        
    def go_back(self):
        self.vc.device.press("BACK")

    def enter(self):
        self.vc.device.press("ENTER")

    def get_screenshot(self):
        return self.vc.device.takeSnapshot(reconnect=True)
    
    def click_ui(self, id, ui_list):
        ele = ui_list[id]
        ele.touch()
    
    def long_press_ui(self, id, ui_list):
        ele = ui_list[id]
        ele.longTouch(duration=2000)

    def type_to(self, id, str, ui_list):
        ele = ui_list[id]
        ele.type(str)

    def scroll(self, direction):
        w = self.display_info['width']
        h = self.display_info['height']
        if direction == DeviceManager.ScrollDirection.DOWN:
            # show content at bottom, aka from scroll bottom to top
            start_x = w // 2
            start_y = h // 3 * 2
            end_x = w // 2
            end_y = h // 3
        elif direction == DeviceManager.ScrollDirection.UP:
            start_x = w // 2
            start_y = h // 3
            end_x = w // 2
            end_y = h // 3 * 2
        elif direction == DeviceManager.ScrollDirection.LEFT:
            # show content at left
            start_x = w // 4
            start_y = h // 2
            end_x = w // 4 * 3
            end_y = h // 2
        elif direction == DeviceManager.ScrollDirection.RIGHT:
            start_x = w // 4 * 3
            start_y = h // 2
            end_x = w // 4
            end_y = h // 2
        self.vc.swipe(start_x, start_y, end_x, end_y)

    def sleep(self, seconds=2):
        time.sleep(seconds)
    
    def annotate_ui(self):
        max_retry = 20
        dump_succeed = False
        for i in range(0, max_retry):
            try:
                self.vc.dump() # force refetch current ui state
                dump_succeed = True
                break
            except:
                continue # retry
        if not dump_succeed:
            raise RuntimeError(f"Dump failed after {max_retry} times")
        elements_dict = self.vc.getViewsById()
        ui_list = []
        for k in elements_dict:
            ele = elements_dict[k]

            (x, y), (x2, y2) = ele.map['bounds']
            w = x2 - x
            h = y2 - y

            if w == self.display_info['width'] and h == self.display_info['height']:
                continue # skip the top level view

            if ele.map['clickable'] == 'false' and self._is_inside_other_view(elements_dict, k):
                # skip non clickable views, unless it's not inside any other view
                # that is saying, if a textview is not clickable, we still need to keep it if
                # no other view contains it
                continue 
        
            # if ele.getVisibility() != 0:
            #     print(ele.getVisibility())
            #     continue
        
            ui_list.append(ele)
        return ui_list
    
    def save_annotated_screenshot(self, ui_list=None, filename='./screenshot.jpg', size=(512, 1024)):
        if ui_list is None:
            ui_list = self.annotate_ui()
        img = self.get_annotated_screenshot(ui_list)
        if size is not None:
            img = cv2.resize(img, size)
        cv2.imwrite(filename, img)
        return filename

    def get_annotated_screenshot(self, ui_list):
        img = self.get_screenshot()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        

        for i, ele in enumerate(ui_list):
            (x, y), (x2, y2) = ele.map['bounds']
            w = x2 - x
            h = y2 - y

            # shrink the box a little bit
            y -= 3
            h -= 6 

            color = self._generate_random_color()
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 4)

            # draw id text
            id_x = x
            id_y = y

            id_width = 35
            if i > 9:
                id_width = 50
            cv2.rectangle(img, (id_x, id_y), (id_x + id_width, id_y + 40), color, cv2.FILLED)
            cv2.putText(img, str(i), (id_x + 0, id_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        
        return img

    def _generate_random_color(self):
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            if r + g + b < 400: # avoid light colors
                return r, g, b
            
    def _is_inside_other_view(self, ui_dict, view_k):
        # check if view_k is inside another view in ui_dict
        view_top_left, view_bottom_right = ui_dict[view_k].map['bounds']
        for k in ui_dict:
            if k == view_k:
                continue # don't check self
            top_left, bottom_right = ui_dict[k].map['bounds']
            if view_top_left[0] > top_left[0] and view_top_left[1] > top_left[1] and view_bottom_right[0] < bottom_right[0] and view_bottom_right[1] < bottom_right[1]:
                return True
        return False
