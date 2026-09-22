import os
import sys
import ctypes
import subprocess
import tkinter as tk
import keyboard  # pip install keyboard

# ============ Закрытие браузеров ============
def kill_browsers():
    for proc in ("msedge.exe", "chrome.exe"):
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", proc, "/T"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception:
            pass

# ============ Блокировка клавиш через keyboard ============
def block_keys():
    # Win (левая и правая)
    keyboard.block_key("left windows")
    keyboard.block_key("right windows")

    # Ctrl+Esc — блокируем Esc, когда зажат Ctrl
    def block_ctrl_esc(e):
        if keyboard.is_pressed("ctrl"):
            return False  # False = проглатываем событие
    keyboard.hook_key("esc", block_ctrl_esc, suppress=True)

    # Ctrl+Shift+Esc — на всякий случай тоже (тот же хук выше покрывает)
    # Дополнительно можно повесить хук на 'ctrl+shift+esc' — но hook_key('esc')
    # уже ловит любое нажатие Esc, включая с зажатыми Ctrl и Shift.

# ============ Полноэкранное окно ============
def create_overlay():
    root = tk.Tk()
    root.title("Блокировка")
    root.configure(bg="black")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)  # убираем рамку и крестик

    label = tk.Label(
        root,
        text="ПК ПОД БЛОКИРОВКОЙ",
        fg="red",
        bg="black",
        font=("Arial", 72, "bold"),
    )
    label.pack(expand=True)

    sub = tk.Label(
        root,
        text="Нажмите Alt+F4 для выхода",
        fg="red",
        bg="black",
        font=("Arial", 24),
    )
    sub.pack(expand=True)

    # Держим окно поверх всех окон
    def keep_on_top():
        try:
            root.attributes("-topmost", True)
            root.lift()
        except Exception:
            pass
        root.after(500, keep_on_top)

    keep_on_top()

    try:
        root.mainloop()
    finally:
        # Снимаем блокировки при выходе
        try:
            keyboard.unblock_key("left windows")
            keyboard.unblock_key("right windows")
            keyboard.unhook_all()
        except Exception:
            pass

# ============ Точка входа ============
if __name__ == "__main__":
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1
        )
        sys.exit(0)

    kill_browsers()
    block_keys()
    create_overlay()