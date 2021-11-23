import string
import time
import numpy as np
import pyautogui
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT, RECT

pyautogui.FAILSAFE = False
handle = windll.user32.FindWindowW(None, "Counter-Strike")

PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA

SetWindowPos = windll.user32.SetWindowPos
GetClientRect = windll.user32.GetClientRect
GetWindowRect = windll.user32.GetWindowRect
GetCursorPos = windll.user32.GetCursorPos
EnableWindow = windll.user32.EnableWindow

ClientToScreen = windll.user32.ClientToScreen

WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120

SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0X0002
SWP_NOZORDER = 0x0004

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101

# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VkCode = {
    "back": 0x08,
    "tab": 0x09,
    "return": 0x0D,
    "shift": 0x10,
    "control": 0x11,
    "menu": 0x12,
    "pause": 0x13,
    "capital": 0x14,
    "escape": 0x1B,
    "space": 0x20,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "print": 0x2A,
    "snapshot": 0x2C,
    "insert": 0x2D,
    "delete": 0x2E,
    "lwin": 0x5B,
    "rwin": 0x5C,
    "numpad0": 0x60,
    "numpad1": 0x61,
    "numpad2": 0x62,
    "numpad3": 0x63,
    "numpad4": 0x64,
    "numpad5": 0x65,
    "numpad6": 0x66,
    "numpad7": 0x67,
    "numpad8": 0x68,
    "numpad9": 0x69,
    "multiply": 0x6A,
    "add": 0x6B,
    "separator": 0x6C,
    "subtract": 0x6D,
    "decimal": 0x6E,
    "divide": 0x6F,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "numlock": 0x90,
    "scroll": 0x91,
    "lshift": 0xA0,
    "rshift": 0xA1,
    "lcontrol": 0xA2,
    "rcontrol": 0xA3,
    "lmenu": 0xA4,
    "rmenu": 0XA5
}


def move_to(handle: HWND, x: int, y: int):
    """移动鼠标到坐标（x, y)

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
    wparam = 0
    lparam = y << 16 | x
    PostMessageW(handle, WM_MOUSEMOVE, wparam, lparam)


def left_down(handle: HWND, x: int, y: int):
    """在坐标(x, y)按下鼠标左键

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
    wparam = 0
    lparam = y << 16 | x
    PostMessageW(handle, WM_LBUTTONDOWN, wparam, lparam)


def left_up(handle: HWND, x: int, y: int):
    """在坐标(x, y)放开鼠标左键

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
    wparam = 0
    lparam = y << 16 | x
    PostMessageW(handle, WM_LBUTTONUP, wparam, lparam)


def scroll(handle: HWND, delta: int, x: int, y: int):
    """在坐标(x, y)滚动鼠标滚轮

    Args:
        handle (HWND): 窗口句柄
        delta (int): 为正向上滚动，为负向下滚动
        x (int): 横坐标
        y (int): 纵坐标
    """
    move_to(handle, x, y)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
    wparam = delta << 16
    p = POINT(x, y)
    ClientToScreen(handle, byref(p))
    lparam = p.y << 16 | p.x
    PostMessageW(handle, WM_MOUSEWHEEL, wparam, lparam)


def scroll_up(handle: HWND, x: int, y: int):
    """在坐标(x, y)向上滚动鼠标滚轮

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    scroll(handle, WHEEL_DELTA, x, y)


def scroll_down(handle: HWND, x: int, y: int):
    """在坐标(x, y)向下滚动鼠标滚轮

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    scroll(handle, -WHEEL_DELTA, x, y)


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]


def key_down(handle: HWND, key: str):
    """按下指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)


def key_up(handle: HWND, key: str):
    """放开指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
    wparam = vk_code
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)


def key_click(handle: HWND, key: str):
    key_down(handle, key)
    time.sleep(.2)
    key_up(handle, key)


def move_window(handle: HWND, x: int, y: int):
    """移动窗口到坐标(x, y)

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    SetWindowPos(handle, 0, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER)


def resize_window(handle: HWND, width: int, height: int):
    """设置窗口大小为width × height

    Args:
        handle (HWND): 窗口句柄
        width (int): 宽
        height (int): 高
    """
    SetWindowPos(handle, 0, 0, 0, width, height, SWP_NOMOVE | SWP_NOZORDER)


def resize_client(handle: HWND, width: int, height: int):
    """设置客户区大小为width × height

    Args:
        handle (HWND): 窗口句柄
        width (int): 宽
        height (int): 高
    """
    client_rect = RECT()
    GetClientRect(handle, byref(client_rect))
    delta_w = width - client_rect.right
    delta_h = height - client_rect.bottom
    window_rect = RECT()
    GetWindowRect(handle, byref(window_rect))
    current_width = window_rect.right - window_rect.left
    current_height = window_rect.bottom - window_rect.top
    resize_window(handle, current_width + delta_w, current_height + delta_h)


def lock_window(handle: HWND):
    """锁定窗口

    Args:
        handle (HWND): 窗口句柄
    """
    EnableWindow(handle, 0)


def unlock_window(handle: HWND):
    """解锁窗口

    Args:
        handle (HWND): 窗口句柄
    """
    EnableWindow(handle, 1)


def get_mouse_point():
    """获得当前鼠标的绝对坐标

    """
    po = POINT()
    GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def shoot(boxes):
    """开枪

        Args:
            :param boxes: 标注的方框
    """
    # 获取当前鼠标的绝对坐标
    po = get_mouse_point()
    window_rect = RECT()
    GetWindowRect(handle, byref(window_rect))

    # 获得窗口内的相对坐标
    mouse_x = po[0] - window_rect.left
    mouse_y = po[1] - window_rect.top
    print('当前坐标：', mouse_x, ',', mouse_y)

    boxes = np.array(boxes)
    # 找离相对坐标最近的box
    x = 0.5 * boxes[:, 0] + 0.5 * boxes[:, 2]
    x = x - mouse_x
    y = 0.6 * boxes[:, 1] + 0.4 * boxes[:, 3]  # 具体0.4、0.6的关系看情况，打头还是哪儿
    y = y - mouse_y

    index = np.argmin(np.sqrt(x ** 2 + y ** 2), 0)  # 找x轴最近的目标

    x = int(x[index])
    y = int(y[index])

    # 自己实测的数据：游戏中移动像素数=moveRel输入 / 1.56
    rel_x = x * 1.56
    rel_y = y * 1.56
    print('偏移坐标：', rel_x, ',', rel_y)

    time.sleep(0.2)
    pyautogui.moveRel(rel_x, rel_y)  # 这两步占用一半时间（各0.1s)
    time.sleep(0.2)
    pyautogui.click()  # 开几枪也是自己改
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.2)

    # 返回窗口内的射击坐标
    x = round(((boxes[index][0] + boxes[index][2]) / 2).item())
    y = round((0.6 * boxes[index][1] + 0.4 * boxes[index][3]).item())
    f = round(boxes[index][4], 2)
    return x, y, f


if __name__ == "__main__":
    print(get_mouse_point())
