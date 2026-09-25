import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import requests
import threading

def validate_format(username):
    if not username:
        return False, "الرجاء إدخال اسم المستخدم."
    if len(username) < 2 or len(username) > 24:
        return False, "الطول يجب أن يكون بين 2 و 24 حرفًا."
    if not re.match(r"^[A-Za-z0-9._]+$", username):
        return False, "الأحرف المسموحة: حروف، أرقام، _ و . فقط."
    if username.startswith('.') or username.endswith('.'):
        return False, "لا يمكن أن يبدأ أو ينتهي بنقطة."
    if '..' in username:
        return False, "لا يُسمح بنقطتين متتاليتين."
    return True, "الصيغة صحيحة."

def check_availability(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        if r.status_code == 404:
            return True, "متاح ✅"
        elif r.status_code == 200:
            text = r.text.lower()
            if "couldn't find this account" in text or "user not found" in text:
                return True, "متاح ✅"
            return False, "محجوز ❌"
        else:
            return None, f"استجابة غير متوقعة: {r.status_code}"
    except requests.RequestException as e:
        return None, f"خطأ في الاتصال: {e}"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Username Checker")
        self.root.geometry("650x620")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)

        title = tk.Label(root, text="فاحص أسماء مستخدمي تيك توك",
                         font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#111")
        title.pack(pady=15)

        frame_in = tk.Frame(root, bg="#f5f5f5")
        frame_in.pack(pady=5, fill="x", padx=30)
        tk.Label(frame_in, text="أدخل اسم المستخدم:",
                 font=("Arial", 12), bg="#f5f5f5").pack(anchor="e")
        self.entry = tk.Entry(frame_in, font=("Arial", 13), justify="left")
        self.entry.pack(fill="x", pady=5, ipady=6)
        self.entry.bind("<Return>", lambda e: self.check_one())

        frame_btn = tk.Frame(root, bg="#f5f5f5")
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="فحص", command=self.check_one,
                  bg="#25D366", fg="white", font=("Arial", 11, "bold"),
                  padx=25, pady=8).pack(side="right", padx=5)
        tk.Button(frame_btn, text="مسح", command=self.clear_all,
                  bg="#999", fg="white", font=("Arial", 11, "bold"),
                  padx=25, pady=8).pack(side="right", padx=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14, "bold"),
                                     bg="#f5f5f5", wraplength=580)
        self.result_label.pack(pady=10)

        tk.Label(root, text="السجل:", font=("Arial", 11, "bold"),
                 bg="#f5f5f5").pack(anchor="e", padx=30)
        self.log = tk.Text(root, height=12, font=("Consolas", 10),
                           bg="white", fg="#333", borderwidth=1, relief="solid")
        self.log.pack(fill="both", padx=30, pady=5)
        self.log.configure(state="disabled")

        tk.Button(root, text="تصدير السجل", command=self.export_log,
                  bg="#007BFF", fg="white", font=("Arial", 10),
                  padx=15, pady=5).pack(pady=5)

        rules = ("القواعد: الطول 2-24 | الأحرف: a-z A-Z 0-9 _ . | "
                 "لا شرطة (-) | لا نقطة بداية/نهاية | لا نقطتين متتاليتين")
        tk.Label(root, text=rules, font=("Arial", 9), bg="#f5f5f5",
                 fg="#666", wraplength=580).pack(pady=10)

    def add_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def clear_all(self):
        self.entry.delete(0, "end")
        self.result_label.config(text="")
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def check_one(self):
        username = self.entry.get().strip().lstrip("@")
        if "tiktok.com/" in username:
            username = username.split("tiktok.com/")[-1].strip("/").split("?")[0]

        valid, msg = validate_format(username)
        if not valid:
            self.result_label.config(text=f"❌ {msg}", fg="red")
            self.add_log(f"[خطأ صيغة] {username} -> {msg}")
            return

        self.result_label.config(text="جاري الفحص...", fg="orange")
        self.root.update_idletasks()

        def run():
            ok, msg = check_availability(username)
            color = "green" if ok else ("red" if ok is False else "orange")
            self.result_label.config(text=f"@{username} -> {msg}", fg=color)
            self.add_log(f"@{username} -> {msg}")

        threading.Thread(target=run, daemon=True).start()

    def export_log(self):
        content = self.log.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("تنبيه", "السجل فارغ.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("تم", "تم التصدير بنجاح.")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
