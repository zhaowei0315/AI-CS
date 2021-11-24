
import pyautogui
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT, RECT
import pywintypes
import win32gui, win32con, win32api, win32ui

pyautogui.FAILSAFE = False

def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)

def get_hwnd(name: str):
    return windll.user32.FindWindowW(None, name)

def set_focus(hwnd: HWND):
    win32api.SendMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)

def click_point(x: int, y: int, hwnd: HWND):
    print('Click:', x, y)
    set_focus(hwnd)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, ((y) << 16 | (x)))
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, ((y) << 16 | (x)))

def send_enter(hwnd: HWND):
       win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, 13, 0)
       win32api.SendMessage(hwnd, win32con.WM_KEYUP, 13, 0)

def send_str(text: str, hwnd: HWND):
    astrToint = [ord(c) for c in text]
    for item in astrToint:
        win32api.PostMessage(hwnd, win32con.WM_CHAR, item, 0)

def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)

def shoot(boxes):
    # 获取当前鼠标的绝对坐标
    po = get_mouse_point()
    window_rect = RECT()
    windll.user32.GetWindowRect(handle, byref(window_rect))

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
    list_window_names()
    
    hwnd = get_hwnd('eclipse_workspace - AI-CS/KeyMouse.py - Eclipse IDE')
    print(hwnd)
    set_focus(hwnd)
    click_point(165, 70, hwnd)
    
    send_str('Test Test', hwnd)
    
    win32api.SetCursorPos((165, 70))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,165, 70,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,165, 70,0,0)