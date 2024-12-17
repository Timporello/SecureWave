import tkinter as tk
from tkinter import filedialog, messagebox
from steg import AudioSteganography
from analysis import AudioAnalysis


class StegGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Steganography")

        self.steg = AudioSteganography()
        self.analysis = AudioAnalysis()

        self.mode_var = tk.StringVar(value="hide")

        # ========== Configure root window grid ==========
        self.master.rowconfigure(0, weight=0)  # Mode selection
        self.master.rowconfigure(1, weight=0)  # Input frame
        self.master.rowconfigure(2, weight=1)  # Message/Extracted frame
        self.master.rowconfigure(3, weight=0)  # Buttons frame
        self.master.columnconfigure(0, weight=1)

        # ========== Frame: Mode selection ==========
        mode_frame = tk.Frame(self.master)
        mode_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.hide_radio = tk.Radiobutton(mode_frame, text="Hide Message", variable=self.mode_var,
                                         value="hide", command=self.toggle_mode)
        self.extract_radio = tk.Radiobutton(mode_frame, text="Extract Message", variable=self.mode_var,
                                            value="extract", command=self.toggle_mode)

        self.hide_radio.pack(side="left", padx=(0, 20))
        self.extract_radio.pack(side="left")

        # ========== Frame: Input and Save ==========
        input_frame = tk.Frame(self.master)
        input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        tk.Label(input_frame, text="Input audio:").grid(row=0, column=0, sticky='e', padx=10, pady=5)
        self.input_entry = tk.Entry(input_frame)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.input_browse = tk.Button(input_frame, text="Browse", command=self.browse_input)
        self.input_browse.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Save as button (for hide mode)
        self.save_button = tk.Button(input_frame, text="Save as", command=self.save_as)

        # ========== Frame: Message/Extracted Text ==========
        # We'll create both frames and show/hide them depending on the mode
        self.hide_frame = tk.Frame(self.master)
        self.hide_frame.columnconfigure(0, weight=0)
        self.hide_frame.columnconfigure(1, weight=1)
        self.hide_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.message_label = tk.Label(self.hide_frame, text="Message:")
        self.message_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.message_text = tk.Text(self.hide_frame, wrap="word")
        self.message_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.hide_frame.rowconfigure(0, weight=1)

        self.extract_frame = tk.Frame(self.master)
        self.extract_frame.columnconfigure(0, weight=0)
        self.extract_frame.columnconfigure(1, weight=1)
        self.extract_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.extracted_label = tk.Label(self.extract_frame, text="Extracted Message:")
        self.extracted_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.extracted_text = tk.Text(self.extract_frame, wrap="word", state='disabled')
        self.extracted_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.extract_frame.rowconfigure(0, weight=1)

        # ========== Frame: Action Buttons ==========
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=0)

        self.action_button = tk.Button(button_frame, text="Hide Message", command=self.execute_action)
        self.action_button.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.spectrogram_button = tk.Button(button_frame, text="Show Spectrogram", command=self.show_spectrogram)
        self.spectrogram_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Hold the chosen output path when "Save as" is clicked
        self.output_path = None

        self.toggle_mode()

    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "hide":
            # Show hide mode widgets
            self.save_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")
            self.hide_frame.grid()
            self.extract_frame.grid_remove()

            self.action_button.config(text="Hide Message")
        else:
            # Show extract mode widgets
            self.save_button.grid_remove()
            self.extract_frame.grid()
            self.hide_frame.grid_remove()

            self.action_button.config(text="Extract Message")

    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", ("*.wav", "*.mp3", "*.m4a", "*.flac", "*.ogg", "*.aac", "*.wma", "*.webm")),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def save_as(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[
                ("Audio Files", ("*.wav", "*.mp3", "*.m4a", "*.flac", "*.ogg", "*.aac", "*.wma", "*.webm")),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.output_path = filename

    def execute_action(self):
        mode = self.mode_var.get()
        input_path = self.input_entry.get().strip()

        if not input_path:
            messagebox.showerror("Error", "Please select an input file.")
            return

        if mode == "hide":
            if not self.output_path:
                messagebox.showerror("Error", "Please choose a location to save the output file.")
                return

            message = self.message_text.get("1.0", tk.END).strip()

            if not message:
                messagebox.showerror("Error", "Please enter a message.")
                return

            try:
                self.steg.hide_message(input_path, self.output_path, message)
                messagebox.showinfo("Success", f"Message hidden successfully in {self.output_path}!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        else:
            try:
                extracted = self.steg.extract_message(input_path)
                self.extracted_text.config(state='normal')
                self.extracted_text.delete("1.0", tk.END)
                self.extracted_text.insert(tk.END, extracted)
                self.extracted_text.config(state='disabled')
                messagebox.showinfo("Success", "Message extracted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def show_spectrogram(self):
        input_path = self.input_entry.get().strip()
        if not input_path:
            messagebox.showerror("Error", "Please select an input file for spectral analysis.")
            return
        try:
            self.analysis.show_spectrogram(input_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate spectrogram: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StegGUI(root)
    root.mainloop()