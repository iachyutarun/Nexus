import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
import os
import time
from nexus.config.settings import settings
from nexus.ai.engine import AIEngine
from nexus.commands.history import add_history
from nexus.core.utils import get_models_dir

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

class TerminalUI:
    def __init__(self, username):
        self.username = username
        self.display_name = username.upper()
        self.root = tk.Tk()
        self.root.title(f'NEXUS - {self.display_name}')
        self.root.configure(bg=COLORS['bg'])
        self.root.state('zoomed')
        self.font_mono = tkfont.Font(family='Consolas', size=11)
        self.font_bold = tkfont.Font(family='Consolas', size=11, weight='bold')
        self.font_title = tkfont.Font(family='Consolas', size=16, weight='bold')
        self.font_small = tkfont.Font(family='Consolas', size=9)
        self.ai = AIEngine(output_callback=self._display, confirm_callback=self._confirm)
        self.history = []
        self.history_index = -1
        self.demo_mode = False
        self._build()
        self._welcome()

    def _build(self):
        main = tk.Frame(self.root, bg=COLORS['bg'])
        main.pack(fill='both', expand=True)

        header = tk.Frame(main, bg=COLORS['bg'], height=70)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=COLORS['bg'])
        title_frame.pack(side='left', padx=20, pady=8)
        tk.Label(title_frame, text='N E X U S', font=self.font_title, bg=COLORS['bg'], fg=COLORS['fg']).pack(anchor='w')
        tk.Label(title_frame, text='AI COMMAND TERMINAL', font=self.font_small, bg=COLORS['bg'], fg=COLORS['dim']).pack(anchor='w')

        info_frame = tk.Frame(header, bg=COLORS['bg'])
        info_frame.pack(side='right', padx=20, pady=8)

        user_switch_frame = tk.Frame(info_frame, bg=COLORS['bg'])
        user_switch_frame.pack(side='right', padx=12)
        tk.Label(user_switch_frame, text='SWITCH USER:', font=self.font_small, bg=COLORS['bg'], fg=COLORS['dim']).pack(side='left', padx=4)
        users = settings.get_users()
        self.user_var = tk.StringVar(value=self.username)
        user_menu = tk.OptionMenu(user_switch_frame, self.user_var, *users.keys(), command=self._switch_user)
        user_menu.config(font=self.font_small, bg=COLORS['input_bg'], fg=COLORS['fg'], relief='flat', highlightthickness=0, activebackground=COLORS['dim'], activeforeground=COLORS['bg'])
        user_menu.pack(side='left', padx=4)
        menu = user_menu['menu']
        menu.config(font=self.font_small, bg=COLORS['input_bg'], fg=COLORS['fg'], activebackground=COLORS['dim'], activeforeground=COLORS['bg'], relief='flat')

        model_frame = tk.Frame(info_frame, bg=COLORS['bg'])
        model_frame.pack(side='right', padx=12)
        tk.Label(model_frame, text='MODEL:', font=self.font_small, bg=COLORS['bg'], fg=COLORS['dim']).pack(side='left', padx=4)
        self.model_status_label = tk.Label(model_frame, text=self.ai.get_engine_name(), font=self.font_small, bg=COLORS['bg'], fg=COLORS['fg'])
        self.model_status_label.pack(side='left', padx=4)
        tk.Button(model_frame, text='BROWSE', font=self.font_small, bg=COLORS['input_bg'], fg=COLORS['fg'], activebackground=COLORS['dim'], relief='flat', padx=8, pady=2, command=self._browse_model).pack(side='left', padx=4)
        tk.Button(model_frame, text='OFF', font=self.font_small, bg=COLORS['input_bg'], fg=COLORS['error'], activebackground=COLORS['dim'], relief='flat', padx=8, pady=2, command=self._model_off).pack(side='left', padx=4)

        tk.Label(info_frame, text=f'MODE: TEXT', font=self.font_small, bg=COLORS['bg'], fg=COLORS['dim']).pack(side='right', padx=12)
        tk.Label(info_frame, text=f'AI: {self.ai.get_engine_name()}', font=self.font_small, bg=COLORS['bg'], fg=COLORS['dim']).pack(side='right', padx=12)
        tk.Label(info_frame, text=f'USER: {self.display_name}', font=self.font_small, bg=COLORS['bg'], fg=COLORS['dim']).pack(side='right', padx=12)

        self.output = tk.Text(main, font=self.font_mono, bg=COLORS['bg'], fg=COLORS['fg'], insertbackground=COLORS['fg'], relief='flat', wrap='word', state='disabled', padx=12, pady=12)
        self.output.pack(fill='both', expand=True, padx=8, pady=(0, 8))

        input_frame = tk.Frame(main, bg=COLORS['bg'], height=44)
        input_frame.pack(fill='x', side='bottom', padx=8, pady=(0, 8))
        input_frame.pack_propagate(False)

        self.prompt_label = tk.Label(input_frame, text=f'{self.display_name}:', font=self.font_bold, bg=COLORS['bg'], fg=COLORS['fg'])
        self.prompt_label.pack(side='left')

        self.input_entry = tk.Entry(input_frame, font=self.font_mono, bg=COLORS['input_bg'], fg=COLORS['fg'], insertbackground=COLORS['fg'], relief='flat')
        self.input_entry.pack(side='left', fill='x', expand=True, padx=(8, 0), ipady=4)
        self.input_entry.bind('<Return>', self._on_enter)
        self.input_entry.bind('<Up>', self._on_up)
        self.input_entry.bind('<Down>', self._on_down)

        self.root.bind('<Configure>', lambda e: None)

    def _switch_user(self, new_user):
        if new_user == self.username:
            return
        self.username = new_user
        self.display_name = new_user.upper()
        self.root.title(f'NEXUS - {self.display_name}')
        self.prompt_label.config(text=f'{self.display_name}:')
        self.history = []
        self.history_index = -1
        self._display(f'--- Switched to user: {self.display_name} ---')
        self._display('')
        self._update_model_status()

    def _browse_model(self):
        initial_dir = get_models_dir()
        if not os.path.isdir(initial_dir):
            initial_dir = os.path.expanduser('~')
        path = filedialog.askopenfilename(
            title='Select GGUF Model',
            initialdir=initial_dir,
            filetypes=[('GGUF Model', '*.gguf'), ('All Files', '*.*')]
        )
        if path:
            result = self.ai.enable_local_model(path)
            self._update_model_status()
            self._display(f'Model loaded: {result}')
            self._display(f'Path: {path}')

    def _model_off(self):
        result = self.ai.disable_local_model()
        self._update_model_status()
        self._display(f'Model switched: {result}')

    def _update_model_status(self):
        name = self.ai.get_engine_name()
        self.model_status_label.config(text=name)

    def _display(self, text):
        self.output.config(state='normal')
        if text == '__CLEAR__':
            self.output.delete('1.0', 'end')
        else:
            self.output.insert('end', text + '\n')
        self.output.see('end')
        self.output.config(state='disabled')

    def _confirm(self, prompt):
        self._display(prompt)
        self.root.update()
        self.input_entry.config(state='normal')
        self.input_entry.focus_set()
        self._confirm_mode = True
        self._confirm_var = tk.StringVar()
        self.input_entry.config(textvariable=self._confirm_var)
        self.input_entry.bind('<Return>', self._on_confirm_return)
        self.input_entry.wait_variable(self._confirm_var)
        self.input_entry.unbind('<Return>')
        self.input_entry.config(textvariable=None, state='normal')
        self._confirm_mode = False
        val = self._confirm_result
        del self._confirm_result
        return val

    def _on_confirm_return(self, event):
        val = self.input_entry.get().strip().lower()
        self._confirm_result = val in ('yes', 'y', 'ok', 'confirm')
        self.input_entry.delete(0, 'end')
        self._confirm_var.set('done')

    def _on_up(self, event):
        if not self.history:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, self.history[self.history_index])

    def _on_down(self, event):
        if not self.history:
            return
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, self.history[self.history_index])
        else:
            self.history_index = -1
            self.input_entry.delete(0, 'end')

    def _on_enter(self, event):
        text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, 'end')
        self.history.insert(0, text)
        self.history_index = -1
        self._display(f'{self.display_name}: {text}')
        add_history(text, self.username)
        if self.demo_mode and text.lower() == 'exit':
            self.demo_mode = False
            self._display('\nEXHIBITION MODE ENDED\n')
            return
        result = self.ai.process(text, username=self.username)
        if result == '__CLEAR__':
            self._display('__CLEAR__')
        elif result == '__LOGOUT__':
            self.root.destroy()
        elif result == '__DEMO__':
            self._run_demo()
        else:
            self._display(f'NEXUS:\n{result}')
        self._display('')

    def _welcome(self):
        self._display('====================================================')
        self._display('N E X U S')
        self._display('AI COMMAND TERMINAL')
        self._display('')
        self._display(f'USER: {self.display_name}')
        self._display('MODE: TEXT')
        self._display(f'AI: {self.ai.get_engine_name()}')
        self._display('STORAGE: USB')
        self._display('---')
        self._display('')
        self.input_entry.focus_set()

    def _run_demo(self):
        self.demo_mode = True
        self._display('========================================')
        self._display('     NEXUS EXHIBITION MODE')
        self._display('========================================')
        self._display('')
        self._display('AUTHENTICATION       [PASS]')
        self._display('COMMAND ENGINE       [READY]')
        self._display(f'AI ENGINE            [{self.ai.get_engine_name()}]')
        self._display('USB STORAGE          [ONLINE]')
        self._display('TEXT INTERFACE       [READY]')
        self._display('')
        self._display('========================================')
        self._display('')
        self._display(f'{self.display_name}: status')
        self._display(self.ai.process('status', username=self.username))
        self._display('')
        self._display(f'{self.display_name}: What can you do?')
        self._display("NEXUS:\nI can answer supported questions, perform calculations, manage notes, inspect approved system information, and operate my built-in tools.")
        self._display('')
        self._display(f"Type 'exit' to leave exhibition mode.")

    def run(self):
        self.root.mainloop()
