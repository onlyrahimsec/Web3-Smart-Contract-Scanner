import customtkinter as ctk
from tkinter import filedialog, messagebox
import scanner
import os
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BG_COLOR      = "#000000"
CARD_COLOR    = "#0A0B10"
ACCENT_BLUE   = "#00D2FF" 
NEON_GREEN    = "#00FF87" 
CRITICAL_RED  = "#FF4B2B" 
TEXT_WHITE    = "#FFFFFF"

ctk.set_appearance_mode("dark")

class Web3ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WEB3 SMART AUDIT")
        self.geometry("1150x950")
        self.configure(fg_color=BG_COLOR)

        self.scan_results = []
        self.scanned_files = [] 
        self.selected_path = None

        self._build_ui()

    def _build_ui(self):
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, height=90, fg_color=BG_COLOR, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        
        ctk.CTkLabel(self.header_frame, text=" WEB3 SMART CONTRACT SCANNER ", 
                     font=("Segoe UI", 35, "bold"), text_color=ACCENT_BLUE).pack(pady=(20, 0))
        ctk.CTkLabel(self.header_frame, text="INDUSTRIAL SECURITY ANALYSIS", 
                     font=("Consolas", 12), text_color="#FFFFFF").pack(pady=(0, 10))

        # --- Main Container ---
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=40, pady=10)

        # 1. Target Acquisition Card
        self.target_card = ctk.CTkFrame(self.main_container, fg_color=CARD_COLOR, corner_radius=15, border_width=1, border_color="#1A1C25")
        self.target_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(self.target_card, text="[ TARGET ACQUISITION ]", font=("Consolas", 14, "bold"), text_color=ACCENT_BLUE).pack(pady=(15, 10))
        
        self.btn_row = ctk.CTkFrame(self.target_card, fg_color="transparent")
        self.btn_row.pack(pady=10)
        
        ctk.CTkButton(self.btn_row, text="📄 SELECT .SOL FILE", command=self.open_file, 
                      fg_color="#1A1C25", hover_color=ACCENT_BLUE, font=("Segoe UI", 13, "bold"), width=180).pack(side="left", padx=15)
        ctk.CTkButton(self.btn_row, text="📂 SELECT FOLDER", command=self.open_folder, 
                      fg_color="#1A1C25", hover_color=ACCENT_BLUE, font=("Segoe UI", 13, "bold"), width=180).pack(side="left", padx=15)
        
        self.path_label = ctk.CTkLabel(self.target_card, text="AWAITING TARGET...", font=("Segoe UI", 15, "bold"), text_color="#8B949E")
        self.path_label.pack(pady=(5, 15))

        # 2. Engine Selection
        self.engine_card = ctk.CTkFrame(self.main_container, fg_color=CARD_COLOR, corner_radius=15)
        self.engine_card.pack(fill="x", pady=10)
        
        self.engine_container = ctk.CTkFrame(self.engine_card, fg_color="transparent")
        self.engine_container.pack(expand=True)
        
        self.use_slither = ctk.BooleanVar(value=True)
        self.use_mythril = ctk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(self.engine_container, text="SLITHER (STATIC)", variable=self.use_slither, 
                        border_color=ACCENT_BLUE, text_color=TEXT_WHITE, font=("Segoe UI", 12, "bold")).pack(side="left", padx=30, pady=20)
        ctk.CTkCheckBox(self.engine_container, text="MYTHRIL (SYMBOLIC)", variable=self.use_mythril, 
                        border_color=ACCENT_BLUE, text_color=TEXT_WHITE, font=("Segoe UI", 12, "bold")).pack(side="left", padx=30, pady=20)

        # 3. Visualization
        self.graph_frame = ctk.CTkFrame(self.main_container, height=280, fg_color="transparent")
        self.graph_frame.pack(pady=10, fill="x")

        self.status_label = ctk.CTkLabel(self.main_container, text="", font=("Consolas", 16, "bold"))
        self.status_label.pack(pady=5)

        # 4. Action Buttons
        self.btn_scan = ctk.CTkButton(self.main_container, text="INITIATE SECURITY AUDIT", command=self.start_audit_thread, 
                                     fg_color=NEON_GREEN, text_color="#000", height=50, font=("Segoe UI", 16, "bold"), 
                                     hover_color="#00CC6A", width=500)
        self.btn_scan.pack(pady=10)

        self.btn_export = ctk.CTkButton(self.main_container, text="📥 EXPORT OFFICIAL AUDIT REPORT (PDF)", command=self.export_pdf, 
                                       state="disabled", fg_color=CRITICAL_RED, text_color="#FFF", height=45, 
                                       font=("Segoe UI", 14, "bold"), width=500)
        self.btn_export.pack(pady=5)

        # 5. Output Stream
        self.result_box = ctk.CTkTextbox(self.main_container, height=350, font=("Consolas", 12), 
                                        fg_color="#050505", text_color=NEON_GREEN, border_width=1, border_color="#1A1C25")
        self.result_box.pack(pady=15, fill="both")

    def open_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Solidity", "*.sol")])
        if self.selected_path: 
            self.path_label.configure(text=f"TARGET ➔ {os.path.basename(self.selected_path)}", text_color=ACCENT_BLUE)

    def open_folder(self):
        self.selected_path = filedialog.askdirectory()
        if self.selected_path: 
            self.path_label.configure(text=f"TARGET FOLDER ➔ {self.selected_path}", text_color=ACCENT_BLUE)

    def start_audit_thread(self):
        if not self.selected_path:
            messagebox.showwarning("Error", "Please select a target first!")
            return
        threading.Thread(target=self.start_audit, daemon=True).start()

    def start_audit(self):
        self.btn_scan.configure(state="disabled", text="AUDITING...")
        self.status_label.configure(text="🛰️ SCANNING IN PROGRESS...", text_color="#f1c40f")
        self.result_box.delete("1.0", "end")
        self.scan_results = []
        self.scanned_files = []
        
        files = [self.selected_path] if os.path.isfile(self.selected_path) else [os.path.join(self.selected_path, x) for x in os.listdir(self.selected_path) if x.endswith(".sol")]
        h, m, l = 0, 0, 0
        
        for f in files:
            f_name = os.path.basename(f)
            self.scanned_files.append(f_name)
            self.result_box.insert("end", f">>> ANALYZING: {f_name}\n")
            self.update()
            
            if self.use_slither.get():
                s_res = scanner.run_slither_scan(f)
                if s_res and 'results' in s_res:
                    for i in s_res['results'].get('detectors', []):
                        sev = str(i.get('impact', 'Info')).upper()
                        if "HIGH" in sev: h += 1
                        elif "MEDIUM" in sev: m += 1
                        else: l += 1
                        i['source'] = 'Slither'; i['file'] = f_name
                        self.scan_results.append(i)
            
            if self.use_mythril.get():
                m_res = scanner.run_mythril_scan(f)
                if m_res:
                    issues = m_res if isinstance(m_res, list) else m_res.get('issues', [])
                    for i in issues:
                        sev = str(i.get('severity', 'High')).upper()
                        if "HIGH" in sev: h += 1
                        elif "MEDIUM" in sev: m += 1
                        else: l += 1
                        self.scan_results.append({'check': i.get('title', 'Mythril Issue'), 'source': 'Mythril', 'file': f_name, 'impact': sev})
        
        self.status_label.configure(text="✅ AUDIT COMPLETE // DATA READY", text_color=NEON_GREEN)
        self.show_chart(h, m, l)
        self.display_dashboard_results()
        self.btn_export.configure(state="normal") 
        self.btn_scan.configure(state="normal", text="INITIATE SECURITY AUDIT")

    def display_dashboard_results(self):
        self.result_box.insert("end", "\n[!] ANALYSIS LOG:\n" + "="*30 + "\n")
        
        for file_name in self.scanned_files:
            file_issues = [i for i in self.scan_results if i.get('file') == file_name]
            self.result_box.insert("end", f"📂 [FILE: {file_name}]\n")
            
            if not file_issues:
                self.result_box.insert("end", "   ✅ No Vulnerabilities Detected\n\n")
            else:
                for issue in file_issues:
                    source = issue.get('source', 'Unknown')
                    name = issue.get('check')
                    details = scanner.get_vulnerability_details(name)
                    self.result_box.insert("end", f"   ▶ [{source}] {name}\n")
                    self.result_box.insert("end", f"     ↪ FIX: {details['fix']}\n\n")
        
        self.result_box.see("end")

    def show_chart(self, h, m, l):
        for w in self.graph_frame.winfo_children(): w.destroy()
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.bar(['CRITICAL', 'MEDIUM', 'STABLE'], [h, m, l], color=[CRITICAL_RED, '#F39C12', ACCENT_BLUE])
        ax.set_title("SECURITY THREAT POSTURE", color=TEXT_WHITE, fontweight='bold')
        ax.set_facecolor(CARD_COLOR)
        fig.patch.set_facecolor(CARD_COLOR)
        ax.tick_params(colors=TEXT_WHITE)
        plt.savefig("temp_graph.png")
        canvas_chart = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack()
        plt.close(fig)

    def export_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="WEB3_AUDIT_REPORT.pdf")
        if not file_path: return
        try:
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 24)
            c.drawString(60, 750, "Security Audit Report")
            c.setFont("Helvetica", 10)
            c.drawString(60, 730, "Generated by: WEB3 SMART AUDIT")
            c.line(60, 725, 550, 725)
            if os.path.exists("temp_graph.png"): c.drawImage("temp_graph.png", 60, 480, width=420, height=220)
            
            y = 450
            for file_name in self.scanned_files:
                if y < 100: c.showPage(); y = 750
                
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.blue)
                c.drawString(60, y, f"FILE: {file_name}")
                y -= 20
                
                file_issues = [i for i in self.scan_results if i.get('file') == file_name]
                
                if not file_issues:
                    c.setFont("Helvetica", 10)
                    c.setFillColor(colors.green)
                    c.drawString(75, y, "✅ No Vulnerabilities Detected")
                    y -= 30
                else:
                    for issue in file_issues:
                        if y < 80: c.showPage(); y = 750
                        name = issue.get('check')
                        source = issue.get('source', 'Unknown')
                        impact = str(issue.get('impact', 'INFO')).upper()
                        details = scanner.get_vulnerability_details(name)
                        
                        c.setFont("Helvetica-Bold", 10)
                        c.setFillColor(colors.red if "HIGH" in impact or "CRITICAL" in impact else colors.orange if "MEDIUM" in impact else colors.black)
                        c.drawString(75, y, f"[{impact}] {name} (via {source})")
                        y -= 15
                        
                        c.setFont("Helvetica", 9)
                        c.setFillColor(colors.black)
                        c.drawString(90, y, f"REMEDIATION: {details['fix']}")
                        y -= 25
                
                c.line(60, y+10, 500, y+10)
                y -= 15

            c.save()
            messagebox.showinfo("SUCCESS", "Report Exported!")
        except Exception as e: messagebox.showerror("ERROR", str(e))

if __name__ == "__main__":
    app = Web3ScannerApp()
    app.mainloop()
