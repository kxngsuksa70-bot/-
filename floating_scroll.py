"""
Floating Scroll Buttons - เหมือนในเว็บไซต์
ปุ่มเลื่อนขึ้น-ลงแบบลอยที่มุมหน้าจอ
"""
import tkinter as tk

def add_floating_scroll_buttons(parent, canvas, bg_color, button_color, text_color):
    """
    เพิ่มปุ่ม scroll แบบลอย (floating) ที่มุมล่างขวา
    
    Args:
        parent: parent widget (window หรือ frame)
        canvas: canvas ที่ต้องการควบคุม
        bg_color: สีพื้นหลังปุ่ม
        button_color: สีปุ่ม
        text_color: สีข้อความ
    """
    # Container for floating buttons (อยู่มุมล่างขวา)
    floating_container = tk.Frame(parent, bg=bg_color)
    floating_container.place(relx=0.95, rely=0.85, anchor="se")
    
    # Scroll to top button
    def scroll_to_top():
        canvas.yview_moveto(0)  # เลื่อนขึ้นบนสุด
    
    top_btn = tk.Button(
        floating_container, text="↑ บนสุด", 
        font=("Segoe UI", 10, "bold"),
        bg=button_color, fg=text_color, bd=0, cursor="hand2",
        command=scroll_to_top, padx=12, pady=8,
        relief="raised"
    )
    top_btn.pack(pady=(0, 5))
    
    # Scroll to bottom button
    def scroll_to_bottom():
        canvas.yview_moveto(1)  # เลื่อนลงล่างสุด
    
    bottom_btn = tk.Button(
        floating_container, text="↓ ล่างสุด",
        font=("Segoe UI", 10, "bold"),
        bg=button_color, fg=text_color, bd=0, cursor="hand2",
        command=scroll_to_bottom, padx=12, pady=8,
        relief="raised"
    )
    bottom_btn.pack()
    
    return floating_container
