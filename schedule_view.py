import tkinter as tk
from tkinter import ttk

class ScheduleViewer(tk.Toplevel):
    def __init__(self, parent, teacher_info):
        super().__init__(parent)
        self.teacher_info = teacher_info
        self.title(f"Schedule - {teacher_info['name']}")
        self.geometry("1300x700")
        
        # Modern Dark Theme Colors
        self.COLORS = {
            "bg": "#121212",
            "card_bg": "#1E1E1E",
            "primary": "#BB86FC",
            "text": "#FFFFFF",
            "text_sec": "#B0B0B0",
            "grid_line": "#2C2C2C",
            "header_bg": "#252525"
        }
        
        self.config(bg=self.COLORS["bg"])
        
        # Header Section (Teacher Info)
        header_container = tk.Frame(self, bg=self.COLORS["card_bg"])
        header_container.pack(fill="x", padx=30, pady=20)
        
        header_frame = tk.Frame(header_container, bg=self.COLORS["card_bg"])
        header_frame.pack(fill="x", padx=20, pady=15)
        
        # Back Button
        back_btn = tk.Button(
            header_frame, text="← ย้อนกลับ", font=("Segoe UI", 10),
            bg="#2C2C2C", fg=self.COLORS["text"], bd=0, cursor="hand2",
            activebackground=self.COLORS["primary"], activeforeground="white",
            command=self.destroy, padx=15, pady=5
        )
        back_btn.pack(anchor="w", pady=(0, 10))
        
        # Name with accent color
        tk.Label(
            header_frame, 
            text=teacher_info['name'], 
            font=("Segoe UI", 22, "bold"), 
            bg=self.COLORS["card_bg"], 
            fg=self.COLORS["primary"]
        ).pack(anchor="w")
        
        # Details Row
        details_frame = tk.Frame(header_frame, bg=self.COLORS["card_bg"])
        details_frame.pack(fill="x", pady=(10, 0))
        
        # Subject
        tk.Label(
            details_frame, 
            text=f"📚 {teacher_info['subject']}", 
            font=("Segoe UI", 11), 
            bg=self.COLORS["card_bg"], 
            fg=self.COLORS["text_sec"]
        ).pack(side="left", padx=(0, 20))
        
        # Room
        tk.Label(
            details_frame, 
            text=f"📍 {teacher_info['room']}", 
            font=("Segoe UI", 11), 
            bg=self.COLORS["card_bg"], 
            fg=self.COLORS["text_sec"]
        ).pack(side="left", padx=(0, 20))
        
        # Time/Contact
        tk.Label(
            details_frame, 
            text=f"🕒 {teacher_info['time']}", 
            font=("Segoe UI", 11), 
            bg=self.COLORS["card_bg"], 
            fg=self.COLORS["text_sec"]
        ).pack(side="left")

        # Canvas for the grid
        self.canvas_frame = tk.Frame(self, bg=self.COLORS["bg"])
        self.canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            bg=self.COLORS["card_bg"], 
            bd=0, 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        self.days_map = {
            "Mon": "จันทร์", "Tue": "อังคาร", "Wed": "พุธ", 
            "Thu": "พฤหัสบดี", "Fri": "ศุกร์", "Sat": "เสาร์"
        }
        self.days_keys = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        self.hours = ["08:30 - 09:30", "09:30 - 10:30", "10:30 - 11:30", "11:30 - 12:30", "12:30 - 13:30", "13:30 - 14:30", "14:30 - 15:30", "15:30 - 16:30", "16:30 - 17:30", "17:30 - 18:30"]
        
        self.day_col_width = 100  # Width for Day names (Left column)
        self.time_col_width = 100  # Width for each Time slot (increased for better visibility)
        self.row_height = 60      # Height for each Day row
        self.header_height = 50   # Height for Time header
        
        self.schedule_data = teacher_info.get('schedule', [])
        
        self.draw_grid()
        self.draw_classes()

    def draw_grid(self):
        # Draw Header Background
        total_width = self.day_col_width + (len(self.hours) * self.time_col_width)
        self.canvas.create_rectangle(
            0, 0, total_width, self.header_height,
            fill=self.COLORS["header_bg"], outline=""
        )
        
        # Draw Header (Time) with modern styling
        for i, hour in enumerate(self.hours):
            x = self.day_col_width + (i * self.time_col_width)
            self.canvas.create_text(
                x + (self.time_col_width / 2), 
                self.header_height / 2, 
                text=hour, 
                font=("Segoe UI", 10, "bold"), 
                fill=self.COLORS["primary"]
            )
            # Vertical line for time
            self.canvas.create_line(
                x, 0, x, self.header_height + (len(self.days_keys) * self.row_height), 
                fill=self.COLORS["grid_line"], width=1
            )

        # Draw Days Column (Rows)
        for i, day_key in enumerate(self.days_keys):
            y = self.header_height + (i * self.row_height)
            
            # Alternating row background for better readability
            row_bg = self.COLORS["card_bg"] if i % 2 == 0 else "#191919"
            self.canvas.create_rectangle(
                0, y, total_width, y + self.row_height,
                fill=row_bg, outline=""
            )
            
            self.canvas.create_text(
                self.day_col_width / 2, 
                y + (self.row_height / 2), 
                text=self.days_map[day_key], 
                font=("Segoe UI", 11, "bold"), 
                fill=self.COLORS["text"]
            )
            
            # Horizontal line
            self.canvas.create_line(
                0, y, total_width, y, 
                fill=self.COLORS["grid_line"], width=1
            )

        # Final closing lines
        total_height = self.header_height + (len(self.days_keys) * self.row_height)
        self.canvas.create_line(
            total_width, 0, total_width, total_height, 
            fill=self.COLORS["grid_line"], width=2
        )
        self.canvas.create_line(
            0, total_height, total_width, total_height, 
            fill=self.COLORS["grid_line"], width=2
        )
        # Left border
        self.canvas.create_line(
            0, 0, 0, total_height, 
            fill=self.COLORS["grid_line"], width=2
        )
        # Day column separator
        self.canvas.create_line(
            self.day_col_width, 0, self.day_col_width, total_height, 
            fill=self.COLORS["grid_line"], width=2
        )

    def draw_classes(self):
        for item in self.schedule_data:
            if item["day"] not in self.days_keys: continue
            day_idx = self.days_keys.index(item["day"])
            
            # Parse start time
            start_h = int(item["start"].split(":")[0])
            start_m = int(item["start"].split(":")[1])
            
            # Calculate X position relative to 08:30 (8.5 hours)
            base_h = 8.5
            current_h = start_h + (start_m / 60)
            offset_hours = current_h - base_h
            
            # X Start = DayColumnWidth + (OffsetHours * TimeColWidth)
            x_start = self.day_col_width + (offset_hours * self.time_col_width)
            
            # Duration in hours -> Width
            duration = float(item["duration"]) if item["duration"] else 0.0
            width = duration * self.time_col_width
            
            # Debug for red box
            if "Database" in item["subject"]:
                print(f"\n=== {item['subject']} ===")
                print(f"Start: {item['start']}, End: {item.get('end', 'N/A')}")
                print(f"Duration: {duration} hours")
                print(f"X start: {x_start}, Width: {width}, X end: {x_start + width}")
                print(f"Should reach line at X={x_start + width}")
            
            # Y Start = HeaderHeight + (DayIndex * RowHeight)
            y_start = self.header_height + (day_idx * self.row_height) + 8 # +8 padding
            height = self.row_height - 16 # -16 padding for better spacing
            
            # Draw rounded rectangle (simulate with multiple rectangles)
            radius = 6
            color = item["color"]
            
            # Main rectangle
            self.canvas.create_rectangle(
                x_start + radius, y_start, 
                x_start + width - radius, y_start + height, 
                fill=color, outline="", tags="class_block"
            )
            self.canvas.create_rectangle(
                x_start, y_start + radius, 
                x_start + width, y_start + height - radius, 
                fill=color, outline="", tags="class_block"
            )
            
            # Calculate text lines and vertical centering
            lines = []
            lines.append(("subject", item["subject"], ("Segoe UI", 9, "bold")))
            
            if item.get("course_code"):
                lines.append(("code", item["course_code"], ("Segoe UI", 8)))
            
            if item.get("classroom"):
                lines.append(("room", f"🚪 {item['classroom']}", ("Segoe UI", 8)))
            
            # Calculate total height of text block
            line_heights = [12, 11, 11]  # Approximate heights for each line
            total_text_height = sum(line_heights[:len(lines)])
            
            # Start Y position to center vertically
            text_start_y = y_start + (height - total_text_height) / 2
            
            # X position for center horizontally
            center_x = x_start + (width / 2)
            
            # Draw each line
            current_y = text_start_y
            for i, (line_type, text, font) in enumerate(lines):
                self.canvas.create_text(
                    center_x, current_y,
                    text=text, 
                    anchor="n",  # Center horizontally, top anchor
                    font=font, 
                    fill="white", 
                    width=width - 16
                )
                current_y += line_heights[i]




