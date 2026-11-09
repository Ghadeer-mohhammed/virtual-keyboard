"""
Virtual Keyboard | كيبورد افتراضي

A virtual keyboard appears with each keystroke and tracks the keys as you type.
The program only colors the keys and plays keyboard sounds; it does not save or send any data.

كيبورد افتراضي يظهر فوق كل النوافذ ويتتبع الأزرار أثناء الكتابة.
البرنامج فقط يلوّن الأزرار ويصدر صوت ضربات الكيبورد، ولا يحفظ ولا يرسل أي بيانات.
"""

import os
import queue
import tkinter.colorchooser as colorchooser

import customtkinter as ctk
import pygame
from pynput import keyboard


# ==================================================
# Setup | الإعدادات الأساسية
# ==================================================

ctk.set_appearance_mode("dark")

# Folder paths are relative to this file, so the project works on any computer
# المسارات نسبية لمكان الملف، عشان المشروع يشتغل عند أي شخص
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Colors | الألوان
NORMAL_COLOR = "#94bdd1"
PRESSED_COLOR = "#285b9e"
TEXT_COLOR = "#ffffff"

# Key size and spacing | حجم الأزرار والمسافات
KEY_WIDTH = 45
KEY_HEIGHT = 44
GAP = 5


# ==================================================
# Sounds | الأصوات
# ==================================================

pygame.mixer.init()

key_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "key_sound.mp3"))
space_enter_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "space_enter.mp3"))


# ==================================================
# Main window | النافذة الرئيسية
# ==================================================

app = ctk.CTk()
app.geometry("750x360")
app.title("Keyboard")
app.attributes("-alpha", 0.85)      # Transparency | الشفافية
app.attributes("-topmost", True)    # Always on top | فوق كل النوافذ
app.overrideredirect(True)          # Remove title bar | إزالة شريط العنوان


# ==================================================
# Keyboard layout | شكل الكيبورد
# Each key is (label, relative width)
# كل زر: (الاسم، العرض النسبي)
# ==================================================

keyboard_layout = [
    # Row 1 | الصف الأول
    [("Esc", 1)] + [(f"F{i}", 1) for i in range(1, 13)],

    # Row 2 | الصف الثاني
    [("`", 1)] + [(str(n), 1) for n in "1234567890"] + [("-", 1), ("=", 1), ("Backspace", 2)],

    # Row 3 | الصف الثالث
    [("Tab", 1.5)] + [(c, 1) for c in "QWERTYUIOP"] + [("[", 1), ("]", 1), ("\\", 1.5)],

    # Row 4 | الصف الرابع
    [("Caps", 1.7)] + [(c, 1) for c in "ASDFGHJKL"] + [(";", 1), ("'", 1), ("Enter", 2)],

    # Row 5 | الصف الخامس
    [("Shift", 2.2)] + [(c, 1) for c in "ZXCVBNM"] + [(",", 1), (".", 1), ("/", 1), ("Shift", 2.2)],

    # Row 6 | الصف السادس
    [("Ctrl", 1.3), ("Win", 1.3), ("Alt", 1.3), ("Space", 6), ("Alt", 1.3), ("Ctrl", 1.3)],
]

# Arabic letters shown under each key (standard Arabic 101 layout)
# الحروف العربية اللي تظهر تحت كل زر (التوزيع العربي القياسي)
ARABIC_LABELS = {
    "`": "ذ",
    "Q": "ض", "W": "ص", "E": "ث", "R": "ق", "T": "ف",
    "Y": "غ", "U": "ع", "I": "ه", "O": "خ", "P": "ح",
    "[": "ج", "]": "د",
    "A": "ش", "S": "س", "D": "ي", "F": "ب", "G": "ل",
    "H": "ا", "J": "ت", "K": "ن", "L": "م", ";": "ك", "'": "ط",
    "Z": "ئ", "X": "ء", "C": "ؤ", "V": "ر", "B": "لا",
    "N": "ى", "M": "ة", ",": "و", ".": "ز", "/": "ظ",
}

# Each key name maps to a list of buttons, because some keys appear twice (Shift, Ctrl, Alt)
# كل اسم مفتاح له قائمة أزرار، لأن بعض المفاتيح مكررة مثل Shift و Ctrl و Alt
buttons = {}

# pynput runs in a separate thread, but Tkinter must be updated from its own thread,
# so we pass key events through a queue
# pynput يشتغل في Thread مختلف، و Tkinter لازم يتحدث من Thread الخاص به، فنستخدم Queue
key_queue = queue.Queue()


# ==================================================
# Key conversion | تحويل المفاتيح
# Uses Windows virtual key codes, so it works with any keyboard language (Arabic/English)
# يعتمد على المفتاح الفيزيائي، فيشتغل مع الكيبورد العربي والإنجليزي
# ==================================================

SYMBOL_VK = {
    192: "`", 189: "-", 187: "=", 219: "[", 221: "]", 220: "\\",
    186: ";", 222: "'", 188: ",", 190: ".", 191: "/",
}

SPECIAL_KEYS = {
    keyboard.Key.space: "Space",
    keyboard.Key.enter: "Enter",
    keyboard.Key.backspace: "Backspace",
    keyboard.Key.tab: "Tab",
    keyboard.Key.caps_lock: "Caps",
    keyboard.Key.shift: "Shift",
    keyboard.Key.shift_l: "Shift",
    keyboard.Key.shift_r: "Shift",
    keyboard.Key.ctrl: "Ctrl",
    keyboard.Key.ctrl_l: "Ctrl",
    keyboard.Key.ctrl_r: "Ctrl",
    keyboard.Key.alt: "Alt",
    keyboard.Key.alt_l: "Alt",
    keyboard.Key.alt_r: "Alt",
    keyboard.Key.cmd: "Win",
    keyboard.Key.cmd_l: "Win",
    keyboard.Key.cmd_r: "Win",
    keyboard.Key.esc: "Esc",
}


def convert_pynput_key(key):
    """Convert a pynput key to the label used on our keyboard (or None).
    تحويل مفتاح pynput إلى الاسم المستخدم في الكيبورد (أو None)."""

    # Normal keys | المفاتيح العادية
    if isinstance(key, keyboard.KeyCode):
        vk = key.vk

        if vk is None:
            return None

        # Letters A-Z (65-90) and digits 0-9 (48-57) match their ASCII codes
        # الحروف والأرقام أكوادها نفس كود ASCII
        if 65 <= vk <= 90 or 48 <= vk <= 57:
            return chr(vk)

        return SYMBOL_VK.get(vk)

    # Special keys | المفاتيح الخاصة
    if key in SPECIAL_KEYS:
        return SPECIAL_KEYS[key]

    # F1 - F12
    name = getattr(key, "name", "") or ""
    if name.startswith("f") and name[1:].isdigit() and 1 <= int(name[1:]) <= 12:
        return name.upper()

    return None


# ==================================================
# Global keyboard listener | الاستماع للكيبورد
# ==================================================

# When False, the app ignores all keystrokes (used for passwords or private typing)
# لما تكون False، البرنامج يتجاهل كل الضغطات (للباسوردات أو الكتابة الخاصة)
tracking_enabled = True


def global_key_pressed(key):
    if not tracking_enabled:
        return
    try:
        converted = convert_pynput_key(key)
        if converted:
            key_queue.put(("press", converted))
    except Exception:
        pass


def global_key_released(key):
    if not tracking_enabled:
        return
    try:
        converted = convert_pynput_key(key)
        if converted:
            key_queue.put(("release", converted))
    except Exception:
        pass


keyboard_listener = keyboard.Listener(
    on_press=global_key_pressed,
    on_release=global_key_released,
)
keyboard_listener.start()


# ==================================================
# Key highlighting | تلوين الأزرار
# ==================================================

def set_key_color(key, color):
    """Change the color of every button with this key name.
    تغيير لون كل الأزرار اللي تحمل نفس اسم المفتاح."""
    for button in buttons.get(key, []):
        button.configure(fg_color=color)


def update_all_buttons(**options):
    """Apply the same settings to all buttons.
    تطبيق نفس الإعدادات على كل الأزرار."""
    for button_list in buttons.values():
        for button in button_list:
            button.configure(**options)


def process_keyboard_queue():
    """Read key events from the queue and update the UI every 10 ms.
    قراءة أحداث الكيبورد من الـ Queue وتحديث الواجهة كل 10 مللي ثانية."""
    try:
        while True:
            action, key = key_queue.get_nowait()

            if action == "press":
                # Sound | الصوت
                if key in ("Space", "Enter"):
                    space_enter_sound.play()
                else:
                    key_sound.play()

                # Highlight | التظليل
                set_key_color(key, PRESSED_COLOR)

            elif action == "release":
                set_key_color(key, NORMAL_COLOR)

    except queue.Empty:
        pass

    app.after(10, process_keyboard_queue)


# ==================================================
# Color settings | إعدادات الألوان
# ==================================================

def change_normal_color():
    global NORMAL_COLOR
    color = colorchooser.askcolor(title="اختر لون الأزرار")[1]
    if color:
        NORMAL_COLOR = color
        update_all_buttons(fg_color=NORMAL_COLOR)


def change_pressed_color():
    global PRESSED_COLOR
    color = colorchooser.askcolor(title="اختر لون الضغط")[1]
    if color:
        PRESSED_COLOR = color


def change_text_color():
    global TEXT_COLOR
    color = colorchooser.askcolor(title="اختر لون الكتابة")[1]
    if color:
        TEXT_COLOR = color
        update_all_buttons(text_color=TEXT_COLOR)


def open_settings():
    """Settings window | نافذة الإعدادات"""
    settings = ctk.CTkToplevel(app)
    settings.title("Keyboard Settings")
    settings.geometry("300x280")
    settings.resizable(False, False)
    settings.attributes("-topmost", True)

    ctk.CTkLabel(
        settings,
        text="Keyboard Settings",
        font=("Arial", 18, "bold"),
    ).pack(pady=(20, 15))

    ctk.CTkButton(settings, text="Button color", command=change_normal_color).pack(pady=7)
    ctk.CTkButton(settings, text="Click color", command=change_pressed_color).pack(pady=7)
    ctk.CTkButton(settings, text="Text color", command=change_text_color).pack(pady=7)


# ==================================================
# Build the keyboard | بناء أزرار الكيبورد
# ==================================================

keyboard_frame = ctk.CTkFrame(app, fg_color="transparent")
keyboard_frame.pack(expand=True, fill="both", padx=10, pady=(45, 10))

for row in keyboard_layout:
    row_frame = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
    row_frame.pack(pady=3)

    for key_name, width in row:
        # English on top, Arabic below | الإنجليزي فوق والعربي تحته
        arabic = ARABIC_LABELS.get(key_name)
        label = f"{key_name}\n{arabic}" if arabic else key_name

        button = ctk.CTkButton(
            row_frame,
            text=label,
            width=int(KEY_WIDTH * width),
            height=KEY_HEIGHT,
            corner_radius=7,
            fg_color=NORMAL_COLOR,
            hover=False,
            text_color=TEXT_COLOR,
            font=("Arial", 11 if arabic else 12, "bold"),
        )
        button.pack(side="left", padx=GAP / 2)

        buttons.setdefault(key_name, []).append(button)


# ==================================================
# Window controls | أزرار التحكم بالنافذة
# ==================================================

is_maximized = False
normal_geometry = "750x360"


def toggle_maximize():
    """Maximize / restore the window | تكبير واستعادة النافذة"""
    global is_maximized, normal_geometry

    if not is_maximized:
        # Save current size and position | حفظ الحجم والمكان الحالي
        normal_geometry = (
            f"{app.winfo_width()}x{app.winfo_height()}"
            f"+{app.winfo_x()}+{app.winfo_y()}"
        )
        app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")
        is_maximized = True
        maximize_button.configure(text="❐")
    else:
        app.geometry(normal_geometry)
        is_maximized = False
        maximize_button.configure(text="□")


def close_app():
    """Stop the listener and close the app | إيقاف الاستماع وإغلاق البرنامج"""
    try:
        keyboard_listener.stop()
    except Exception:
        pass
    app.destroy()


STOP_COLOR, STOP_HOVER = "#C0392B", "#E74C3C"        # red | أحمر
RESUME_COLOR, RESUME_HOVER = "#2E7D32", "#43A047"    # green | أخضر


def toggle_tracking():
    """Pause / resume key tracking | إيقاف / استئناف التتبع"""
    global tracking_enabled
    tracking_enabled = not tracking_enabled

    if tracking_enabled:
        stop_button.configure(
            text="Stop | إيقاف", fg_color=STOP_COLOR, hover_color=STOP_HOVER
        )
    else:
        # Clear any highlighted keys so none stay stuck while paused
        # إرجاع كل الأزرار للون العادي عشان ما يعلق زر ملوّن أثناء الإيقاف
        update_all_buttons(fg_color=NORMAL_COLOR)
        stop_button.configure(
            text="Resume | استئناف", fg_color=RESUME_COLOR, hover_color=RESUME_HOVER
        )


stop_button = ctk.CTkButton(
    app, text="Stop | إيقاف", width=110, height=26, corner_radius=8,
    font=("Arial", 11, "bold"),
    fg_color=STOP_COLOR, hover_color=STOP_HOVER, command=toggle_tracking
)

settings_button = ctk.CTkButton(
    app, text="⚙", width=35, height=30, corner_radius=8, command=open_settings
)

minimize_button = ctk.CTkButton(
    app, text="—", width=35, height=30, corner_radius=8, command=app.iconify
)

maximize_button = ctk.CTkButton(
    app, text="□", width=35, height=30, corner_radius=8, command=toggle_maximize
)

close_button = ctk.CTkButton(
    app, text="✕", width=35, height=30, corner_radius=8,
    fg_color="#8B3A3A", hover_color="#B84A4A", command=close_app
)


def show_controls(event=None):
    """Show control buttons when the mouse enters the window.
    إظهار أزرار التحكم عند دخول الماوس للنافذة."""
    settings_button.place(x=10, y=8)
    stop_button.place(relx=0.5, y=10, anchor="n")
    minimize_button.place(relx=1.0, x=-125, y=8, anchor="ne")
    maximize_button.place(relx=1.0, x=-85, y=8, anchor="ne")
    close_button.place(relx=1.0, x=-45, y=8, anchor="ne")


def hide_controls(event=None):
    """Hide control buttons when the mouse leaves the window.
    إخفاء أزرار التحكم عند خروج الماوس."""
    settings_button.place_forget()
    # Keep the button visible while paused, so you never forget tracking is off
    # أبقي الزر ظاهر أثناء الإيقاف عشان ما تنسين إن التتبع متوقف
    if tracking_enabled:
        stop_button.place_forget()
    minimize_button.place_forget()
    maximize_button.place_forget()
    close_button.place_forget()


# ==================================================
# Dragging the window | تحريك النافذة بالماوس
# ==================================================

drag_x = 0
drag_y = 0


def start_move(event):
    global drag_x, drag_y
    drag_x = event.x
    drag_y = event.y


def move_window(event):
    x = app.winfo_x() + event.x - drag_x
    y = app.winfo_y() + event.y - drag_y
    app.geometry(f"+{x}+{y}")


app.bind("<Button-1>", start_move)
app.bind("<B1-Motion>", move_window)
app.bind("<Enter>", show_controls)
app.bind("<Leave>", hide_controls)

# Hide controls at startup | إخفاء الأزرار عند البداية
hide_controls()


# ==================================================
# Run | تشغيل البرنامج
# ==================================================

app.after(10, process_keyboard_queue)
app.mainloop()