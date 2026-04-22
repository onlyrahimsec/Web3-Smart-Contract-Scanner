import customtkinter as ctk
from tkinter import filedialog, messagebox
import scanner
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Theme Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Web3ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Web3 Smart Contract Scanner")
        self.geometry("1100x900")
        self.scan_results = []
        self.selected_path = None

        # UI Header
        ctk.CTkLabel(self, text="🛡️ Web3 Smart Contract Scanner", font=("Arial", 28, "bold")).pack(pady=20)
        
        # File/Folder Selection
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)
        ctk.CTkButton(self.btn_frame, text="📄 Select File", command=self.open_file).pack(side="left", padx=10)
        ctk.CTkButton(self.btn_frame, text="📂 Select Folder", command=self.open_folder).pack(side="left", padx=10)
        
        self.path_label = ctk.CTkLabel(self, text="No path selected", font=("Arial", 11))
        self.path_label.pack(pady=5)

        # Engine Selection Checkboxes
        self.tool_frame = ctk.CTkFrame(self)
        self.tool_frame.pack(pady=10)
        self.use_slither = ctk.BooleanVar(value=True)
        self.use_mythril = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tool_frame, text="Slither (Fast)", variable=self.use_slither).pack(side="left", padx=20)
        ctk.CTkCheckBox(self.tool_frame, text="Mythril (Deep Scan)", variable=self.use_mythril).pack(side="left", padx=20)

        # Graph Area
        self.graph_frame = ctk.CTkFrame(self, height=250, fg_color="transparent")
        self.graph_frame.pack(pady=10, fill="x", padx=100)

        # Control Buttons
        self.btn_scan = ctk.CTkButton(self, text="🚀 Run Audit", command=self.start_audit, fg_color="green", height=45, font=("Arial", 16, "bold"))
        self.btn_scan.pack(pady=10)

        self.btn_export = ctk.CTkButton(self, text="📥 Export PDF Report", command=self.export_pdf, state="disabled", fg_color="blue")
        self.btn_export.pack(pady=5)

        # Result Box
        self.result_box = ctk.CTkTextbox(self, width=1000, height=300, font=("Segoe UI Emoji", 12))
        self.result_box.pack(pady=15, padx=20)

    def open_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Solidity", "*.sol")])
        if self.selected_path:
            self.path_label.configure(text=self.selected_path)
            self.btn_export.configure(state="disabled")

    def open_folder(self):
        self.selected_path = filedialog.askdirectory()
        if self.selected_path:
            self.path_label.configure(text=f"Folder: {self.selected_path}")
            self.btn_export.configure(state="disabled")

    def start_audit(self):
        if not self.selected_path:
            messagebox.showwarning("Warning", "Select file or folder first!")
            return

        self.result_box.delete("1.0", "end")
        self.scan_results = []
        files_to_scan = []

        if os.path.isdir(self.selected_path):
            for root, _, files in os.walk(self.selected_path):
                for file in files:
                    if file.endswith(".sol"):
                        files_to_scan.append(os.path.join(root, file))
        else:
            files_to_scan.append(self.selected_path)

        self.result_box.insert("end", f"🔍 Audit Started on {len(files_to_scan)} file(s)...\n")
        self.update()

        h, m, l = 0, 0, 0
        for f in files_to_scan:
            f_name = os.path.basename(f)
            self.result_box.insert("end", f"🛠️ Auditing: {f_name}...\n")
            self.update()
            
            # --- Slither Scan ---
            if self.use_slither.get():
                s_res = scanner.run_slither_scan(f)
                if s_res and 'results' in s_res:
                    for i in s_res.get('results', {}).get('detectors', []):
                        sev = str(i.get('impact', 'Info')).upper()
                        i['source'] = 'Slither'
                        i['file'] = f_name
                        if "HIGH" in sev: h += 1
                        elif "MEDIUM" in sev: m += 1
                        else: l += 1
                        self.scan_results.append(i)

            # --- Mythril Scan (Universal Fix) ---
            if self.use_mythril.get():
                self.result_box.insert("end", f"   ⏳ Mythril analysis on {f_name}...\n")
                self.update()
                m_res = scanner.run_mythril_scan(f)
                
                if m_res:
                    # Mythril returns a list of issues
                    issues_list = m_res if isinstance(m_res, list) else m_res.get('issues', [])
                    
                    for issue in issues_list:
                        # Map severity/impact from various possible keys
                        raw_sev = issue.get('severity', issue.get('impact', 'High'))
                        sev = str(raw_sev).upper()
                        title = issue.get('title', issue.get('description', 'Mythril Vulnerability'))
                        
                        if "HIGH" in sev: h += 1
                        elif "MEDIUM" in sev: m += 1
                        else: l += 1
                        
                        self.scan_results.append({
                            'impact': sev, 
                            'check': title,
                            'source': 'Mythril', 
                            'file': f_name
                        })

        self.show_chart(h, m, l)
        self.display_text_results()
        if self.scan_results:
            self.btn_export.configure(state="normal")

    def show_chart(self, h, m, l):
        for widget in self.graph_frame.winfo_children(): widget.destroy()
        
        # If no issues found, provide a clean display
        if h == 0 and m == 0 and l == 0:
            ctk.CTkLabel(self.graph_frame, text="✅ No Vulnerabilities Found", font=("Arial", 16)).pack(pady=50)
            return

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.bar(['High', 'Medium', 'Low/Info'], [h, m, l], color=['#e74c3c', '#f39c12', '#3498db'])
        ax.set_title("Vulnerability Distribution", color='white')
        ax.tick_params(colors='white')
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        canvas_chart = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack()
        plt.close(fig)

    def display_text_results(self):
        self.result_box.insert("end", "\n" + "="*60 + "\n✅ Audit Complete!\n" + "="*60 + "\n\n")
        if not self.scan_results:
            self.result_box.insert("end", "🛡️ No significant vulnerabilities detected.\n")
            return

        for issue in self.scan_results:
            v_type = issue.get('check', 'Unknown')
            details = scanner.get_vulnerability_details(v_type)
            self.result_box.insert("end", f"📍 {issue.get('file')}: [{issue.get('impact')}] {v_type} (via {issue.get('source')})\n")
            self.result_box.insert("end", f"   Fix: {details['fix']}\n\n")

    def export_pdf(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Audit_Report.pdf",
            title="Save Audit Report"
        )
        if not file_path: return

        try:
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(100, 750, "Web3 Smart Contract Scanner Report")
            c.setFont("Helvetica", 12)
            c.drawString(100, 725, f"Source: {self.path_label.cget('text')}")
            c.drawString(100, 710, f"Total Vulnerabilities: {len(self.scan_results)}")
            c.line(100, 700, 500, 700)
            
            y = 670
            for issue in self.scan_results:
                if y < 100: c.showPage(); y = 750
                c.setFont("Helvetica-Bold", 11)
                c.drawString(100, y, f"[{issue.get('impact').upper()}] {issue.get('check')} ({issue.get('file')})")
                y -= 25
            c.save()
            messagebox.showinfo("Success", f"Report saved at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save PDF: {e}")

if __name__ == "__main__":
    app = Web3ScannerApp()
    app.mainloop()
