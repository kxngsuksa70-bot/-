import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ หน้า Schedule Search ------------------
def open_schedule_page():
    schedule = tk.Toplevel()
    schedule.title("Schedule Search")
    schedule.geometry("380x700")
    schedule.config(bg="#f5f5f5")

    frame = tk.Frame(schedule, bg="#f5f5f5")
    frame.pack(fill="both", expand=True, pady=20)

    title = tk.Label(frame, text="Schedule Search", font=("Segoe UI", 22, "bold"), bg="#f5f5f5")
    title.pack(pady=(10, 20))

    search_entry = tk.Entry(frame, font=("Segoe UI", 12), bd=0, relief="flat")
    search_entry.insert(0, "Search by...")
    search_frame = tk.Frame(frame, bg="white", bd=1, relief="solid")
    search_frame.pack(padx=20, pady=5, fill="x")
    search_entry.pack(in_=search_frame, side="left", fill="x", ipadx=10, ipady=10, expand=True)
    tk.Label(search_frame, text="🔍", bg="white").pack(side="right", padx=10)

    dropdown_frame = tk.Frame(frame, bg="#f5f5f5")
    dropdown_frame.pack(padx=20, pady=10, fill="x")

    day_box = ttk.Combobox(dropdown_frame, values=["Mon","Tue","Wed","Thu","Fri","Sat"], font=("Segoe UI", 12))
    day_box.set("Day")
    time_box = ttk.Combobox(dropdown_frame, values=["08:00","09:00","10:00","11:00"], font=("Segoe UI", 12))
    time_box.set("Time")

    day_box.pack(side="left", fill="x", expand=True, padx=5)
    time_box.pack(side="left", fill="x", expand=True, padx=5)

    tk.Label(frame, text="Results", font=("Segoe UI", 14, "bold"), bg="#f5f5f5").pack(anchor="w", padx=20, pady=(20, 5))

    def create_card(parent, name, subject, time, room):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=8, fill="x")

        tk.Label(card, text=name, font=("Segoe UI", 13, "bold"), bg="white").pack(anchor="w", pady=(10, 0), padx=10)
        tk.Label(card, text=subject, font=("Segoe UI", 11), fg="#555", bg="white").pack(anchor="w", padx=10)

        bottom = tk.Frame(card, bg="white")
        bottom.pack(fill="x", pady=10)

        tk.Label(bottom, text=time, font=("Segoe UI", 11), bg="white").pack(side="left", padx=10)
        tk.Label(bottom, text=room, font=("Segoe UI", 11), bg="white").pack(side="right", padx=10)

    create_card(frame, "Dr. John Smith", "Mathematics III", "9:00 AM - 10:30 AM", "Room 101")
    create_card(frame, "Prof. Emily Johnson", "Chemistry", "9:00 AM - 10:30 AM", "Room 202")
    create_card(frame, "Dr. Michael Lee", "Physics", "9:00 AM - 10:30 AM", "Room 303")
    create_card(frame, "Prof. Linda Brown", "English Literature", "9:00 AM - 10:30 AM", "Room 404")


# ------------------ หน้า Login ------------------
def login():
    user = username.get()
    pwd = password.get()

    # ตรวจสอบรหัสผ่าน
    if user == "คอมพิวเตอร์ธุรกิจ" and pwd == "1234":
        root.withdraw()
        open_schedule_page()
    else:
        messagebox.showerror("Login Failed", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

root = tk.Tk()
root.title("Login")
root.geometry("400x300")
root.config(bg="#f0f2f5")

frame = tk.Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=220)

tk.Label(frame, text="Login", font=("Segoe UI", 20, "bold"), bg="white").pack(pady=10)

username = tk.Entry(frame, font=("Segoe UI", 13))
username.insert(0, "Username")
username.pack(fill="x", pady=8, ipadx=5, ipady=5, padx=20)

password = tk.Entry(frame, font=("Segoe UI", 13), show="")
password.insert(0, "Password")
password.pack(fill="x", pady=8, ipadx=5, ipady=5, padx=20)

# ปุ่ม Login
tk.Button(
    frame, text="Login", font=("Segoe UI", 13, "bold"),
    bg="#2979ff", fg="white", bd=0, cursor="hand2",
    command=login
).pack(pady=15, fill="x", padx=20, ipady=5)

root.mainloop()