import tkinter as tk
from tkinter import font as tkfont
from nexus.config.settings import settings

COLORS = {
    'bg': '#0a0a0a',
    'fg': '#00ff41',
    'dim': '#008f11',
    'error': '#ff3333',
    'accent': '#00cc33',
    'input_bg': '#111111',
    'card_bg': '#111111',
    'border': '#1a1a1a',
}

class LoginScreen:
    def __init__(self, on_success):
        self.on_success = on_success
        self.password_visible = False
        self.root = tk.Tk()
        self.root.title('NEXUS Login')
        self.root.configure(bg=COLORS['bg'])
        self.root.resizable(False, False)
        width, height = 700, 520
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.font_title = tkfont.Font(family='Consolas', size=26, weight='bold')
        self.font_label = tkfont.Font(family='Consolas', size=11)
        self.font_input = tkfont.Font(family='Consolas', size=12)
        self.font_small = tkfont.Font(family='Consolas', size=9)
        self._build()

    def _build(self):
        main = tk.Frame(self.root, bg=COLORS['bg'])
        main.place(relx=0.5, rely=0.5, anchor='center')

        header = tk.Frame(main, bg=COLORS['bg'])
        header.pack(pady=(0, 20))
        tk.Label(header, text='N E X U S', font=self.font_title, bg=COLORS['bg'], fg=COLORS['fg']).pack()
        tk.Label(header, text='PORTABLE AI TERMINAL', font=self.font_label, bg=COLORS['bg'], fg=COLORS['dim']).pack(pady=(4, 0))

        card = tk.Frame(main, bg=COLORS['card_bg'], highlightbackground=COLORS['border'], highlightthickness=1)
        card.pack(padx=40, pady=10, fill='both', expand=True)

        tk.Label(card, text='AUTHENTICATION REQUIRED', font=self.font_label, bg=COLORS['card_bg'], fg=COLORS['fg']).pack(pady=(24, 16))

        users = settings.get_users()
        user_names = list(users.keys())

        user_frame = tk.Frame(card, bg=COLORS['card_bg'])
        user_frame.pack(pady=6, fill='x', padx=40)
        tk.Label(user_frame, text='USER', font=self.font_label, bg=COLORS['card_bg'], fg=COLORS['dim'], width=12, anchor='e').pack(side='left', padx=6)
        self.user_var = tk.StringVar(value=user_names[0] if user_names else '')
        self.user_menu = tk.OptionMenu(user_frame, self.user_var, *user_names)
        self.user_menu.config(font=self.font_input, bg=COLORS['input_bg'], fg=COLORS['fg'], relief='flat', highlightthickness=0, activebackground=COLORS['dim'], activeforeground=COLORS['bg'])
        self.user_menu.pack(side='left', padx=6, ipady=4, fill='x', expand=True)
        menu = self.user_menu['menu']
        menu.config(font=self.font_input, bg=COLORS['input_bg'], fg=COLORS['fg'], activebackground=COLORS['dim'], activeforeground=COLORS['bg'], relief='flat')

        pass_frame = tk.Frame(card, bg=COLORS['card_bg'])
        pass_frame.pack(pady=6, fill='x', padx=40)
        tk.Label(pass_frame, text='PASSWORD', font=self.font_label, bg=COLORS['card_bg'], fg=COLORS['dim'], width=12, anchor='e').pack(side='left', padx=6)
        self.pass_entry = tk.Entry(pass_frame, font=self.font_input, bg=COLORS['input_bg'], fg=COLORS['fg'], insertbackground=COLORS['fg'], relief='flat', show='*', width=20)
        self.pass_entry.pack(side='left', padx=6, ipady=6)
        self.eye_btn = tk.Button(pass_frame, text='[HIDE]', font=self.font_label, bg=COLORS['input_bg'], fg=COLORS['fg'], activebackground=COLORS['dim'], relief='flat', width=6, command=self._toggle_password)
        self.eye_btn.pack(side='left', padx=4)

        self.status_label = tk.Label(card, text='', font=self.font_label, bg=COLORS['card_bg'], fg=COLORS['error'])
        self.status_label.pack(pady=(12, 6))

        tk.Button(card, text='LOGIN', font=self.font_label, bg=COLORS['dim'], fg=COLORS['bg'], activebackground=COLORS['fg'], activeforeground=COLORS['bg'], relief='flat', padx=32, pady=8, command=self._login).pack(pady=16)

        tk.Label(card, text='', font=self.font_small, bg=COLORS['card_bg'], fg=COLORS['dim']).pack(pady=(0, 16))

        self.user_var.trace_add('write', lambda *args: self.pass_entry.focus_set())
        self.pass_entry.bind('<Return>', lambda e: self._login())
        self.pass_entry.focus_set()

    def _toggle_password(self):
        self.password_visible = not self.password_visible
        self.pass_entry.config(show='' if self.password_visible else '*')
        self.eye_btn.config(text='[SHOW]' if self.password_visible else '[HIDE]')

    def _login(self):
        username = self.user_var.get().strip()
        password = self.pass_entry.get().strip()
        if settings.verify_user(username, password):
            self.root.destroy()
            self.on_success(username)
        else:
            self.status_label.config(text='ACCESS DENIED')
            self.pass_entry.delete(0, 'end')

    def run(self):
        self.root.mainloop()
