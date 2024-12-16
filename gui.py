import tkinter as tk
from tkinter import filedialog, messagebox
from steg import AudioSteganography


class StegGUI:
    """
    A Tkinter-based GUI to interact with the AudioSteganography class.
    Allows user to choose between 'hide' and 'extract' modes,
    select files, and either embed or extract a message.
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Audio Steganography")

        # Instance of our steganography logic class
        self.steg = AudioSteganography()

        # Mode: hide or extract
        self.mode_var = tk.StringVar(value="hide")

        # Radio buttons for mode selection
        self.hide_radio = tk.Radiobutton(master, text="Hide Message", variable=self.mode_var,
                                         value="hide", command=self.toggle_mode)
        self.extract_radio = tk.Radiobutton(master, text="Extract Message", variable=self.mode_var,
                                            value="extract", command=self.toggle_mode)
        self.hide_radio.grid(row=0, column=0, padx=10, pady=10)
        self.extract_radio.grid(row=0, column=1, padx=10, pady=10)

        # Input file selection (for either mode)
        tk.Label(master, text="Input WAV:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.input_entry = tk.Entry(master, width=50)
        self.input_entry.grid(row=1, column=1, padx=5, pady=5)
        self.input_browse = tk.Button(master, text="Browse", command=self.browse_input)
        self.input_browse.grid(row=1, column=2, padx=5, pady=5)

        # Output file selection (for hide mode only)
        self.output_label = tk.Label(master, text="Output WAV:")
        self.output_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.output_entry = tk.Entry(master, width=50)
        self.output_entry.grid(row=2, column=1, padx=5, pady=5)
        self.output_browse = tk.Button(master, text="Browse", command=self.browse_output)
        self.output_browse.grid(row=2, column=2, padx=5, pady=5)

        # Message text (for hide mode only)
        self.message_label = tk.Label(master, text="Message:")
        self.message_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.message_text = tk.Text(master, width=50, height=5)
        self.message_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Extracted message display (for extract mode)
        self.extracted_label = tk.Label(master, text="Extracted Message:")
        self.extracted_text = tk.Text(master, width=50, height=5, state='disabled')

        # Action button
        self.action_button = tk.Button(master, text="Hide Message", command=self.execute_action)
        self.action_button.grid(row=4, column=1, pady=10)

        self.toggle_mode()

    def toggle_mode(self):
        """Enable/disable fields depending on mode (hide or extract)."""
        mode = self.mode_var.get()
        if mode == "hide":
            # Show fields for hiding
            self.output_label.grid()
            self.output_entry.grid()
            self.output_browse.grid()
            self.message_label.grid()
            self.message_text.grid()
            self.extracted_label.grid_remove()
            self.extracted_text.grid_remove()

            self.action_button.config(text="Hide Message")
        else:
            # Show fields for extracting
            self.output_label.grid_remove()
            self.output_entry.grid_remove()
            self.output_browse.grid_remove()
            self.message_label.grid_remove()
            self.message_text.grid_remove()

            self.extracted_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
            self.extracted_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
            self.extracted_text.config(state='disabled')

            self.action_button.config(text="Extract Message")

    def browse_input(self):
        """Open file dialog to select input WAV."""
        filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)

    def browse_output(self):
        """Open file dialog to select output WAV."""
        filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def execute_action(self):
        """Perform the hide or extract action based on the chosen mode."""
        mode = self.mode_var.get()
        input_path = self.input_entry.get().strip()

        if not input_path:
            messagebox.showerror("Error", "Please select an input file.")
            return

        if mode == "hide":
            output_path = self.output_entry.get().strip()
            message = self.message_text.get("1.0", tk.END).strip()

            if not output_path:
                messagebox.showerror("Error", "Please select an output file.")
                return
            if not message:
                messagebox.showerror("Error", "Please enter a message.")
                return

            try:
                self.steg.hide_message(input_path, output_path, message)
                messagebox.showinfo("Success", f"Message hidden successfully in {output_path}!")
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