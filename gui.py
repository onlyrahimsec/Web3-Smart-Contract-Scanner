import customtkinter as ctk
from tkinter import filedialog
import subprocess
import os

# থিম সেটআপ
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Web3 Smart Contract Vuln Scanner")
        self.geometry("800x600")

        # শিরোনাম
        self.label = ctk.CTkLabel(self, text="Web3 Smart Contract Vulnerability Scanner", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # ফাইল সিলেক্ট বাটন
        self.btn_select = ctk.CTkButton(self, text="Select Solidity File", command=self.open_file)
        self.btn_select.pack(pady=10)

        # ফাইল পাথ দেখানোর জন্য লেবেল
        self.path_label = ctk.CTkLabel(self, text="No file selected", font=("Arial", 12))
        self.path_label.pack()

        # স্ক্যান বাটন
        self.btn_scan = ctk.CTkButton(self, text="Start Scan", command=self.start_scan, fg_color="green", hover_color="darkgreen")
        self.btn_scan.pack(pady=20)

        # রেজাল্ট দেখানোর বক্স
        self.result_box = ctk.CTkTextbox(self, width=700, height=350)
        self.result_box.pack(pady=10)

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Solidity Files", "*.sol")])
        if filename:
            self.path_label.configure(text=filename)
            self.selected_file = filename

    def start_scan(self):
        if hasattr(self, 'selected_file'):
            self.result_box.delete("1.0", "end")
            self.result_box.insert("end", "Scanning in progress... Please wait...\n")
            self.update()

            # ফাইলটির ডিরেক্টরি এবং নাম আলাদা করা
            file_dir = os.path.dirname(self.selected_file)
            file_name = os.path.basename(self.selected_file)

            # ডকার কমান্ড (Slither)
            cmd = f'docker run -v "{file_dir}":/share trailofbits/eth-security-toolbox slither /share/{file_name}'
            
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                output, _ = process.communicate()
                self.result_box.delete("1.0", "end")
                self.result_box.insert("end", output)
            except Exception as e:
                self.result_box.insert("end", f"Error: {str(e)}")
        else:
            self.result_box.insert("end", "Error: Please select a .sol file first!")

if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()