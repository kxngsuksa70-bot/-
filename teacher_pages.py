import tkinter as tk
from tkinter import ttk, messagebox
import coppy
import database as db
from user_management import open_user_management_page

# ------------------ Teacher Dashboard ------------------
def open_teacher_dashboard(login_root, teacher_data):
    dashboard = tk.Toplevel()
    dashboard.title(f"Teacher Dashboard - {teacher_data['name']}")
    dashboard.geometry("900x700")
    dashboard.config(bg=coppy.COLORS["bg"])
    
    login_root.withdraw()
    dashboard.protocol("WM_DELETE_WINDOW", lambda: (dashboard.destroy(), login_root.deiconify()))
    
    # Main Container
    main_container = tk.Frame(dashboard, bg=coppy.COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=30, pady=20)
    
    # Header
    header_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    header_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(
        header_frame, text=f"ยินดีต้อนรับ, {teacher_data['name']}", 
        font=coppy.FONTS["h1"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["primary"]
    ).pack(side="left")
    
    # Logout
    def logout():
        dashboard.destroy()
        login_root.deiconify()
    
    logout_btn = tk.Button(
        header_frame, text="ออกจากระบบ", font=coppy.FONTS["body"],
        bg=coppy.COLORS["error"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        command=logout, padx=15, pady=5
    )
    logout_btn.pack(side="right")
    
    # Stats Cards
    stats_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    stats_frame.pack(fill="x", pady=(0, 20))
    
    create_stat_card(stats_frame, "รวมทั้งหมด", str(len(teacher_data["schedule"])), "📚").pack(side="left", fill="x", expand=True, padx=(0, 10))
    create_stat_card(stats_frame, "ห้องทำงาน", teacher_data["room"], "🚪").pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    # Quick Actions
    tk.Label(main_container, text="จัดการ", font=coppy.FONTS["h2"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 15))
    
    actions_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    actions_frame.pack(fill="x", pady=(0, 20))
    
    row1 = tk.Frame(actions_frame, bg=coppy.COLORS["bg"])
    row1.pack(fill="x", pady=(0, 10))
    
    def open_schedule_editor():
        open_schedule_edit_page(dashboard, login_root, teacher_data)
    
    schedule_btn = tk.Button(
        row1, text="📅 ตารางสอน", font=coppy.FONTS["body_bold"],
        bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2",
        command=open_schedule_editor, padx=20, pady=15
    )
    schedule_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    def open_profile():
        open_profile_page(dashboard, login_root, teacher_data)
    
    profile_btn = tk.Button(
        row1, text="👤 โปรไฟล์", font=coppy.FONTS["body_bold"],
        bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        command=open_profile, padx=20, pady=15
    )
    profile_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))
    
    row2 = tk.Frame(actions_frame, bg=coppy.COLORS["bg"])
    row2.pack(fill="x")
    
    def open_user_mgmt():
        open_user_management_page(dashboard, login_root, teacher_data)
    
    user_mgmt_btn = tk.Button(
        row2, text="👥 จัดการผู้ใช้", font=coppy.FONTS["body_bold"],
        bg="#2C2C2C", fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        command=open_user_mgmt, padx=20, pady=15
    )
    user_mgmt_btn.pack(fill="x")
    
    # Schedule Overview with Scrollable Canvas
    tk.Label(main_container, text="ภาพรวมตารางสอน", font=coppy.FONTS["h2"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(10, 15))
    
    # Create scrollable canvas with scrollbar
    overview_canvas = tk.Canvas(main_container, bg=coppy.COLORS["bg"], highlightthickness=0)
    overview_canvas.pack(side="left", fill="both", expand=True)
    
    # Scrollbar
    overview_scrollbar = tk.Scrollbar(main_container, orient="vertical", command=overview_canvas.yview)
    overview_scrollbar.pack(side="right", fill="y")
    overview_canvas.configure(yscrollcommand=overview_scrollbar.set)
    
    schedule_container = tk.Frame(overview_canvas, bg=coppy.COLORS["bg"])
    overview_canvas.create_window((0, 0), window=schedule_container, anchor="nw")
    
    def update_scroll_region(event=None):
        overview_canvas.configure(scrollregion=overview_canvas.bbox("all"))
    
    schedule_container.bind("<Configure>", update_scroll_region)
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        overview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    overview_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    if teacher_data["schedule"]:
        for class_item in teacher_data["schedule"]:
            create_class_card(schedule_container, class_item).pack(fill="x", pady=5)
    else:
        tk.Label(
            schedule_container, text="ยังไม่มีตารางสอน",
            font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"],
            pady=20
        ).pack(fill="x")

def create_stat_card(parent, title, value, icon):
    card = tk.Frame(parent, bg=coppy.COLORS["card_bg"])
    
    content = tk.Frame(card, bg=coppy.COLORS["card_bg"])
    content.pack(padx=20, pady=15)
    
    tk.Label(content, text=icon, font=("Segoe UI", 24), bg=coppy.COLORS["card_bg"]).pack()
    tk.Label(content, text=value, font=coppy.FONTS["h2"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["primary"]).pack()
    tk.Label(content, text=title, font=coppy.FONTS["small"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"]).pack()
    
    return card

def create_class_card(parent, class_item):
    card = tk.Frame(parent, bg=coppy.COLORS["card_bg"])
    
    accent = tk.Frame(card, bg=class_item.get("color", coppy.COLORS["primary"]), width=4)
    accent.pack(side="left", fill="y")
    
    content = tk.Frame(card, bg=coppy.COLORS["card_bg"])
    content.pack(side="left", fill="both", expand=True, padx=15, pady=10)
    
    day_time = f"{get_day_thai(class_item['day'])} • {class_item['start']} ({class_item['duration']}h)"
    tk.Label(content, text=day_time, font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w")
    
    tk.Label(content, text=class_item["subject"], font=coppy.FONTS["small"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"]).pack(anchor="w")
    
    return card

def get_day_thai(day_en):
    days_map = {
        "Mon": "จันทร์", "Tue": "อังคาร", "Wed": "พุธ", 
        "Thu": "พฤหัสบดี", "Fri": "ศุกร์", "Sat": "เสาร์"
    }
    return days_map.get(day_en, day_en)

# ------------------ Schedule Edit Page ------------------
def open_schedule_edit_page(parent_window, login_root, teacher_data):
    editor = tk.Toplevel(parent_window)
    editor.title("แก้ไขตารางสอน")
    editor.geometry("800x600")
    editor.config(bg=coppy.COLORS["bg"])
    
    main_container = tk.Frame(editor, bg=coppy.COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=30, pady=20)
    
    header_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    header_frame.pack(fill="x", pady=(0, 20))
    
    back_btn = tk.Button(
        header_frame, text="← ย้อนกลับ", font=coppy.FONTS["body"],
        bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        command=editor.destroy, padx=15, pady=5
    )
    back_btn.pack(side="left", padx=(0, 20))
    
    tk.Label(header_frame, text="ตารางสอนของฉัน", font=coppy.FONTS["h1"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["primary"]).pack(side="left")
    
    def add_class():
        open_class_dialog(editor, teacher_data, None)
        refresh_schedule_list()
    
    add_btn = tk.Button(
        header_frame, text="+ เพิ่มวิชา", font=coppy.FONTS["body"],
        bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2",
        command=add_class, padx=15, pady=5
    )
    add_btn.pack(side="right")
    
    table_header = tk.Frame(main_container, bg=coppy.COLORS["card_bg"])
    table_header.pack(fill="x", pady=(0, 10))
    
    tk.Label(table_header, text="วัน", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=10, anchor="w", padx=15, pady=10).pack(side="left")
    tk.Label(table_header, text="เวลา", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=10, anchor="w", padx=15, pady=10).pack(side="left")
    tk.Label(table_header, text="วิชา", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=20, anchor="w", padx=15, pady=10).pack(side="left", fill="x", expand=True)
    tk.Label(table_header, text="จัดการ", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=15, anchor="center", padx=15, pady=10).pack(side="right")
    
    # Create scrollable list container with standard scrollbar
    list_outer_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    list_outer_frame.pack(fill="both", expand=True)
    
    # Scrollable canvas for list
    list_canvas = tk.Canvas(list_outer_frame, bg=coppy.COLORS["bg"], highlightthickness=0)
    list_canvas.pack(side="left", fill="both", expand=True)
    
    # Standard scrollbar on the right
    list_scrollbar = tk.Scrollbar(list_outer_frame, orient="vertical", command=list_canvas.yview)
    list_scrollbar.pack(side="right", fill="y")
    list_canvas.configure(yscrollcommand=list_scrollbar.set)
    
    # List container inside canvas
    list_container = tk.Frame(list_canvas, bg=coppy.COLORS["bg"])
    list_canvas.create_window((0, 0), window=list_container, anchor="nw")
    
    def update_scroll_region(event=None):
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    
    list_container.bind("<Configure>", update_scroll_region)
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    list_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def refresh_schedule_list():
        for widget in list_container.winfo_children():
            widget.destroy()
        
        teacher_data["schedule"] = db.get_teacher_schedule(teacher_data["id"])
        
        for class_item in teacher_data["schedule"]:
            create_schedule_row(list_container, class_item, teacher_data, refresh_schedule_list, editor).pack(fill="x", pady=2)
    
    refresh_schedule_list()

def create_schedule_row(parent, class_item, teacher_data, refresh_callback, editor_window):
    row = tk.Frame(parent, bg=coppy.COLORS["card_bg"])
    
    accent = tk.Frame(row, bg=class_item.get("color", coppy.COLORS["primary"]), width=4)
    accent.pack(side="left", fill="y")
    
    tk.Label(row, text=get_day_thai(class_item["day"]), font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=10, anchor="w", padx=15, pady=12).pack(side="left")
    tk.Label(row, text=f"{class_item['start']} ({class_item['duration']}h)", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=10, anchor="w", padx=15, pady=12).pack(side="left")
    tk.Label(row, text=class_item["subject"], font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=20, anchor="w", padx=15, pady=12).pack(side="left", fill="x", expand=True)
    
    actions = tk.Frame(row, bg=coppy.COLORS["card_bg"])
    actions.pack(side="right", padx=15)
    
    def edit_class():
        open_class_dialog(editor_window, teacher_data, class_item)
        refresh_callback()
    
    edit_btn = tk.Button(
        actions, text="แก้ไข", font=coppy.FONTS["small"],
        bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2",
        command=edit_class, padx=10, pady=5
    )
    edit_btn.pack(side="left", padx=2)
    
    def delete_class():
        if messagebox.askyesno("ยืนยันการลบ", "คุณแน่ใจหรือไม่ที่จะลบวิชานี้?"):
            if db.delete_schedule(class_item["id"]):
                refresh_callback()
                messagebox.showinfo("สำเร็จ", "ลบวิชาเรียบร้อยแล้ว")
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถลบวิชาได้")
    
    delete_btn = tk.Button(
        actions, text="ลบ", font=coppy.FONTS["small"],
        bg=coppy.COLORS["error"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        command=delete_class, padx=10, pady=5
    )
    delete_btn.pack(side="left", padx=2)
    
    return row

# ------------------ Add/Edit Class Dialog ------------------
def open_class_dialog(parent, teacher_data, class_item=None):
    dialog = tk.Toplevel(parent)
    dialog.title("เพิ่มวิชา" if class_item is None else "แก้ไขวิชา")
    dialog.geometry("450x600")  # Reduced height to fit screen better
    dialog.config(bg=coppy.COLORS["card_bg"])
    dialog.transient(parent)
    dialog.grab_set()
    
    if class_item is not None:
        existing = class_item
    else:
        existing = {
            "day": "Mon", "start": "08:00", "end": "10:00", "duration": 2.0, 
            "subject": "", "course_code": "", "classroom": "", "color": "#4285F4"
        }
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(dialog, bg=coppy.COLORS["card_bg"])
    main_frame.pack(fill="both", expand=True)
    
    # Scroll down button at bottom (pack before main_frame expands)
    scroll_button_frame = tk.Frame(dialog, bg=coppy.COLORS["card_bg"])
    scroll_button_frame.pack(side="bottom", fill="x", padx=30, pady=5)
    
    # Create canvas and scrollbar
    canvas = tk.Canvas(main_frame, bg=coppy.COLORS["card_bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=coppy.COLORS["card_bg"])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Remove scroll button frame (not needed anymore)
    scroll_button_frame.destroy()
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    dialog.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))
    
    # Container inside scrollable frame
    container = tk.Frame(scrollable_frame, bg=coppy.COLORS["card_bg"])
    container.pack(fill="both", expand=True, padx=30, pady=20)

    
    tk.Label(container, text="รายละเอียดวิชา", font=coppy.FONTS["h2"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(pady=(0, 20))
    
    # Day Selection with Thai labels
    day_map = {
        "จันทร์": "Mon", "อังคาร": "Tue", "พุธ": "Wed",
        "พฤหัสบดี": "Thu", "ศุกร์": "Fri", "เสาร์": "Sat"
    }
    day_map_reverse = {v: k for k, v in day_map.items()}  # Reverse mapping
    
    tk.Label(container, text="วัน", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    day_var = tk.StringVar(value=day_map_reverse.get(existing["day"], "จันทร์"))
    day_combo = ttk.Combobox(container, textvariable=day_var, values=list(day_map.keys()), state="readonly", font=coppy.FONTS["body"])
    day_combo.pack(fill="x", pady=(0, 15))
    
    # Course Code
    tk.Label(container, text="รหัสวิชา", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    course_code_var = tk.StringVar(value=existing.get("course_code", ""))
    course_code_entry = tk.Entry(container, textvariable=course_code_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"])
    course_code_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    # Subject
    tk.Label(container, text="ชื่อวิชา", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    subject_var = tk.StringVar(value=existing["subject"])
    subject_entry = tk.Entry(container, textvariable=subject_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"])
    subject_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    # Start Time
    tk.Label(container, text="เวลาเริ่ม", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    start_time_var = tk.StringVar(value=existing["start"])
    start_time_combo = ttk.Combobox(container, textvariable=start_time_var, 
                                    values=["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"], 
                                    font=coppy.FONTS["body"])
    start_time_combo.pack(fill="x", pady=(0, 15))
    
    # End Time
    tk.Label(container, text="เวลาเลิก", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    end_time_var = tk.StringVar(value=existing.get("end", "10:00"))
    end_time_combo = ttk.Combobox(container, textvariable=end_time_var, 
                                   values=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"], 
                                   font=coppy.FONTS["body"])
    end_time_combo.pack(fill="x", pady=(0, 15))
    
    # Duration (Auto-calculated)
    tk.Label(container, text="ระยะเวลา (คำนวณอัตโนมัติ)", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    duration_display = tk.Label(container, text="2.0 ชั่วโมง", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["primary"], anchor="w", padx=10, pady=8)
    duration_display.pack(fill="x", pady=(0, 15))
    
    def calculate_duration(*args):
        try:
            start = start_time_var.get()
            end = end_time_var.get()
            
            start_h, start_m = map(int, start.split(":"))
            end_h, end_m = map(int, end.split(":"))
            
            start_decimal = start_h + start_m / 60.0
            end_decimal = end_h + end_m / 60.0
            
            duration = end_decimal - start_decimal
            
            if duration <= 0:
                duration_display.config(text="⚠️ เวลาไม่ถูกต้อง", fg=coppy.COLORS["error"])
            else:
                duration_display.config(text=f"{duration:.1f} ชั่วโมง", fg=coppy.COLORS["primary"])
            
            return duration
        except:
            duration_display.config(text="0.0 ชั่วโมง", fg=coppy.COLORS["error"])
            return 0.0
    
    start_time_var.trace_add("write", calculate_duration)
    end_time_var.trace_add("write", calculate_duration)
    calculate_duration()
    
    # Classroom
    tk.Label(container, text="ห้องเรียน", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    classroom_var = tk.StringVar(value=existing.get("classroom", ""))
    classroom_entry = tk.Entry(container, textvariable=classroom_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"])
    classroom_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    # Color
    tk.Label(container, text="สี", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    color_var = tk.StringVar(value=existing["color"])
    color_frame = tk.Frame(container, bg=coppy.COLORS["card_bg"])
    color_frame.pack(fill="x", pady=(0, 20))
    
    colors = ["#4285F4", "#DB4437", "#F4B400", "#0F9D58", "#673AB7", "#E91E63", "#009688", "#FF5722"]
    for color in colors:
        btn = tk.Button(color_frame, bg=color, width=3, height=1, bd=0, cursor="hand2", command=lambda c=color: color_var.set(c))
        btn.pack(side="left", padx=2)
    
    button_frame = tk.Frame(container, bg=coppy.COLORS["card_bg"])
    button_frame.pack(fill="x", pady=(10, 0))
    
    def save_class():
        duration = calculate_duration()
        
        if duration <= 0:
            messagebox.showerror("ข้อผิดพลาด", "เวลาเลิกต้องมากกว่าเวลาเริ่ม")
            return
        
        if not subject_var.get():
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกชื่อวิชา")
            return
        
        # Convert Thai day to English code
        day_thai = day_var.get()
        day_english = day_map.get(day_thai, "Mon")
        
        if class_item is not None:
            if db.update_schedule(
                class_item["id"],
                day_english,
                start_time_var.get(),
                end_time_var.get(),
                duration,
                subject_var.get(),
                course_code_var.get(),
                classroom_var.get(),
                color_var.get()
            ):
                messagebox.showinfo("สำเร็จ", "อัพเดทวิชาเรียบร้อยแล้ว")
                dialog.destroy()
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถอัพเดทวิชาได้")
        else:
            if db.add_schedule(
                teacher_data["id"],
                day_english,
                start_time_var.get(),
                end_time_var.get(),
                duration,
                subject_var.get(),
                course_code_var.get(),
                classroom_var.get(),
                color_var.get()
            ):
                messagebox.showinfo("สำเร็จ", "เพิ่มวิชาเรียบร้อยแล้ว")
                dialog.destroy()
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถเพิ่มวิชาได้")
    
    save_btn = tk.Button(
        button_frame, text="บันทึก", font=coppy.FONTS["body"],
        bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2",
        command=save_class, padx=20, pady=10
    )
    save_btn.pack(side="right", padx=(5, 0))
    
    cancel_btn = tk.Button(
        button_frame, text="ยกเลิก", font=coppy.FONTS["body"],
        bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=1, cursor="hand2",
        command=dialog.destroy, padx=20, pady=10
    )
    cancel_btn.pack(side="right")

# ------------------ Profile Page ------------------
def open_profile_page(parent_window, login_root, teacher_data):
    profile = tk.Toplevel(parent_window)
    profile.title("โปรไฟล์ของฉัน")
    profile.geometry("500x600")
    profile.config(bg=coppy.COLORS["bg"])
    
    main_container = tk.Frame(profile, bg=coppy.COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=30, pady=20)
    
    header_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    header_frame.pack(fill="x", pady=(0, 20))
    
    back_btn = tk.Button(
        header_frame, text="← ย้อนกลับ", font=coppy.FONTS["body"],
        bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        command=profile.destroy, padx=15, pady=5
    )
    back_btn.pack(side="left", padx=(0, 20))
    
    tk.Label(header_frame, text="โปรไฟล์ของฉัน", font=coppy.FONTS["h1"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["primary"]).pack(side="left")
    
    form = tk.Frame(main_container, bg=coppy.COLORS["card_bg"])
    form.pack(fill="both", expand=True, padx=0, pady=0)
    
    form_content = tk.Frame(form, bg=coppy.COLORS["card_bg"])
    form_content.pack(padx=30, pady=30)
    
    tk.Label(form_content, text="ชื่อ", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    name_var = tk.StringVar(value=teacher_data["name"])
    name_entry = tk.Entry(form_content, textvariable=name_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"], width=40)
    name_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(form_content, text="วิชา/ภาควิชา", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    subject_var = tk.StringVar(value=teacher_data["subject"])
    subject_entry = tk.Entry(form_content, textvariable=subject_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"], width=40)
    subject_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(form_content, text="เบอร์ติดต่อ", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    contact_var = tk.StringVar(value=teacher_data["contact"])
    contact_entry = tk.Entry(form_content, textvariable=contact_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"], width=40)
    contact_entry.pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(form_content, text="ห้องทำงาน", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    room_var = tk.StringVar(value=teacher_data["room"])
    room_entry = tk.Entry(form_content, textvariable=room_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, insertbackground=coppy.COLORS["primary"], width=40)
    room_entry.pack(fill="x", ipady=8, pady=(0, 20))
    
    def save_profile():
        if db.update_teacher_profile(teacher_data["id"], name_var.get(), subject_var.get(), contact_var.get(), room_var.get()):
            teacher_data["name"] = name_var.get()
            teacher_data["subject"] = subject_var.get()
            teacher_data["contact"] = contact_var.get()
            teacher_data["room"] = room_var.get()
            messagebox.showinfo("สำเร็จ", "อัพเดทโปรไฟล์เรียบร้อยแล้ว!")
            profile.destroy()
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถอัพเดทโปรไฟล์ได้")
    
    save_btn = tk.Button(
        form_content, text="บันทึกการเปลี่ยนแปลง", font=coppy.FONTS["body_bold"],
        bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2",
        command=save_profile, padx=30, pady=12
    )
    save_btn.pack(fill="x")
