import asyncio
import json
import os
import hashlib
import threading
import time
import uuid
import re
import shutil
import webbrowser
import pandas as pd
from datetime import datetime
import customtkinter as ctk
from telethon import TelegramClient, functions, types
from telethon.errors import SessionPasswordNeededError, InviteHashExpiredError, InviteHashInvalidError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from tkinter import messagebox, filedialog
import os
if not os.path.exists("sessions"):
    os.makedirs("sessions")

GITHUB_URL = "https://github.com/wlzcaq-crypto/CYBER-CORE-Professional-Telegram-PARSER-Marketing-Tool"
TELEGRAM_URL = "https://t.me/bulatovt77"

# --- Константы оформления ---
BTN_DEFAULT = ("#D3D3D3", "gray25")
BTN_ACCENT = ("#A9A9A9", "#1f538d")
TEXT_COLOR = ("black", "white")

LANG_DATA = {
    "RU": {
        "title": "CYBER CORE v10.0",
        "parser": "ПАРСЕР",
        "inviter": "ИНВАЙТЕР",
        "mailer": "РАССЫЛКА",
        "settings": "НАСТРОЙКИ",
        "connect": "ПОДКЛЮЧИТЬ",
        "save": "СОХРАНИТЬ",
        "start": "ЗАПУСТИТЬ",
        "pause": "ПАУЗА",
        "resume": "ПРОДОЛЖИТЬ",
        "stop": "ЗАВЕРШИТЬ",
        "status_dev": "МОДУЛЬ В РАЗРАБОТКЕ",
        "pw_wrong": "Неверный пароль. Попыток: ",
        "locked": "БЛОКИРОВКА: ",
        "err_join": "Ошибка входа в чат: ",
        "err_entity": "Чат не найден или недоступен",
        "forgot": "Забыли пароль?",
        "reset_full": "ПОЛНЫЙ СБРОС (УДАЛИТЬ ВСЁ)",
        "use_secret": "ОТВЕТИТЬ НА ВОПРОС",
        "theme_lab": "Тема:",
        "lang_lab": "Язык:",
        "collected": "Собрано человек: ",
        "copy_btn": "Копировать",
        "excel_btn": "В Excel",
        "txt_btn": "В TXT",
        "updates": "ОБНОВЛЕНИЯ",
        "help": "ИНСТРУКЦИЯ",
        "tos_btn": "СОГЛАШЕНИЕ",
        "github": "GITHUB",
        "telegram": "TELEGRAM"
    },
    "EN": {
        "title": "CYBER CORE v10.0",
        "parser": "PARSER",
        "inviter": "INVITER",
        "mailer": "MAILER",
        "settings": "SETTINGS",
        "connect": "CONNECT",
        "save": "SAVE",
        "start": "START",
        "status_dev": "UNDER DEVELOPMENT",
        "pw_wrong": "Wrong password. Attempts: ",
        "locked": "LOCKED: ",
        "err_join": "Join error: ",
        "err_entity": "Chat not found or inaccessible",
        "forgot": "Forgot Password?",
        "reset_full": "HARD RESET (DELETE ALL)",
        "use_secret": "SECRET QUESTION",
        "theme_lab": "Theme:",
        "lang_lab": "Language:",
        "collected": "Collected: ",
        "copy_btn": "Copy",
        "excel_btn": "To Excel",
        "txt_btn": "To TXT",
        "updates": "UPDATES",
        "help": "GUIDE",
        "tos_btn": "TOS",
        "github": "GITHUB",
        "telegram": "TELEGRAM"
    }
}

TOS_TEXT = """ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ И ОГРАНИЧЕНИЕ ОТВЕТСТВЕННОСТИ (EULA)



1. ПРЕДОСТАВЛЕНИЕ "КАК ЕСТЬ". Данное ПО предоставляется без каких-либо гарантий. Автор не несет ответственности за ошибки или сбои.

2. ПОЛНЫЙ ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ. Разработчик не отвечает за любой ущерб (материальный, репутационный или технический), возникший в ходе использования ПО.

3. БЕЗОПАСНОСТЬ АККАУНТОВ. Использование автоматизации нарушает правила Telegram. Вы осознаете риск полной и безвозвратной блокировки ваших аккаунтов.

4. ОТСУТСТВИЕ СБОРА ДАННЫХ. Автор не собирает ваши API Hash, сессии или номера. Всё хранится локально. Ответственность за кражу этих данных с вашего ПК лежит на вас.

5. ЗАКОННОСТЬ ДЕЙСТВИЙ. Вы обязуетесь не использовать ПО для нарушения законов вашей страны и международного права.

6. ПЕРСОНАЛЬНЫЕ ДАННЫЕ ТРЕТЬИХ ЛИЦ. Сбор (парсинг) данных пользователей является вашей инициативой. Вы берете на себя ответственность за хранение и использование этих баз в рамках GDPR и ФЗ-152.

7. ОТСУТСТВИЕ ПОДДЕРЖКИ. Автор не обязан предоставлять обновления или исправления.

8. ПРАВО НА ИЗМЕНЕНИЯ. Разработчик может изменять функционал ПО без уведомления.

9. РИСКИ АВТОМАТИЗАЦИИ. Любое действие ПО имитирует действия человека, но не гарантирует защиту от алгоритмов антифлуда Telegram.

10. ЗАПРЕТ НА РЕВЕРС-ИНЖИНИРИНГ. Запрещено вскрывать код ПО для создания вредоносных модификаций.

11. КОСВЕННЫЕ УБЫТКИ. Автор не возмещает убытки от упущенной выгоды в результате работы софта.

12. ПРИВАТНЫЕ ЧАТЫ. Парсинг приватных чатов без разрешения их владельцев является этическим нарушением, за которое отвечает только пользователь.

13. СТОРОННИЕ БИБЛИОТЕКИ. ПО использует Telethon. Все ограничения данной библиотеки распространяются и на это ПО.

14. ОТВЕТСТВЕННОСТЬ ЗА СПАМ. Автор категорически против спам-рассылок. Ответственность за использование модуля Mailer лежит на пользователе.

15. ИНТЕЛЛЕКТУАЛЬНАЯ СОБСТВЕННОСТЬ. Названия и логотипы Telegram принадлежат Telegram FZ-LLC.

16. СРОК ДЕЙСТВИЯ. Соглашение вступает в силу с момента запуска ПО.

17. ТЕРРИТОРИЯ ИСПОЛЬЗОВАНИЯ. Пользователь сам следит за легальностью ПО в своей юрисдикции.

18. ПОЛНОЕ СОГЛАСИЕ. Нажатие "Принять" означает ваш отказ от любых судебных исков к автору.

19. ПЕРЕДАЧА ПО. При передаче ПО третьим лицам вы обязаны уведомить их об этом соглашении.

20. ФОРС-МАЖОР. Автор не отвечает за работу API Telegram и их изменения."""

HELP_TEXT = """ИНСТРУКЦИЯ ПО ЭКСПЛУАТАЦИИ CYBER CORE:



1. НАСТРОЙКА API:

   - Создайте приложение на my.telegram.org.

   - Скопируйте API ID и Hash в верхнюю панель.



2. ПАРСИНГ ПУБЛИЧНЫХ ЧАТОВ:

   - Вставьте ссылку вида @username или t.me/username.



3. ПАРСИНГ ПРИВАТНЫХ ЧАТОВ:

   - Если у вас есть ссылка-приглашение (t.me/+ABC... или t.me/joinchat/...), просто вставьте её в поле "Ссылка".

   - Если аккаунт уже состоит в чате, программа автоматически начнет сбор без повторного вступления.

   - ВАЖНО: Программа сама вступит в чат по ссылке, если там не требуется ручное подтверждение администратором (заявка).



4. РЕЖИМЫ:

   - "Участники": Парсит всех видимых людей.

   - "Комментарии": Собирает тех, кто писал под последними постами (эффективно для каналов).



5. ГОРЯЧИЕ КЛАВИШИ:

   - Enter: переход между полями и быстрый запуск."""

UPDATES_TEXT = """
🚀 РЕЛИЗ CYBER CORE v10.0 [OFFICIAL RELEASE]

Добро пожаловать в первую версию профессионального инструмента для автоматизации работы в Telegram. 

✅ ЧТО ДОБАВЛЕНО В ТЕКУЩЕЙ ВЕРСИИ:

1. ЯДРО СИСТЕМЫ:
   - Полная интеграция с библиотекой Telethon.
   - Поддержка асинхронности для стабильной работы без фризов интерфейса.
   - Система безопасного хранения сессий в папке /sessions.

2. МОДУЛЬ ПАРСИНГА (Parser):
   - Сбор участников из публичных чатов.
   - Уникальный алгоритм сбора пользователей из КОММЕНТАРИЕВ каналов (позволяет достать активную аудиторию).
   - Поддержка вступления в приватные чаты по инвайт-ссылкам (t.me/+...).
   - Фильтрация дубликатов в реальном времени.

3. УПРАВЛЕНИЕ ДАННЫМИ:
   - Мгновенный экспорт результатов в форматы Excel (.xlsx) и TXT.
   - Функция копирования всей базы в буфер обмена одной кнопкой.

4. ИНТЕРФЕЙС И ЮЗАБИЛИТИ:
   - Современный UI на базе CustomTkinter с поддержкой Dark/Light тем.
   - Система профилей: сохраняйте данные разных аккаунтов и переключайтесь между ними в два клика.
   - Интерактивный терминал (Log Monitor) для отслеживания действий программы.
   - Двуязычный интерфейс (RU / EN).

---

🛠 В СЛЕДУЮЩИХ ОБНОВЛЕНИЯХ:

- [ ] МОДУЛЬ INVITER: Массовое добавление собранной аудитории в ваши группы.
- [ ] МОДУЛЬ MAILER: Рассылка личных сообщений с поддержкой рандомизации текста (SpinTax).
- [ ] MULTI-ACCOUNTING: Работа одновременно с 10+ аккаунтами.
- [ ] FILTER: Очистка базы от "ботов" и тех, кто давно не был в сети.
- [ ] PROXY: Поддержка HTTP/SOCKS5 прокси для защиты от банов.

Благодарим за использование Cyber Core! Следите за историей обновлений в этом разделе.
"""


class CyberCoreV10(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config_file = "config_v10.json"
        self.profiles_file = "profiles_v10.json"
        self.load_config()

        ctk.set_appearance_mode(self.config.get("theme", "Dark"))
        self.lang = self.config.get("lang", "RU")

        self.client = None
        self.parsed_data = []
        self.is_parsing = False
        self.is_paused = False

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()

        self.title(LANG_DATA[self.lang]["title"])
        self.geometry("1200x850")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if not self.config.get("tos_accepted", False):
            self.withdraw()
            self.show_tos_window()
        else:
            self.init_main_ui()

    def show_tos_window(self):
        tos_win = ctk.CTkToplevel()
        tos_win.title("Соглашение")
        tos_win.geometry("700x650")
        tos_win.protocol("WM_DELETE_WINDOW", self.on_closing)
        tos_win.attributes("-topmost", True)

        ctk.CTkLabel(tos_win, text="ЮРИДИЧЕСКИЙ ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ", font=("Arial", 18, "bold")).pack(pady=10)

        txt = ctk.CTkTextbox(tos_win, width=650, height=450)
        txt.pack(pady=10)
        txt.insert("1.0", TOS_TEXT)
        txt.configure(state="disabled")

        btn_f = ctk.CTkFrame(tos_win, fg_color="transparent")
        btn_f.pack(pady=10)

        def accept():
            self.config["tos_accepted"] = True
            self.save_config()
            tos_win.destroy()
            self.deiconify()
            self.init_main_ui()

        ctk.CTkButton(btn_f, text="Я ПРИНИМАЮ ВСЕ РИСКИ И УСЛОВИЯ", fg_color="green", command=accept, width=300,
                      height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="ВЫХОД", fg_color="red", command=self.on_closing).pack(side="left", padx=10)

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def init_main_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self.main_container, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.render_sidebar()

        self.top_bar = ctk.CTkFrame(self.main_container, height=60)
        self.top_bar.grid(row=0, column=1, sticky="new", padx=20, pady=10)

        self.prof_selector = ctk.CTkOptionMenu(self.top_bar, values=["Новый"], command=self.on_profile_load)
        self.prof_selector.pack(side="left", padx=10)

        self.api_id = ctk.CTkEntry(self.top_bar, placeholder_text="API ID", width=100)
        self.api_id.pack(side="left", padx=5)
        self.api_id.bind("<Return>", lambda e: self.api_hash.focus())

        self.api_hash = ctk.CTkEntry(self.top_bar, placeholder_text="API Hash", width=150)
        self.api_hash.pack(side="left", padx=5)
        self.api_hash.bind("<Return>", lambda e: self.phone.focus())

        self.phone = ctk.CTkEntry(self.top_bar, placeholder_text="Phone")
        self.phone.pack(side="left", padx=5)
        self.phone.bind("<Return>", lambda e: asyncio.run_coroutine_threadsafe(self.tg_connect(), self.loop))

        ctk.CTkButton(self.top_bar, text=LANG_DATA[self.lang]["connect"],
                      command=lambda: asyncio.run_coroutine_threadsafe(self.tg_connect(), self.loop)).pack(side="left",
                                                                                                           padx=5)
        ctk.CTkButton(self.top_bar, text=LANG_DATA[self.lang]["save"], fg_color="green",
                      command=self.save_profile_data).pack(side="left", padx=5)

        self.main_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=(80, 20))

        self.monitor = ctk.CTkTextbox(self.main_area, height=150, fg_color="black", text_color="#00FF41",
                                      font=("Consolas", 12))
        self.monitor.pack(side="bottom", fill="x", pady=(0, 10))

        self.stats_label = ctk.CTkLabel(self.main_area, text=f"{LANG_DATA[self.lang]['collected']} 0",
                                        font=("Arial", 14, "bold"))
        self.stats_label.pack(side="bottom", pady=5)

        self.content = ctk.CTkFrame(self.main_area)
        self.content.pack(fill="both", expand=True)

        self.load_profiles_to_menu()
        self.set_tab("Parser")

    def render_sidebar(self):
        for w in self.sidebar.winfo_children(): w.destroy()
        ctk.CTkLabel(self.sidebar, text="⚡ CORE", font=("Consolas", 26, "bold")).pack(pady=20)

        # Фикс ошибки ValueError: используем проверку темы вместо кортежа с transparent
        current_theme = self.config.get("theme", "Dark")
        bg_btn = "transparent" if current_theme == "Dark" else "#E0E0E0"

        tabs = [("Parser", "parser"), ("Inviter", "inviter"), ("Mailer", "mailer"), ("Settings", "settings")]
        for name, key in tabs:
            ctk.CTkButton(self.sidebar, text=LANG_DATA[self.lang][key], command=lambda n=name: self.set_tab(n),
                          fg_color=bg_btn, text_color=TEXT_COLOR).pack(fill="x", padx=10, pady=5)

        bottom_menu = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_menu.pack(side="bottom", fill="x", pady=20)

        ctk.CTkButton(bottom_menu, text=LANG_DATA[self.lang]["telegram"], fg_color="#229ED9",
                      command=lambda: webbrowser.open(TELEGRAM_URL)).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(bottom_menu, text=LANG_DATA[self.lang]["github"], fg_color="#333",
                      command=lambda: webbrowser.open(GITHUB_URL)).pack(fill="x", padx=10, pady=2)

        for tab_name, lang_key in [("Updates", "updates"), ("Help", "help"), ("TOS", "tos_btn")]:
            ctk.CTkButton(bottom_menu, text=LANG_DATA[self.lang][lang_key], command=lambda n=tab_name: self.set_tab(n),
                          fg_color="gray25", height=30).pack(fill="x", padx=10, pady=2)

    def set_tab(self, name):
        for w in self.content.winfo_children(): w.destroy()
        if name == "Parser":
            ctk.CTkLabel(self.content, text=LANG_DATA[self.lang]["parser"], font=("Arial", 20, "bold")).pack(pady=10)
            target = ctk.CTkEntry(self.content, placeholder_text="Ссылка на чат / @username", width=400)
            target.pack(pady=5)
            limit = ctk.CTkEntry(self.content, placeholder_text="Лимит (0 - все)", width=400)
            limit.pack(pady=5)
            mode = ctk.CTkSegmentedButton(self.content, values=["Участники", "Комментарии"])
            mode.set("Участники")
            mode.pack(pady=10)

            target.bind("<Return>", lambda e: limit.focus())
            limit.bind("<Return>", lambda e: asyncio.run_coroutine_threadsafe(
                self.start_parsing_logic(target.get(), int(limit.get() or 0), mode.get()), self.loop))

            self.start_btn = ctk.CTkButton(self.content, text=LANG_DATA[self.lang]["start"], height=40, width=200,
                                           command=lambda: asyncio.run_coroutine_threadsafe(
                                               self.start_parsing_logic(target.get(), int(limit.get() or 0),
                                                                        mode.get()), self.loop))
            self.start_btn.pack(pady=20)
        elif name == "Settings":
            self.render_settings()
        elif name == "Updates":
            self.render_text_tab("ОБНОВЛЕНИЯ", UPDATES_TEXT)
        elif name == "Help":
            self.render_text_tab("ИНСТРУКЦИЯ", HELP_TEXT)
        elif name == "TOS":
            self.render_text_tab("СОГЛАШЕНИЕ", TOS_TEXT)
        else:
            ctk.CTkLabel(self.content, text=LANG_DATA[self.lang]["status_dev"], font=("Arial", 16),
                         text_color="orange").pack(expand=True)

    async def start_parsing_logic(self, url, limit, mode):
        if not self.client:
            self.log("ОШИБКА: Сначала подключите аккаунт!")
            return

        self.parsed_data = []
        self.is_parsing = True
        self.is_paused = False
        self.update_stats(0)
        self.show_process_ui()

        target_clean = url.strip()
        if "t.me/" in target_clean: target_clean = target_clean.split("/")[-1]

        try:
            entity = await self.client.get_entity(target_clean)
        except:
            if not await self.join_chat(url):
                self.log(LANG_DATA[self.lang]["err_entity"])
                self.stop_parsing_process()
                return
            entity = await self.client.get_entity(target_clean)

        users_set = set()
        try:
            if mode == "Участники":
                async for user in self.client.iter_participants(entity, limit=limit):
                    while self.is_paused: await asyncio.sleep(0.5)
                    if not self.is_parsing: break
                    if user.username:
                        u_name = f"@{user.username}"
                        if u_name not in users_set:
                            users_set.add(u_name)
                            self.parsed_data.append((u_name, str(user.id)))
                            self.update_stats(len(users_set))
                            self.log(f"Найдено: {u_name}")

            elif mode == "Комментарии":
                async for message in self.client.iter_messages(entity, limit=50):
                    if not self.is_parsing: break
                    if message.replies:
                        try:
                            async for reply in self.client.iter_messages(entity, reply_to=message.id):
                                while self.is_paused: await asyncio.sleep(0.5)
                                if not self.is_parsing: break
                                if reply.sender and getattr(reply.sender, 'username', None):
                                    u_name = f"@{reply.sender.username}"
                                    if u_name not in users_set:
                                        users_set.add(u_name)
                                        self.parsed_data.append((u_name, str(reply.sender.id)))
                                        self.update_stats(len(users_set))
                                        self.log(f"Найдено (коммент): {u_name}")
                                        if limit > 0 and len(users_set) >= limit: break
                        except:
                            continue

            self.log(f"Завершено! Всего: {len(users_set)}")
            self.show_results_panel()
        except Exception as e:
            self.log(f"Ошибка: {e}")
        finally:
            self.stop_parsing_process()

    # --- Вспомогательные методы UI ---
    def show_process_ui(self):
        self.after(0, self._render_process_buttons)

    def _render_process_buttons(self):
        self.start_btn.pack_forget()
        self.process_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.process_frame.pack(pady=20)
        self.pause_btn = ctk.CTkButton(self.process_frame, text=LANG_DATA[self.lang]["pause"], width=100,
                                       command=self.toggle_pause)
        self.pause_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(self.process_frame, text=LANG_DATA[self.lang]["stop"], fg_color="red", width=120,
                                      command=self.confirm_stop)
        self.stop_btn.pack(side="left", padx=5)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_btn.configure(
            text=LANG_DATA[self.lang]["resume"] if self.is_paused else LANG_DATA[self.lang]["pause"])

    def confirm_stop(self):
        if messagebox.askyesno("Завершение", "Показать текущий результат?"):
            self.is_parsing = False

    def stop_parsing_process(self):
        self.is_parsing = False
        self.after(0, self._restore_start_ui)

    def _restore_start_ui(self):
        if hasattr(self, 'process_frame'): self.process_frame.destroy()
        self.start_btn.pack(pady=20)

    def show_results_panel(self):
        self.after(0, self._render_results_panel)

    def _render_results_panel(self):
        res_win = ctk.CTkToplevel(self)
        res_win.title("Результаты")
        res_win.geometry("600x600")
        res_win.attributes("-topmost", True)
        txt_area = ctk.CTkTextbox(res_win, width=560, height=400)
        txt_area.pack(pady=10, padx=20)
        txt_area.insert("1.0", "\n".join([u[0] for u in self.parsed_data]))
        btn_f = ctk.CTkFrame(res_win, fg_color="transparent")
        btn_f.pack(pady=10)
        ctk.CTkButton(btn_f, text=LANG_DATA[self.lang]["copy_btn"], command=self.copy_to_clipboard, width=120).pack(
            side="left", padx=5)
        ctk.CTkButton(btn_f, text=LANG_DATA[self.lang]["excel_btn"], fg_color="green", command=self.export_to_excel,
                      width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_f, text=LANG_DATA[self.lang]["txt_btn"], fg_color="gray30", command=self.export_to_txt,
                      width=120).pack(side="left", padx=5)

    def render_text_tab(self, title, text_content):
        ctk.CTkLabel(self.content, text=title, font=("Arial", 20, "bold")).pack(pady=10)
        txt = ctk.CTkTextbox(self.content, width=600, height=400)
        txt.pack(pady=10, padx=20, fill="both", expand=True)
        txt.insert("1.0", text_content)
        txt.configure(state="disabled")

    def render_settings(self):
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(scroll, text=LANG_DATA[self.lang]["settings"], font=("Arial", 22, "bold")).pack(pady=10)

        f1 = ctk.CTkFrame(scroll)
        f1.pack(fill="x", pady=5)
        ctk.CTkLabel(f1, text=LANG_DATA[self.lang]["theme_lab"]).pack(side="left", padx=10)
        ctk.CTkSegmentedButton(f1, values=["Light", "Dark"], command=self.ui_change_theme).pack(side="right", padx=10)

        f2 = ctk.CTkFrame(scroll)
        f2.pack(fill="x", pady=5)
        ctk.CTkLabel(f2, text=LANG_DATA[self.lang]["lang_lab"]).pack(side="left", padx=10)
        seg_lang = ctk.CTkSegmentedButton(f2, values=["RU", "EN"], command=self.ui_change_lang)
        seg_lang.set(self.lang)
        seg_lang.pack(side="right", padx=10)

    # --- Логика Данных ---
    def ui_change_lang(self, v):
        self.lang = v
        self.config["lang"] = v
        self.save_config()
        self.title(LANG_DATA[self.lang]["title"])
        self.render_sidebar()
        self.set_tab("Settings")

    def ui_change_theme(self, v):
        self.config["theme"] = v
        self.save_config()
        ctk.set_appearance_mode(v)
        self.render_sidebar()

    async def tg_connect(self):
        try:
            ph = self.phone.get().strip()
            self.client = TelegramClient(f"sessions/{ph}", int(self.api_id.get()), self.api_hash.get(), loop=self.loop)
            await self.client.connect()
            if not await self.client.is_user_authorized():
                await self.client.send_code_request(ph)
                self.log("Код отправлен!")
            else:
                self.log("Аккаунт подключен")
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def on_profile_load(self, name):
        p = self.safe_load_json(self.profiles_file, {}).get(name)
        if p:
            self.api_id.delete(0, 'end');
            self.api_id.insert(0, str(p['api_id']))
            self.api_hash.delete(0, 'end');
            self.api_hash.insert(0, p['api_hash'])
            self.phone.delete(0, 'end');
            self.phone.insert(0, p['phone'])

    def save_profile_data(self):
        ph = self.phone.get()
        if ph:
            p = self.safe_load_json(self.profiles_file, {})
            p[ph] = {"api_id": self.api_id.get(), "api_hash": self.api_hash.get(), "phone": ph}
            with open(self.profiles_file, "w") as f: json.dump(p, f)
            self.load_profiles_to_menu()
            self.log(f"Профиль {ph} сохранен")

    def load_profiles_to_menu(self):
        p = self.safe_load_json(self.profiles_file, {})
        self.prof_selector.configure(values=list(p.keys()) + ["Новый"])

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {"tos_accepted": False, "theme": "Dark", "lang": "RU"}

    def save_config(self):
        with open(self.config_file, "w") as f: json.dump(self.config, f)

    def safe_load_json(self, path, default):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return default

    def log(self, msg):
        self.after(0, lambda: (self.monitor.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n"),
                               self.monitor.see("end")))

    async def join_chat(self, target):
        try:
            target = target.strip().replace("@", "")
            if "t.me/" in target: target = target.split("/")[-1]
            if "joinchat/" in target or "+" in target:
                hash_chat = target.split('/')[-1].replace('+', '')
                await self.client(ImportChatInviteRequest(hash_chat))
            else:
                await self.client(JoinChannelRequest(target))
            return True
        except:
            return False

    def on_closing(self):
        try:
            self.loop.call_soon_threadsafe(self.loop.stop)
        except:
            pass
        self.quit();
        self.destroy()

    def update_stats(self, count):
        self.after(0, lambda: self.stats_label.configure(text=f"{LANG_DATA[self.lang]['collected']} {count}"))

    def copy_to_clipboard(self):
        self.clipboard_clear();
        self.clipboard_append("\n".join([u[0] for u in self.parsed_data]));
        self.log("Скопировано")

    def export_to_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f: f.write("\n".join([u[0] for u in self.parsed_data]))

    def export_to_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if path: pd.DataFrame(self.parsed_data, columns=["Username", "ID"]).to_excel(path, index=False)


if __name__ == "__main__":
    if not os.path.exists("sessions"): os.makedirs("sessions")
    app = CyberCoreV10()
    app.mainloop()