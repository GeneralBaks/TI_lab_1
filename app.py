from tkinter import (
    Tk, END, Menu, Label, Entry, StringVar, Radiobutton,
    Button, Frame, messagebox, filedialog
)
from enum import Enum
from typing import Final
import platform
from global_val import CYRILLIC, NUMBERS, ENGLISH_LEN
from logic import (
    gcd, cipher_decimation, cipher_vigenere,
    decipher_vigenere, decipher_decimation
)


class CipherMethod(Enum):
    DECIMATION = "Метод децимации"
    VIGENERE = "Алгоритм Виженера"


class App:
    MAX_DECIMATION_KEY_LEN: Final[int] = 7
    MAX_VIGENERE_KEY_LEN: Final[int] = 20

    __slots__ = ("main_form",
                 "f_in", "f_sel", "f_btns",
                 "file_menu", "main_menu",
                 "entry_key", "entry_plane_text", "entry_ciphered_text",
                 "lbl_key", "lbl_plane_text",
                 "lbl_ciphered_text", "lbl_encription_method",
                 "encription_method",
                 "rbtn_decimation", "rbtn_vigenere",
                 "btn_cipher", "btn_decipher",
                 "validate_decimation_key", "validate_vigenere_key")

    def __init__(self) -> None:
        self._init_main_form()
        self._init_selection_cipher()
        self._init_input_field()
        self._init_menu()
        self._init_buttons()

    def _init_main_form(self) -> None:
        self.main_form = Tk()
        self.main_form.title("Шифрование")
        self.main_form.geometry("1000x400")
        self.main_form.resizable(False, False)
        if platform.system() == "Windows":
            self.main_form.attributes("-toolwindow", True)

        self.main_form.columnconfigure(0, weight=3)
        self.main_form.columnconfigure(1, weight=1)

    def _init_menu(self) -> None:
        self.file_menu = Menu(self.main_form, tearoff=0)
        self.file_menu.add_command(label="Сохранить", command=self._on_save_file)
        self.file_menu.add_command(label="Открыть", command=self._on_open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выйти", command=self._on_exit)

        self.main_menu = Menu(self.main_form)
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_form.config(menu=self.main_menu)

    def _init_input_field(self) -> None:
        self.f_in = Frame(self.main_form)
        self.f_in.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.f_in.columnconfigure(1, weight=1)

        self.lbl_key = Label(self.f_in, text="Ключ:")
        self.lbl_key.grid(row=0, column=0, sticky="w", pady=10)

        self.entry_key = Entry(self.f_in, validate="key")
        self.entry_key.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.lbl_plane_text = Label(self.f_in, text="Исходный Текст:")
        self.lbl_plane_text.grid(row=1, column=0, sticky="w", pady=10)
        self.entry_plane_text = Entry(self.f_in)
        self.entry_plane_text.grid(row=1, column=1, sticky="ew", padx=(10, 0))

        self.lbl_ciphered_text = Label(self.f_in, text="Результат:")
        self.lbl_ciphered_text.grid(row=2, column=0, sticky="w", pady=10)
        self.entry_ciphered_text = Entry(self.f_in, state="readonly")
        self.entry_ciphered_text.grid(row=2, column=1, sticky="ew", padx=(10, 0))

    def _init_selection_cipher(self) -> None:
        self.f_sel = Frame(self.main_form)
        self.f_sel.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        self.encription_method = StringVar(value=CipherMethod.DECIMATION.value)

        self.lbl_encription_method = Label(
            self.f_sel, text="Способ шифрования:", font=("Arial", 10, "bold")
        )
        self.lbl_encription_method.pack(anchor="w", pady=(0, 10))

        self.rbtn_decimation = Radiobutton(
            self.f_sel, text=CipherMethod.DECIMATION.value, value=CipherMethod.DECIMATION.value,
            variable=self.encription_method, command=self._on_change_method
        )
        self.rbtn_decimation.pack(anchor="w")

        self.rbtn_vigenere = Radiobutton(
            self.f_sel, text=CipherMethod.VIGENERE.value, value=CipherMethod.VIGENERE.value,
            variable=self.encription_method, command=self._on_change_method
        )
        self.rbtn_vigenere.pack(anchor="w")

    def _init_buttons(self) -> None:
        f_btns = Frame(self.main_form)
        f_btns.grid(row=1, column=0, columnspan=2, pady=20)

        self.btn_cipher = Button(f_btns, text="Шифровать", width=15, command=self._on_cipher)
        self.btn_cipher.pack(side="left", padx=10)

        self.btn_decipher = Button(f_btns, text="Дешифровать", width=15, command=self._on_decipher)
        self.btn_decipher.pack(side="left", padx=10)

    def _get_valid_key(self, text: str) -> str:
        allowed_chars: str
        if self.encription_method.get() == CipherMethod.DECIMATION.value:
            allowed_chars = NUMBERS
        else:
            allowed_chars = CYRILLIC

        return "".join(c for c in text.lower() if c in allowed_chars)

    @property
    def key(self) -> str:
        text: str = self.entry_key.get().strip()
        return self._get_valid_key(text)

    @property
    def plane_text(self) -> str:
        return self.entry_plane_text.get()

    @plane_text.setter
    def plane_text(self, string: str) -> None:
        self.entry_plane_text.delete(0, END)
        self.entry_plane_text.insert(0, string)

    @property
    def ciphered_text(self) -> str:
        return self.entry_ciphered_text.get()

    @ciphered_text.setter
    def ciphered_text(self, string: str) -> None:
        self.entry_ciphered_text.config(state="normal")
        self.entry_ciphered_text.delete(0, END)
        self.entry_ciphered_text.insert(0, string)
        self.entry_ciphered_text.config(state="readonly")

    def _on_change_method(self) -> None:
        self._clear_all_entries()

    def _on_cipher(self) -> None:
        key = self.key
        if not key:
            messagebox.showwarning("Внимание", "Введите ключ для шифровки.")
            return

        text = self.plane_text
        if not text:
            messagebox.showwarning("Внимание", "Введите текст для шифровки.")
            return

        res_str: str
        if self.encription_method.get() == CipherMethod.VIGENERE.value:
            res_str = cipher_vigenere(text, key)
        else:
            step = int(key)

            if gcd(ENGLISH_LEN, step) != 1:
                messagebox.showerror(
                    "Ошибка",
                    f"НОД({ENGLISH_LEN}, {step}) должен быть равен 1.\n"
                    f"Ключ {step} не подходит для шифрования."
                )
                return

            res_str = cipher_decimation(text, step)

        self.ciphered_text = res_str

    def _on_decipher(self) -> None:
        key = self.key
        if not key:
            messagebox.showwarning("Внимание", "Введите ключ для дешифровки.")
            return

        text = self.plane_text
        if not text:
            messagebox.showwarning("Внимание", "Введите текст для дешифровки.")
            return

        res_str: str
        if self.encription_method.get() == CipherMethod.VIGENERE.value:
            res_str = decipher_vigenere(text, key)
        else:
            step = int(key)

            if gcd(ENGLISH_LEN, step) != 1:
                messagebox.showerror(
                    "Ошибка",
                    f"НОД({ENGLISH_LEN}, {step}) должен быть равен 1!\n"
                    f"Невозможно дешифровать с ключом {step}."
                )
                return

            res_str = decipher_decimation(text, step)

        self.ciphered_text = res_str

    def _on_exit(self) -> None:
        self.main_form.destroy()

    def _read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def _on_open_file(self) -> None:
        path: str = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*")]
        )
        if not path:
            return

        try:
            text: str = self._read_file(path)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден.")
            return
        except PermissionError:
            messagebox.showerror("Ошибка", "Нет прав на чтение.")
            return
        except UnicodeDecodeError:
            messagebox.showerror("Ошибка", "Неверная кодировка файла.")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка: {e}")
            return

        self.plane_text = text

    def _on_save_file(self) -> None:
        text: str = self.ciphered_text
        if not text:
            return

        path: str = filedialog.asksaveasfilename(
            confirmoverwrite=False,
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*")]
        )
        if not path:
            return

        try:
            with open(path, "w") as file:
                file.write(text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Возникла ошибка при записи в файл: {e}")
            return

    def _clear_all_entries(self) -> None:
        self.entry_key.config(validate="none")
        self.entry_key.delete(0, END)
        self.entry_key.config(validate="key")
        self.entry_plane_text.delete(0, END)
        self.entry_ciphered_text.config(state="normal")
        self.entry_ciphered_text.delete(0, END)
        self.entry_ciphered_text.config(state="readonly")

    def run(self):
        self.main_form.mainloop()
