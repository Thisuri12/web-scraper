import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from scraper import scrape_emails

def run_scraper(input_path, selected_country, progress, status_label):
    def update_progress(current, total, company):
        progress["maximum"] = total
        progress["value"] = current
        status_label.config(text=f"Scraping: {company}")
        status_label.update_idletasks()
        progress.update_idletasks()

    try:
        df = pd.read_excel(input_path)

        def progress_callback(current, total, company_name):
            update_progress(current, total, company_name)

        progress.pack(pady=10)
        status_label.pack(pady=(0, 10))

        results = scrape_emails(df, selected_country, progress_callback=progress_callback)

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Output As"
        )
        results.to_excel(output_path, index=False)
        messagebox.showinfo("Success", f"Scraping complete.\nSaved to:\n{output_path}")
        status_label.config(text="Scraping complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Error during scraping")
    finally:
        progress.pack_forget()

def launch_gui():
    root = tk.Tk()
    root.title("Detail Scraper")
    root.geometry("500x500")
    root.configure(bg="#f0f0f0")

    input_path = tk.StringVar()
    selected_country = tk.StringVar()

    tk.Label(root, text="Web Scraper 2.0", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    upload_frame = tk.Frame(root, bg="#f0f0f0")
    upload_frame.pack(pady=10)

    tk.Label(upload_frame, text="Upload Excel File:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=10)
    tk.Button(upload_frame, text="Browse", width=15, command=lambda: upload_file()).grid(row=0, column=1, padx=10)

    file_label = tk.Label(upload_frame, text="No file selected", font=("Helvetica", 10), fg="gray", bg="#f0f0f0")
    file_label.grid(row=1, column=0, columnspan=2, pady=5)

    def upload_file():
        path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        input_path.set(path)
        file_label.config(text=f"✅ Selected: {path.split('/')[-1]}", fg="green")

    country_frame = tk.Frame(root, bg="#f0f0f0")
    country_frame.pack(pady=10)

    tk.Label(country_frame, text="Select Country:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=10)
    countries = ["Italy", "France", "Germany", "Spain", "United Kingdom"]
    combo = ttk.Combobox(country_frame, textvariable=selected_country, values=countries, width=20)
    combo.grid(row=0, column=1, padx=10)

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    status_label = tk.Label(root, text="", font=("Helvetica", 11), bg="#f0f0f0")

    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    def on_submit():
        if not input_path.get():
            messagebox.showwarning("Missing File", "Please upload an Excel file.")
            return
        if not selected_country.get():
            messagebox.showwarning("Missing Country", "Please select a country.")
            return

        threading.Thread(
            target=run_scraper,
            args=(input_path.get(), selected_country.get(), progress, status_label),
            daemon=True
        ).start()

    def on_cancel():
        confirm = messagebox.askyesno("Confirm Cancel", "Are you sure you want to exit?")
        if confirm:
            root.destroy()

    tk.Button(button_frame, text="Start Scraping", width=20, bg="#4CAF50", fg="white", font=("Helvetica", 11), command=on_submit).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Cancel", width=20, bg="#f44336", fg="white", font=("Helvetica", 11), command=on_cancel).grid(row=0, column=1, padx=10)

    root.mainloop()
