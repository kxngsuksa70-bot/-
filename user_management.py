# ==================== User Management Page ====================
import tkinter as tk
from tkinter import ttk, messagebox
import coppy
import database as db

def open_user_management_page(parent_window, login_root, teacher_data):
    """หน้าจัดการผู้ใช้ (เพิ่ม/ลบ อาจารย์และนักศึกษา)"""
    mgmt = tk.Toplevel(parent_window)
    mgmt.title("จัดการผู้ใช้")
    mgmt.geometry("900x600")
    mgmt.config(bg=coppy.COLORS["bg"])
    
    main_container = tk.Frame(mgmt, bg=coppy.COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=30, pady=20)
    
    # Header
    header_frame = tk.Frame(main_container, bg=coppy.COLORS["bg"])
    header_frame.pack(fill="x", pady=(0, 20))
    
    back_btn = tk.Button(header_frame, text="← ย้อนกลับ", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=0, cursor="hand2", activebackground=coppy.COLORS["primary"], activeforeground="white", command=mgmt.destroy, padx=15, pady=5)
    back_btn.pack(side="left", padx=(0, 20))
    
    tk.Label(header_frame, text="จัดการผู้ใช้", font=coppy.FONTS["h1"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["primary"]).pack(side="left")
    
    # Tabs
    notebook = ttk.Notebook(main_container)
    notebook.pack(fill="both", expand=True)
    
    teachers_frame = tk.Frame(notebook, bg=coppy.COLORS["bg"])
    notebook.add(teachers_frame, text="อาจารย์")
    
    students_frame = tk.Frame(notebook, bg=coppy.COLORS["bg"])
    notebook.add(students_frame, text="นักศึกษา")
    
    # ========== Teachers Tab ==========
    teachers_content = tk.Frame(teachers_frame, bg=coppy.COLORS["bg"])
    teachers_content.pack(fill="both", expand=True, padx=20, pady=20)
    
    teachers_header = tk.Frame(teachers_content, bg=coppy.COLORS["bg"])
    teachers_header.pack(fill="x", pady=(0, 15))
    
    tk.Label(teachers_header, text="รายชื่ออาจารย์", font=coppy.FONTS["h2"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["text"]).pack(side="left")
    
    def add_teacher():
        open_add_teacher_dialog(mgmt, refresh_teachers)
    
    add_teacher_btn = tk.Button(teachers_header, text="+ เพิ่มอาจารย์", font=coppy.FONTS["body"], bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2", command=add_teacher, padx=15, pady=8)
    add_teacher_btn.pack(side="right")
    
    teachers_list_frame = tk.Frame(teachers_content, bg=coppy.COLORS["bg"])
    teachers_list_frame.pack(fill="both", expand=True)
    
    def refresh_teachers():
        for widget in teachers_list_frame.winfo_children():
            widget.destroy()
        
        teachers = db.get_all_teachers()
        if teachers:
            header = tk.Frame(teachers_list_frame, bg=coppy.COLORS["card_bg"])
            header.pack(fill="x", pady=(0, 5))
            tk.Label(header, text="Username", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=15, anchor="w", padx=10, pady=8).pack(side="left")
            tk.Label(header, text="ชื่อ", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=25, anchor="w", padx=10, pady=8).pack(side="left")
            tk.Label(header, text="วิชา", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=20, anchor="w", padx=10, pady=8).pack(side="left", fill="x", expand=True)
            tk.Label(header, text="", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=10, anchor="w", padx=10, pady=8).pack(side="left")
            
            for t in teachers:
                row = tk.Frame(teachers_list_frame, bg=coppy.COLORS["card_bg"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=t["username"], font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=15, anchor="w", padx=10, pady=8).pack(side="left")
                tk.Label(row, text=t["name"], font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=25, anchor="w", padx=10, pady=8).pack(side="left")
                tk.Label(row, text=t["subject"] or "-", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"], width=20, anchor="w", padx=10, pady=8).pack(side="left", fill="x", expand=True)
                
                def delete_teacher_action(teacher_id=t["id"], teacher_name=t["name"]):
                    if messagebox.askyesno("ยืนยันการลบ", f"คุณต้องการลบอาจารย์ {teacher_name} ใช่หรือไม่?"):
                        if db.delete_teacher(teacher_id):
                            messagebox.showinfo("สำเร็จ", "ลบอาจารย์เรียบร้อย")
                            refresh_teachers()
                        else:
                            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถลบได้")
                
                del_btn = tk.Button(row, text="ลบ", font=coppy.FONTS["body"], bg=coppy.COLORS["error"], fg=coppy.COLORS["text"], bd=0, cursor="hand2", command=delete_teacher_action, padx=10, pady=4)
                del_btn.pack(side="left", padx=10)
        else:
            tk.Label(teachers_list_frame, text="ยังไม่มีข้อมูลอาจารย์", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"], pady=20).pack(fill="x")
    
    refresh_teachers()
    
    # ========== Students Tab ==========
    students_content = tk.Frame(students_frame, bg=coppy.COLORS["bg"])
    students_content.pack(fill="both", expand=True, padx=20, pady=20)
    
    students_header = tk.Frame(students_content, bg=coppy.COLORS["bg"])
    students_header.pack(fill="x", pady=(0, 15))
    
    tk.Label(students_header, text="รายชื่อนักศึกษา", font=coppy.FONTS["h2"], bg=coppy.COLORS["bg"], fg=coppy.COLORS["text"]).pack(side="left")
    
    def add_student():
        open_add_student_dialog(mgmt, refresh_students)
    
    add_student_btn = tk.Button(students_header, text="+ เพิ่มนักศึกษา", font=coppy.FONTS["body"], bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2", command=add_student, padx=15, pady=8)
    add_student_btn.pack(side="right")
    
    students_list_frame = tk.Frame(students_content, bg=coppy.COLORS["bg"])
    students_list_frame.pack(fill="both", expand=True)
    
    def refresh_students():
        for widget in students_list_frame.winfo_children():
            widget.destroy()
        
        students = db.get_all_students()
        if students:
            header = tk.Frame(students_list_frame, bg=coppy.COLORS["card_bg"])
            header.pack(fill="x", pady=(0, 5))
            tk.Label(header, text="Username", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=20, anchor="w", padx=10, pady=8).pack(side="left")
            tk.Label(header, text="ชื่อ", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=30, anchor="w", padx=10, pady=8).pack(side="left", fill="x", expand=True)
            tk.Label(header, text="", font=coppy.FONTS["body_bold"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=10, anchor="w", padx=10, pady=8).pack(side="left")
            
            for s in students:
                row = tk.Frame(students_list_frame, bg=coppy.COLORS["card_bg"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=s["username"], font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=20, anchor="w", padx=10, pady=8).pack(side="left")
                tk.Label(row, text=s["name"], font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], width=30, anchor="w", padx=10, pady=8).pack(side="left", fill="x", expand=True)
                
                def delete_student_action(student_id=s["id"], student_name=s["name"]):
                    if messagebox.askyesno("ยืนยันการลบ", f"คุณต้องการลบนักศึกษา {student_name} ใช่หรือไม่?"):
                        if db.delete_student(student_id):
                            messagebox.showinfo("สำเร็จ", "ลบนักศึกษาเรียบร้อย")
                            refresh_students()
                        else:
                            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถลบได้")
                
                del_btn = tk.Button(row, text="ลบ", font=coppy.FONTS["body"], bg=coppy.COLORS["error"], fg=coppy.COLORS["text"], bd=0, cursor="hand2", command=delete_student_action, padx=10, pady=4)
                del_btn.pack(side="left", padx=10)
        else:
            tk.Label(students_list_frame, text="ยังไม่มีข้อมูลนักศึกษา", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text_sec"], pady=20).pack(fill="x")
    
    refresh_students()


def open_add_teacher_dialog(parent, refresh_callback):
    dialog = tk.Toplevel(parent)
    dialog.title("เพิ่มอาจารย์")
    dialog.geometry("450x550")
    dialog.config(bg=coppy.COLORS["card_bg"])
    dialog.transient(parent)
    dialog.grab_set()
    
    # Create scrollable canvas
    main_frame = tk.Frame(dialog, bg=coppy.COLORS["card_bg"])
    main_frame.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(main_frame, bg=coppy.COLORS["card_bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=coppy.COLORS["card_bg"])
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Enable mousewheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    container = tk.Frame(scrollable_frame, bg=coppy.COLORS["card_bg"])
    container.pack(fill="both", expand=True, padx=30, pady=20)
    
    tk.Label(container, text="เพิ่มอาจารย์ใหม่", font=coppy.FONTS["h2"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(pady=(0, 20))
    
    tk.Label(container, text="Username", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    username_var = tk.StringVar()
    tk.Entry(container, textvariable=username_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="Password", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    password_var = tk.StringVar()
    tk.Entry(container, textvariable=password_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, show="*").pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="ชื่อ-นามสกุล", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    name_var = tk.StringVar()
    tk.Entry(container, textvariable=name_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="วิชา/ภาควิชา", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    subject_var = tk.StringVar()
    tk.Entry(container, textvariable=subject_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="เบอร์ติดต่อ", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    contact_var = tk.StringVar()
    tk.Entry(container, textvariable=contact_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="ห้องทำงาน", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    room_var = tk.StringVar()
    tk.Entry(container, textvariable=room_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 20))
    
    button_frame = tk.Frame(container, bg=coppy.COLORS["card_bg"])
    button_frame.pack(fill="x")
    
    def save_teacher():
        if not username_var.get().strip() or not password_var.get() or not name_var.get().strip():
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอก Username, Password และชื่อ")
            return
        
        if db.add_teacher(username_var.get().strip(), password_var.get(), name_var.get().strip(), subject_var.get().strip(), contact_var.get().strip(), room_var.get().strip()):
            messagebox.showinfo("สำเร็จ", "เพิ่มอาจารย์เรียบร้อย")
            refresh_callback()
            canvas.unbind_all("<MouseWheel>")
            dialog.destroy()
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถเพิ่มได้ (Username ซ้ำ?)")
    
    def cancel():
        canvas.unbind_all("<MouseWheel>")
        dialog.destroy()
    
    tk.Button(button_frame, text="บันทึก", font=coppy.FONTS["body"], bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2", command=save_teacher, padx=20, pady=10).pack(side="right", padx=(5, 0))
    tk.Button(button_frame, text="ยกเลิก", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=1, cursor="hand2", command=cancel, padx=20, pady=10).pack(side="right")


def open_add_student_dialog(parent, refresh_callback):
    dialog = tk.Toplevel(parent)
    dialog.title("เพิ่มนักศึกษา")
    dialog.geometry("450x350")
    dialog.config(bg=coppy.COLORS["card_bg"])
    dialog.transient(parent)
    dialog.grab_set()
    
    # Create scrollable canvas
    main_frame = tk.Frame(dialog, bg=coppy.COLORS["card_bg"])
    main_frame.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(main_frame, bg=coppy.COLORS["card_bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=coppy.COLORS["card_bg"])
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Enable mousewheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    container = tk.Frame(scrollable_frame, bg=coppy.COLORS["card_bg"])
    container.pack(fill="both", expand=True, padx=30, pady=20)
    
    tk.Label(container, text="เพิ่มนักศึกษาใหม่", font=coppy.FONTS["h2"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(pady=(0, 20))
    
    tk.Label(container, text="Username", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    username_var = tk.StringVar()
    tk.Entry(container, textvariable=username_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="Password", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    password_var = tk.StringVar()
    tk.Entry(container, textvariable=password_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0, show="*").pack(fill="x", ipady=8, pady=(0, 15))
    
    tk.Label(container, text="ชื่อ-นามสกุล", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"]).pack(anchor="w", pady=(0, 5))
    name_var = tk.StringVar()
    tk.Entry(container, textvariable=name_var, font=coppy.FONTS["body"], bg=coppy.COLORS["input_bg"], fg=coppy.COLORS["text"], bd=0).pack(fill="x", ipady=8, pady=(0, 20))
    
    button_frame = tk.Frame(container, bg=coppy.COLORS["card_bg"])
    button_frame.pack(fill="x")
    
    def save_student():
        if not username_var.get().strip() or not password_var.get() or not name_var.get().strip():
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return
        
        if db.add_student(username_var.get().strip(), password_var.get(), name_var.get().strip()):
            messagebox.showinfo("สำเร็จ", "เพิ่มนักศึกษาเรียบร้อย")
            refresh_callback()
            canvas.unbind_all("<MouseWheel>")
            dialog.destroy()
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถเพิ่มได้ (Username ซ้ำ?)")
    
    def cancel():
        canvas.unbind_all("<MouseWheel>")
        dialog.destroy()
    
    tk.Button(button_frame, text="บันทึก", font=coppy.FONTS["body"], bg=coppy.COLORS["primary"], fg=coppy.COLORS["bg"], bd=0, cursor="hand2", command=save_student, padx=20, pady=10).pack(side="right", padx=(5, 0))
    tk.Button(button_frame, text="ยกเลิก", font=coppy.FONTS["body"], bg=coppy.COLORS["card_bg"], fg=coppy.COLORS["text"], bd=1, cursor="hand2", command=cancel, padx=20, pady=10).pack(side="right")
