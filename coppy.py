import tkinter as tk
from tkinter import ttk, messagebox
import os

# Try to import PIL for better image support (JPG, resizing, etc.)
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: PIL/Pillow not found. JPG images may not work.")

# ------------------ Configuration & Styles ------------------
COLORS = {
    "bg": "#121212",        # Very dark grey (almost black)
    "card_bg": "#1E1E1E",   # Dark grey for cards/containers
    "primary": "#BB86FC",   # Light Purple accent
    "primary_dark": "#3700B3", # Darker Purple
    "text": "#FFFFFF",      # White text
    "text_sec": "#B0B0B0",  # Secondary text (light grey)
    "error": "#CF6679",     # Error red
    "input_bg": "#2C2C2C",  # Input field background
    "input_fg": "#FFFFFF"   # Input field text
}

FONTS = {
    "h1": ("Segoe UI", 24, "bold"),
    "h2": ("Segoe UI", 18, "bold"),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10)
}

# ------------------ Database Import ------------------
import database as db

# Global variable for current logged-in teacher
current_teacher_id = None
current_teacher_data = None

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Combobox style
    style.configure("TCombobox",
                    fieldbackground=COLORS["input_bg"],
                    background=COLORS["card_bg"],
                    foreground=COLORS["input_fg"],
                    arrowcolor=COLORS["primary"],
                    bordercolor=COLORS["card_bg"],
                    lightcolor=COLORS["card_bg"],
                    darkcolor=COLORS["card_bg"])
    style.map("TCombobox", fieldbackground=[("readonly", COLORS["input_bg"])])

# ------------------ หน้า Schedule Search (สำหรับนักศึกษา) ------------------
def open_schedule_page_student(login_root, student_data):
    schedule = tk.Toplevel()
    schedule.title("Schedule Search")
    schedule.geometry("400x750")
    schedule.config(bg=COLORS["bg"])

    # Main Container
    main_container = tk.Frame(schedule, bg=COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Header
    header_frame = tk.Frame(main_container, bg=COLORS["bg"])
    header_frame.pack(fill="x", pady=(0, 20))
    
    title = tk.Label(header_frame, text="TeachMap", font=FONTS["h1"], bg=COLORS["bg"], fg=COLORS["primary"])
    title.pack(side="left")
    
    # Logout Button
    def logout():
        schedule.destroy()
        login_root.deiconify()
    
    logout_btn = tk.Button(
        header_frame, text="ออกจากระบบ", font=FONTS["body"],
        bg=COLORS["error"], fg=COLORS["text"], bd=0, cursor="hand2",
        activebackground="#B00020", activeforeground="white",
        command=logout, padx=15, pady=5
    )
    logout_btn.pack(side="right")
    
    # Dashboard Button
    def open_dashboard():
        from student_pages import open_student_dashboard
        open_student_dashboard(login_root, student_data)
    
    dashboard_btn = tk.Button(
        header_frame, text="Dashboard", font=FONTS["body"],
        bg=COLORS["primary"], fg=COLORS["bg"], bd=0, cursor="hand2",
        activebackground=COLORS["primary_dark"], activeforeground="white",
        command=open_dashboard, padx=15, pady=5
    )
    dashboard_btn.pack(side="right", padx=(0, 10))

    # ---------------- ช่องค้นหา ----------------
    search_frame = tk.Frame(main_container, bg=COLORS["card_bg"], bd=0, highlightthickness=1, highlightbackground=COLORS["input_bg"])
    search_frame.pack(fill="x", pady=(0, 15), ipady=5)

    search_entry = tk.Entry(search_frame, font=FONTS["body"], bd=0, bg=COLORS["card_bg"], fg=COLORS["text_sec"], insertbackground=COLORS["primary"])
    search_entry.insert(0, "Search by...")
    
    def on_entry_click(event):
        if search_entry.get() == "Search by...":
            search_entry.delete(0, "end")
            search_entry.config(fg=COLORS["text"])

    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "Search by...")
            search_entry.config(fg=COLORS["text_sec"])

    search_entry.bind("<FocusIn>", on_entry_click)
    search_entry.bind("<FocusOut>", on_focus_out)

    search_entry.pack(side="left", fill="x", expand=True, padx=15, pady=5)
    
    # Search Icon Button
    search_icon = tk.Label(search_frame, text="🔍", bg=COLORS["card_bg"], fg=COLORS["primary"], font=("Segoe UI", 14), cursor="hand2")
    search_icon.pack(side="right", padx=15)

    # Section Title
    tk.Label(main_container, text="รายละเอียด", font=FONTS["h2"], bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 10))

    # Filter Frame - Dropdown เลือกวัน และเวลา
    filter_frame = tk.Frame(main_container, bg=COLORS["bg"])
    filter_frame.pack(fill="x", pady=(0, 15))
    
    # Day Filter
    tk.Label(filter_frame, text="วัน:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left", padx=(0, 5))
    
    from tkinter import ttk
    day_map = {
        "ทั้งหมด": "all", "จันทร์": "Mon", "อังคาร": "Tue", 
        "พุธ": "Wed", "พฤหัสบดี": "Thu", "ศุกร์": "Fri", "เสาร์": "Sat"
    }
    day_options = list(day_map.keys())
    day_var = tk.StringVar(value="ทั้งหมด")
    day_combo = ttk.Combobox(filter_frame, textvariable=day_var, values=day_options, state="readonly", font=FONTS["body"], width=12)
    day_combo.pack(side="left", padx=(0, 15))
    
    # Time Filter
    tk.Label(filter_frame, text="เวลา:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left", padx=(0, 5))
    
    time_options = ["ทั้งหมด", "08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]
    time_var = tk.StringVar(value="ทั้งหมด")
    time_combo = ttk.Combobox(filter_frame, textvariable=time_var, values=time_options, state="readonly", font=FONTS["body"], width=12)
    time_combo.pack(side="left")

    # Scrollable Area for Cards with Scrollbar
    cards_outer = tk.Frame(main_container, bg=COLORS["bg"])
    cards_outer.pack(fill="both", expand=True)
    
    # Canvas for scrolling
    cards_canvas = tk.Canvas(cards_outer, bg=COLORS["bg"], highlightthickness=0)
    cards_canvas.pack(side="left", fill="both", expand=True)
    
    # Scrollbar
    cards_scrollbar = tk.Scrollbar(cards_outer, orient="vertical", command=cards_canvas.yview)
    cards_scrollbar.pack(side="right", fill="y")
    cards_canvas.configure(yscrollcommand=cards_scrollbar.set)
    
    # Container inside canvas
    cards_container = tk.Frame(cards_canvas, bg=COLORS["bg"])
    cards_canvas.create_window((0, 0), window=cards_container, anchor="nw")
    
    def update_cards_scroll(event=None):
        cards_canvas.configure(scrollregion=cards_canvas.bbox("all"))
    
    cards_container.bind("<Configure>", update_cards_scroll)
    
    # Mouse wheel scrolling
    def on_mousewheel(event):
        cards_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    cards_canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ---------------- Data & Logic ----------------
    # ดึงข้อมูลอาจารย์ทั้งหมดจาก database
    SCHEDULE_DATA = db.get_all_teachers_with_schedule()

    from schedule_view import ScheduleViewer

    def create_card(parent, item):
        # Card Container
        card = tk.Frame(parent, bg=COLORS["card_bg"], bd=0)
        card.pack(fill="x", pady=8, ipady=5)
        
        # Left Accent Line
        accent_line = tk.Frame(card, bg=COLORS["primary"], width=4)
        accent_line.pack(side="left", fill="y")
        
        content = tk.Frame(card, bg=COLORS["card_bg"])
        content.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        # Name (Clickable)
        def show_schedule():
            # Make sure schedule data is included
            teacher_with_schedule = {
                "name": item["name"],
                "subject": item["subject"],
                "time": item.get("time", item.get("contact", "")),
                "room": item["room"],
                "schedule": item.get("schedule", [])
            }
            ScheduleViewer(schedule, teacher_with_schedule)
        
        name_label = tk.Label(content, text=item["name"], font=FONTS["body_bold"], bg=COLORS["card_bg"], fg=COLORS["text"], cursor="hand2")
        name_label.pack(anchor="w")
        name_label.bind("<Button-1>", lambda e: show_schedule())

        # Subject (smaller, grey)
        tk.Label(content, text=item["subject"], font=FONTS["small"], bg=COLORS["card_bg"], fg=COLORS["text_sec"]).pack(anchor="w")

        # Contact info
        contact_text = item.get("time", item.get("contact", ""))
        tk.Label(content, text=contact_text, font=FONTS["small"], bg=COLORS["card_bg"], fg=COLORS["text_sec"]).pack(anchor="w")

        # Room
        room_label = tk.Label(content, text=f"🚪 {item['room']}", font=FONTS["small"], bg=COLORS["card_bg"], fg=COLORS["primary"])
        room_label.pack(anchor="w")

    # Filter and Search Function
    def filter_and_search():
        # Clear existing cards
        for widget in cards_container.winfo_children():
            widget.destroy()
        
        # Get filter values
        search_text = search_entry.get().lower()
        if search_text == "search by...":
            search_text = ""
        
        selected_day_thai = day_var.get()
        selected_day = day_map[selected_day_thai]
        selected_time = time_var.get()
        
        # Filter data
        filtered_data = []
        for teacher in SCHEDULE_DATA:
            # Search filter (ชื่อ, วิชา, ห้อง)
            if search_text:
                name_match = search_text in teacher["name"].lower()
                subject_match = search_text in teacher["subject"].lower()
                room_match = search_text in teacher["room"].lower()
                if not (name_match or subject_match or room_match):
                    continue
            
            # Day filter
            if selected_day != "all":
                teacher_schedule = teacher.get("schedule", [])
                has_day = any(cls["day"] == selected_day for cls in teacher_schedule)
                if not has_day:
                    continue
            
            # Time filter
            if selected_time != "ทั้งหมด":
                time_parts = selected_time.split("-")
                if len(time_parts) == 2:
                    start_filter = time_parts[0].strip()
                    end_filter = time_parts[1].strip()
                    
                    teacher_schedule = teacher.get("schedule", [])
                    has_time = False
                    for cls in teacher_schedule:
                        cls_start = cls.get("start", "")
                        cls_end = cls.get("end", "")
                        # Check if class time overlaps with filter time
                        if cls_start >= start_filter and cls_start < end_filter:
                            has_time = True
                            break
                        if cls_end > start_filter and cls_end <= end_filter:
                            has_time = True
                            break
                    
                    if not has_time:
                        continue
            
            filtered_data.append(teacher)
        
        # Render filtered cards
        if filtered_data:
            for teacher in filtered_data:
                create_card(cards_container, teacher)
        else:
            tk.Label(
                cards_container, text="ไม่พบข้อมูล",
                font=FONTS["body"], bg=COLORS["card_bg"], fg=COLORS["text_sec"],
                pady=20
            ).pack(fill="x")
        
        update_cards_scroll()
    
    # Bind search and filter events
    search_icon.bind("<Button-1>", lambda e: filter_and_search())
    search_entry.bind("<Return>", lambda e: filter_and_search())
    day_combo.bind("<<ComboboxSelected>>", lambda e: filter_and_search())
    time_combo.bind("<<ComboboxSelected>>", lambda e: filter_and_search())
    
    # Initial render - show all
    filter_and_search()

# ------------------ หน้า Login ------------------
def login():
    global current_teacher_id, current_teacher_data
    user = username.get()
    pwd = password.get()
    role = login_role.get()
    
    # Check if placeholder text is still there
    if user == "Username" or pwd == "Password":
        messagebox.showerror("Login Failed", "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
        return

    if role == "Student":
        # ตรวจสอบรหัสผ่านนักศึกษาจาก database
        if db.verify_student(user, pwd):
            # ล้างข้อมูลในฟอร์ม
            username.delete(0, "end")
            username.insert(0, "Username")
            username.config(fg=COLORS["text_sec"])
            password.delete(0, "end")
            password.insert(0, "Password")
            password.config(show="", fg=COLORS["text_sec"])
            
            root.withdraw()  # ซ่อนหน้า login
            open_schedule_page_student(root, {"name": user})  # เข้าหน้าค้นหาอาจารย์
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    elif role == "Teacher":
        # ตรวจสอบรหัสผ่านอาจารย์จาก database
        teacher = db.get_teacher_by_username(user)
        if teacher and teacher["password"] == pwd:
            current_teacher_id = teacher["id"]
            # ดึงตารางสอนจาก database
            teacher["schedule"] = db.get_teacher_schedule(teacher["id"])
            current_teacher_data = teacher
            
            # ล้างข้อมูลในฟอร์ม
            username.delete(0, "end")
            username.insert(0, "Username")
            username.config(fg=COLORS["text_sec"])
            password.delete(0, "end")
            password.insert(0, "Password")
            password.config(show="", fg=COLORS["text_sec"])
            
            root.withdraw()  # ซ่อนหน้า login
            from teacher_pages import open_teacher_dashboard
            open_teacher_dashboard(root, teacher)  # ใช้ root เดิม
        else:
            messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

# Initialize database first
if not db.init_database():
    import sys
    messagebox.showerror("Database Error", "ไม่สามารถเชื่อมต่อกับฐานข้อมูลได้\nกรุณาตรวจสอบว่า MySQL server กำลังรันอยู่")
    sys.exit(1)

root = tk.Tk()
root.title("Login")
root.geometry("400x500")
root.config(bg=COLORS["bg"])

configure_styles()

# Center container
container = tk.Frame(root, bg=COLORS["bg"])
container.place(relx=0.5, rely=0.5, anchor="center")

# Card Frame
frame = tk.Frame(container, bg=COLORS["card_bg"], padx=40, pady=30)
frame.pack()

# ---------------- Logo ----------------
LOGO_PATH = "logo.jpg"  # Change to .jpg
if os.path.exists(LOGO_PATH):
    try:
        if HAS_PIL:
            # Open with PIL
            pil_image = Image.open(LOGO_PATH)
            # Resize if too big (max width 200px)
            max_width = 200
            if pil_image.size[0] > max_width:
                w_percent = (max_width / float(pil_image.size[0]))
                hsize = int((float(pil_image.size[1]) * float(w_percent)))
                pil_image = pil_image.resize((max_width, hsize), Image.Resampling.LANCZOS)
            
            logo_img = ImageTk.PhotoImage(pil_image)
        else:
            # Fallback for PNG/GIF if PIL is missing (likely won't work for JPG)
            logo_img = tk.PhotoImage(file=LOGO_PATH)

        # Keep a reference to avoid garbage collection
        logo_label = tk.Label(frame, image=logo_img, bg=COLORS["card_bg"])
        logo_label.image = logo_img 
        logo_label.pack(pady=(0, 10))
    except Exception as e:
        # Silently fail if logo can't be loaded
        pass

tk.Label(frame, text="Welcome Back", font=FONTS["h1"], bg=COLORS["card_bg"], fg=COLORS["text"]).pack(pady=(0, 5))
tk.Label(frame, text="Please sign in to continue", font=FONTS["small"], bg=COLORS["card_bg"], fg=COLORS["text_sec"]).pack(pady=(0, 20))

# ---------------- Role Selection ----------------
tk.Label(frame, text="LOGIN AS", font=("Segoe UI", 8, "bold"), bg=COLORS["card_bg"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(0, 5))

login_role = tk.StringVar(value="Student")

role_frame = tk.Frame(frame, bg=COLORS["card_bg"])
role_frame.pack(fill="x", pady=(0, 20))

tk.Radiobutton(role_frame, text="User", variable=login_role, value="Student", bg=COLORS["card_bg"], fg=COLORS["text"], selectcolor=COLORS["primary"], font=FONTS["body"], activebackground=COLORS["card_bg"], activeforeground=COLORS["text"]).pack(side="left", padx=(0, 20))
tk.Radiobutton(role_frame, text="Admin", variable=login_role, value="Teacher", bg=COLORS["card_bg"], fg=COLORS["text"], selectcolor=COLORS["primary"], font=FONTS["body"], activebackground=COLORS["card_bg"], activeforeground=COLORS["text"]).pack(side="left")

# ---------------- Username ----------------
tk.Label(frame, text="USERNAME", font=("Segoe UI", 8, "bold"), bg=COLORS["card_bg"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(0, 5))

username = tk.Entry(frame, font=FONTS["body"], bd=0, bg=COLORS["input_bg"], fg=COLORS["text_sec"], insertbackground=COLORS["primary"])
username.insert(0, "Username")
username.pack(fill="x", ipady=10, pady=(0, 15))

def on_username_click(event):
    if username.get() == "Username":
        username.delete(0, "end")
        username.config(fg=COLORS["text"])

def on_username_focus_out(event):
    if username.get() == "":
        username.insert(0, "Username")
        username.config(fg=COLORS["text_sec"])

username.bind("<FocusIn>", on_username_click)
username.bind("<FocusOut>", on_username_focus_out)

# ---------------- Password ----------------
tk.Label(frame, text="PASSWORD", font=("Segoe UI", 8, "bold"), bg=COLORS["card_bg"], fg=COLORS["text_sec"]).pack(anchor="w", pady=(0, 5))

password = tk.Entry(frame, font=FONTS["body"], bd=0, bg=COLORS["input_bg"], fg=COLORS["text_sec"], insertbackground=COLORS["primary"])
password.insert(0, "Password")
password.pack(fill="x", ipady=10, pady=(0, 20))

def on_password_click(event):
    if password.get() == "Password":
        password.delete(0, "end")
        password.config(show="*", fg=COLORS["text"])

def on_password_focus_out(event):
    if password.get() == "":
        password.config(show="")
        password.insert(0, "Password")
        password.config(fg=COLORS["text_sec"])

password.bind("<FocusIn>", on_password_click)
password.bind("<FocusOut>", on_password_focus_out)

# ---------------- Login Button ----------------
login_btn = tk.Button(
    frame, text="Sign In", font=FONTS["body_bold"],
    bg=COLORS["primary"], fg=COLORS["bg"], bd=0, cursor="hand2",
    activebackground=COLORS["primary_dark"], activeforeground="white",
    command=login
)
login_btn.pack(fill="x", ipady=10)

if __name__ == "__main__":
    root.mainloop()
