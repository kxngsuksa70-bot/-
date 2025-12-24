"""
Scrollable Frame Widget with Standard Scrollbar
"""
import tkinter as tk

def create_scrollable_frame(parent, bg_color, scrollbar_bg=None):
    """
    สร้าง scrollable frame พร้อม scrollbar แบบปกติ
    
    Args:
        parent: parent widget
        bg_color: สีพื้นหลัง
        scrollbar_bg: สี scrollbar (optional)
    
    Returns:
        tuple: (outer_frame, canvas, content_frame, update_scroll_function)
    """
    # Outer frame
    outer_frame = tk.Frame(parent, bg=bg_color)
    
    # Canvas for scrolling
    canvas = tk.Canvas(outer_frame, bg=bg_color, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Content frame inside canvas
    content_frame = tk.Frame(canvas, bg=bg_color)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # Update scroll region function
    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    content_frame.bind("<Configure>", update_scroll_region)
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    return outer_frame, canvas, content_frame, update_scroll_region
