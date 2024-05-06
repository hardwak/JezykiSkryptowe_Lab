import tkinter as tk
from tkinter import ttk, filedialog
from lab6 import SSHLogJournal
from ipaddress import AddressValueError
from datetime import datetime
from lab6.SSHLogEntry import SSHLogEntry_FailedPassword, SSHLogEntry_AcceptedPassword, SSHLogEntry_Other, \
    SSHLogEntry_Error


class MyLogBrowser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Log Browser")
        self.geometry("1000x500")

        self.widgets()

    def widgets(self):
        file_frame = ttk.Frame(self)
        file_frame.pack(padx=10, pady=5)

        # open button
        # ------------------------------------------------------------------
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(file_frame, textvariable=self.path_var, width=100, state='readonly')
        self.path_entry.pack(side='left', padx=5, pady=5)

        self.open_button = ttk.Button(file_frame, text="Open", command=self.load_logs, width=15)
        self.open_button.pack(side="right", padx=5, pady=5)
        # ------------------------------------------------------------------

        # logs list
        # ------------------------------------------------------------------
        list_and_nav_frame = ttk.Frame(self)
        list_and_nav_frame.pack(fill='x', padx=10, pady=5)

        list_frame = ttk.Frame(list_and_nav_frame)
        list_frame.pack(side='left', fill='x', expand=True, padx=1, pady=1)

        self.log_listbox = tk.Listbox(list_frame, height=15)
        self.log_listbox.pack(side='left', fill='both', expand=True)
        self.log_listbox.bind('<<ListboxSelect>>', self.show_details)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.log_listbox.yview)
        scrollbar.pack(side='left', fill='y')
        self.log_listbox.config(yscrollcommand=scrollbar.set)
        # ------------------------------------------------------------------

        # details list
        # ------------------------------------------------------------------
        nav_frame = ttk.Frame(list_frame)
        nav_frame.pack(side='right', fill='x', expand=False, padx=1, pady=1)

        self.log_info_label = tk.Label(list_frame, text="Log Info:", font=("Arial", 12, "bold"))
        self.log_info_label.pack(side='top', pady=10)

        self.log_info = tk.Text(list_frame, height=15, width=40)
        self.log_info.pack(side='right', padx=5)
        # ------------------------------------------------------------------

        # dates ,ips, navigation buttons
        # ------------------------------------------------------------------
        dates_frame = ttk.Frame(self)
        dates_frame.pack(fill='both', expand=False, padx=10, pady=5)

        ttk.Label(dates_frame, text="From date").pack(side="left")
        self.date_from = ttk.Entry(dates_frame)
        self.date_from.pack(side='left', padx=(5, 20))

        ttk.Label(dates_frame, text="To date").pack(side="left")
        self.date_to = ttk.Entry(dates_frame)
        self.date_to.pack(side='left', padx=(5, 20))

        ttk.Label(dates_frame, text="IP").pack(side="left")
        self.ip_box = ttk.Entry(dates_frame)
        self.ip_box.pack(side='left', padx=(5, 20))

        self.previous_button = tk.Button(dates_frame, text="Previous", command=self.prev_log)
        self.previous_button.pack(side='right', padx=5)

        self.next_button = tk.Button(dates_frame, text="Next", command=self.next_log)
        self.next_button.pack(side='right', padx=5)
        # ------------------------------------------------------------------

        # log type
        # ------------------------------------------------------------------
        message_frame = ttk.Frame(self)
        message_frame.pack(fill='both', expand=False, padx=10, pady=10)

        ttk.Label(message_frame, text="Message type").grid(row=0, column=0)

        message_type = tk.StringVar()
        self.message_types = ttk.Combobox(message_frame, textvariable=message_type)

        self.message_types['values'] = ("Failed Password", "Accepted Password", "Error", "Other")
        self.message_types.grid(row=0, column=1, padx=5)
        # ------------------------------------------------------------------

        # filter, refresh, clear buttons
        # ------------------------------------------------------------------
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill='both', expand=False, padx=10, pady=10)

        self.filter_button = ttk.Button(bottom_frame, text="Filter", command=self.filter_logs)
        self.filter_button.pack(side="left", padx=5, pady=5)

        self.reset_button = ttk.Button(bottom_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side="left", padx=5, pady=5)

        self.clear_button = ttk.Button(bottom_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side="left", padx=5, pady=5)
        # ------------------------------------------------------------------

    def filter_logs(self):
        ip_address = self.ip_box.get()
        filtered_journal = SSHLogJournal.SSHLogJournal()

        try:
            from_date = datetime.strptime(self.date_from.get(), '%b %d %H:%M:%S')
        except ValueError:
            from_date = None
        print(from_date)

        try:
            to_date = datetime.strptime(self.date_to.get(), '%b %d %H:%M:%S')
        except ValueError:
            to_date = None
        print(to_date)

        for entry in self.journal:
            if self.match_entry(entry, from_date, to_date, self.message_types.get()):
                filtered_journal.append(entry.raw_message)

        try:
            filtered_journal.journal = filtered_journal.find_by_ip(ip_address)
        except AddressValueError:
            pass

        self.journal = filtered_journal

        self.log_listbox.delete(0, tk.END)

        for entry in filtered_journal:
            self.log_listbox.insert(tk.END, entry.raw_message)

    def match_entry(self, entry, from_date, to_date, message_type):
        if from_date and entry.date < from_date:
            return False
        if to_date and entry.date > to_date:
            return False

        if message_type != "":
            if message_type == "Failed Password" and not isinstance(entry, SSHLogEntry_FailedPassword):
                return False
            elif message_type == "Accepted Password" and not isinstance(entry, SSHLogEntry_AcceptedPassword):
                return False
            elif message_type == "Error" and not isinstance(entry, SSHLogEntry_Error):
                return False
            elif message_type == "Other" and not isinstance(entry, SSHLogEntry_Other):
                return False

        return True

    def load_logs(self, event=None):
        self.journal = SSHLogJournal.SSHLogJournal()
        self.file_path = filedialog.askopenfilename()
        self.show_logs()

    def show_details(self, event=None):
        selection = self.log_listbox.curselection()
        if selection:
            index = selection[0]
            log_entry = self.journal.get(index)

            self.log_info.config(state='normal')
            self.log_info.delete('1.0', 'end')

            self.log_info.insert('end', f"Date : {log_entry.date.strftime('%b %d %H:%M:%S')}\n")
            self.log_info.insert('end', f"Name : {log_entry.name}\n")
            self.log_info.insert('end', f"PID : {log_entry.pid}\n")
            self.log_info.insert('end', f"IP : {log_entry.get_ip_v4_address()}")

            self.log_info.config(state='disabled')

    def prev_log(self):
        current_selection = self.log_listbox.curselection()
        if current_selection:
            index = current_selection[0]
            if index > 0:
                self.log_listbox.select_clear(index)
                self.log_listbox.select_set(index - 1)
                self.log_listbox.event_generate('<<ListboxSelect>>')

    def next_log(self):
        current_selection = self.log_listbox.curselection()
        if current_selection:
            index = current_selection[0]
            if index < self.log_listbox.size() - 1:
                self.log_listbox.select_clear(index)
                self.log_listbox.select_set(index + 1)
                self.log_listbox.event_generate('<<ListboxSelect>>')

    def reset(self, event=None):
        self.clear()
        self.show_logs()

    def clear(self, event=None):
        self.path_var.set("")
        self.date_from.delete(0, tk.END)
        self.date_to.delete(0, tk.END)
        self.ip_box.delete(0, tk.END)
        self.log_listbox.delete(0, tk.END)
        self.message_types.set('')

        self.log_info.config(state='normal')
        self.log_info.delete("1.0", tk.END)
        self.log_info.config(state='disabled')

    def show_logs(self, event=None):
        if self.file_path:
            self.path_var.set(self.file_path)
            with open(self.file_path, 'r') as file:
                logs = file.readlines()
                self.log_listbox.delete(0, tk.END)

                for log in logs:
                    log_entry = self.journal.append(log)
                    self.log_listbox.insert(tk.END, log_entry.raw_message)


if __name__ == "__main__":
    app = MyLogBrowser()
    app.mainloop()
