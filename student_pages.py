import tkinter as tk
from tkinter import messagebox
import coppy
import database as db
from scrollable_widget import create_scrollable_frame

def open_student_dashboard(login_root, student_data):
    """Student Dashboard - shows personalized schedule"""
    dashboard = tk.Toplevel()
    dashboard.title(f"Student Dashboard - {student_data['name']}")
    dashboard.geometry("800x600")
    dashboard.config(bg=coppy.COLORS["bg"])
    
    # Main Container
    main_container = tk.Frame(dashboard, bg=coppy.COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=30, pady=20)
    
    # Header
    header_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    header_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(
        header_frame, text=f"ยินดีต้อนรับ, {student_data['name']}", 
        font=coppy.FONTS["h1"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["primary"]
    ).pack(side="left")
    
    # Logout Button
    def logout():
        dashboard.destroy()
        login_root.deiconify()
    
    logout_btn = tk.Button(
        header_frame, text="ออกจากระบบ", font=coppy.FONTS["body"],
        bg=coppy.COLORS["error"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        activebackground="#B00020", activeforeground="white",
        command=logout, padx=15, pady=5
    )
    logout_btn.pack(side="right")
    
    # Back to Search Button
    def back_to_search():
        dashboard.destroy()
    
    search_btn = tk.Button(
        header_frame, text="← ค้นหาตารางสอน", font=coppy.FONTS["body"],
        bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=0, cursor="hand2",
        activebackground=coppy.COLORS["primary"], activeforeground="white",
        command=back_to_search, padx=15, pady=5
    )
    search_btn.pack(side="right", padx=(0, 10))
    
    # Title
    tk.Label(main_container, text="ตารางเรียนของฉัน", font=coppy.FONTS["h2"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 20))
    
    # Create scrollable frame with scrollbar
    scroll_outer, scroll_canvas, schedule_container, update_scroll = create_scrollable_frame(
        main_container,
        coppy.COLORS["bg"]
    )
    scroll_outer.pack(fill="both", expand=True)
    
    # Fetch all teacher schedules from database
    all_schedules = db.get_all_teacher_schedules()
    
    if all_schedules:
        # Group by day
        days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        schedule_by_day = {day: [] for day in days_order}
        
        for schedule in all_schedules:
            # Parse day from time string (e.g., "Mon 08:00")
            try:
                day_time = schedule["time"].split()
                if len(day_time) >= 2:
                    day = day_time[0]
                    if day in schedule_by_day:
                        schedule_by_day[day].append(schedule)
            except:
                pass
        
        # Display by day
        for day in days_order:
            if schedule_by_day[day]:
                # Day header
                day_thai = get_day_thai(day)
                day_header = tk.Frame(schedule_container, bg=coppy.COLORS["primary"])
                day_header.pack(fill="x", pady=(10, 5))
                tk.Label(day_header, text=day_thai, font=coppy.FONTS["body_bold"], bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], padx=15, pady=8).pack(anchor="w")
                
                # Classes for this day
                for schedule in sorted(schedule_by_day[day], key=lambda x: x["time"]):
                    create_schedule_card(schedule_container, schedule).pack(fill="x", pady=2)
    else:
        tk.Label(
            schedule_container, text="ยังไม่มีตารางเรียน",
            font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"],
            pady=20
        ).pack(fill="x")

def create_schedule_card(parent, schedule):
    card = tk.Frame(parent, bg=coppy.COLORS["card_bg"])
    
    # Left accent
    accent = tk.Frame(card, bg=coppy.COLORS["primary"], width=4)
    accent.pack(side="left", fill="y")
    
    content = tk.Frame(card, bg=coppy.COLORS["card_bg"])
    content.pack(side="left", fill="both", expand=True, padx=15, pady=10)
    
    # Time
    tk.Label(content, text=schedule["time"], font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["primary"]).pack(anchor="w")
    
    # Course name
    tk.Label(content, text=schedule["course"], font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w")
    
    # Teacher and room
    info_text = f"อาจารย์: {schedule['teacher']} • {schedule['room']}"
    tk.Label(content, text=info_text, font=coppy.FONTS["small"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"]).pack(anchor="w")
    
    return card

def get_day_thai(day_en):
    days_map = {
        "Mon": "จันทร์", "Tue": "อังคาร", "Wed": "พุธ", 
        "Thu": "พฤหัสบดี", "Fri": "ศุกร์", "Sat": "เสาร์"
    }
    return days_map.get(day_en, day_en)
