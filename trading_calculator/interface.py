import customtkinter as ctk
from trading_calculator.calculations import (
    calculate_asset_amount,
    calculate_trade_result,
    get_leverage_value,
)
from os.path import join
from .resource_path import get_resource_path
from PIL import Image, ImageTk

class TradingCalculator:
    CURRENCY_SYMBOLS = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }

    def __init__(self):
        self._setup_window()
        self._setup_fonts()
        self._setup_variables()
        self._load_images()
        self._create_widgets()
        self._setup_layout()

    def _setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Simple Profit/Loss Calculator")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.configure(fg_color="#0a0a0a")

        icon_path = get_resource_path(join("Assets", "icon.ico"))
        self.window_icon = ImageTk.PhotoImage(file=icon_path)
        self.window.wm_iconbitmap()
        self.window.iconphoto(False, self.window_icon)

    def _setup_fonts(self):
        self.font_family = "Segoe UI"
        self.bold11 = ctk.CTkFont(family=self.font_family, size=11, weight="bold")
        self.bold12 = ctk.CTkFont(family=self.font_family, size=12, weight="bold")
        self.bold13 = ctk.CTkFont(family=self.font_family, size=13, weight="bold")

    def _setup_variables(self):
        self.current_currency = ctk.StringVar(value="USD")

    def _load_images(self):
        config_path = get_resource_path(join("Assets", "config.png"))
        config_icon = Image.open(config_path)
        self.config_icon = config_icon.resize((20, 20))

    def _create_text_box(self, placeholder="") -> ctk.CTkEntry:
        return ctk.CTkEntry(
            master=self.window,
            placeholder_text=placeholder,
            corner_radius=6,
            width=150,
            height=30,
            font=self.bold11,
            justify="center",
            text_color="#C0C0C0",
            fg_color="#000000",
            border_width=1,
            border_color="#404040",
        )

    def _create_option_menu(self, values: list, default_value: str) -> ctk.CTkOptionMenu:
        return ctk.CTkOptionMenu(
            master=self.window,
            command=lambda x: None,
            values=values,
            width=150,
            height=30,
            corner_radius=6,
            dropdown_font=self.bold11,
            font=self.bold11,
            anchor="center",
            text_color="#C0C0C0",
            fg_color="#000000",
            button_color="#000000",
            button_hover_color="#000000",
            dropdown_fg_color="#000000",
        )

    def _create_widgets(self):
        self.frame_operation_size = ctk.CTkFrame(self.window, fg_color="transparent")

        self.label_entry_price = ctk.CTkLabel(self.window, text="Entry Price:", font=self.bold12)
        self.label_exit_price = ctk.CTkLabel(self.window, text="Exit Price:", font=self.bold12)
        self.label_operation_size = ctk.CTkLabel(self.frame_operation_size, text="Operation Size:", font=self.bold12)
        self.label_leverage = ctk.CTkLabel(self.window, text="Leverage:", font=self.bold12)
        self.label_operation_type  = ctk.CTkLabel(self.window, text="Operation Type:", font=self.bold12)

        self.entry_entry_price = self._create_text_box("Example: 100.5")
        self.entry_exit_price = self._create_text_box("Example: 110.75")
        self.entry_operation_size = self._create_text_box("Example: 1000")

        self.leverage_menu = self._create_option_menu(
            ["None", "10x", "20x", "30x", "50x", "100x"],
            "None"
        )
        self.operation_type_menu = self._create_option_menu(
            ["Buy", "Sell"],
            "Buy"
        )

        self.config_button = ctk.CTkButton(
            self.frame_operation_size,
            text="",
            width=15,
            height=15,
            command=self._open_config,
            image=ctk.CTkImage(light_image=self.config_icon, dark_image=self.config_icon, size=(14, 14)),
            fg_color="transparent",
            hover_color="#1a1a1a"
        )

        self.calculate_button = ctk.CTkButton(
            self.window,
            text="Calculate",
            command=self._calculate,
            font=self.bold13
        )
        self.result_label = ctk.CTkLabel(
            self.window,
            text="",
            font=self.bold11,
            wraplength=300
        )

    def _setup_layout(self):
        self.label_entry_price.pack(pady=5)
        self.entry_entry_price.pack(pady=5)
        self.label_exit_price.pack(pady=5)
        self.entry_exit_price.pack(pady=5)
        
        self.frame_operation_size.pack(pady=5)
        self.label_operation_size.pack(side="left", padx=(0, 1))
        self.config_button.pack(side="left")
        
        self.entry_operation_size.pack(pady=5)
        self.label_leverage.pack(pady=5)
        self.leverage_menu.pack(pady=5)
        self.label_operation_type .pack(pady=5)
        self.operation_type_menu.pack(pady=5)
        self.calculate_button.pack(pady=10)
        self.result_label.pack(pady=10)

    def _update_currency(self, new_currency):
        self.current_currency.set(new_currency)
        if all(entry.get() for entry in [self.entry_entry_price, self.entry_exit_price, self.entry_operation_size]):
            self._calculate()

    def _open_config(self):
        ConfigWindow(self.window, self._update_currency, self.window_icon)

    def _calculate(self):
        try:
            entry_price = float(self.entry_entry_price.get())
            exit_price = float(self.entry_exit_price.get())
            operation_size_dollars = float(self.entry_operation_size.get())
            operation_type  = self.operation_type_menu.get()
            leverage_selection = self.leverage_menu.get()

            leverage = get_leverage_value(leverage_selection)
            asset_amount = calculate_asset_amount(
                operation_size_dollars, entry_price, leverage, operation_type 
            )
            resultado = calculate_trade_result(entry_price, exit_price, asset_amount)
            
            currency_symbol = self.CURRENCY_SYMBOLS[self.current_currency.get()]

            if resultado > 0:
                self.result_label.configure(
                    text=f"Amount of assets: {asset_amount:.2f}\n"
                         f"Profit: {abs(resultado):.2f}{currency_symbol}",
                    text_color="#4B3FEB"
                )
            elif resultado < 0:
                self.result_label.configure(
                    text=f"Amount of assets: {asset_amount:.2f}\n"
                         f"Loss: -{abs(resultado):.2f}{currency_symbol}",
                    text_color="#FF004B"
                )
            else:
                self.result_label.configure(
                    text=f"Amount of assets: {asset_amount:.2f}\n"
                         f"Breakeven: {abs(resultado):.2f}{currency_symbol}",
                    text_color="#C0C0C0"
                )
        except ValueError:
            self.result_label.configure(
                text="Please enter valid values.",
                text_color="#FF6600"
            )

    def run(self):
        self.window.mainloop()
        
class ConfigWindow:
    def __init__(self, parent, callback, icon_image):
        self.top = ctk.CTkToplevel(parent)
        self.top.title("Settings")
        self.top.geometry("300x150")
        self.top.resizable(False, False)
        self.callback = callback

        self.top.configure(fg_color="#0a0a0a")
        self.top.wm_iconbitmap()
        self.top.after(300, lambda: self.top.iconphoto(False, icon_image))
        
        self.top.transient(parent)
        
        self.top.wait_visibility()  
        self.top.grab_set()       

        x = parent.winfo_x() + (parent.winfo_width() // 2) - (300 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (150 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        self.bold11 = ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        self.bold12 = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        
        self._create_widgets()

    def _create_widgets(self):
        label = ctk.CTkLabel(self.top, text="Select Currency:", font=self.bold12)
        label.pack(pady=20)
        
        self.currency_menu = ctk.CTkOptionMenu(
            master=self.top,
            command=self.on_currency_change,
            values=list(TradingCalculator.CURRENCY_SYMBOLS.keys()),
            width=150,
            height=30,
            corner_radius=6,
            font=self.bold11,
            dropdown_font=self.bold11,
            anchor="center",
            text_color="#C0C0C0",
            fg_color="#000000",
            button_color="#000000",
            button_hover_color="#000000",
            dropdown_fg_color="#000000",
        )
        self.currency_menu.set("USD")
        self.currency_menu.pack(pady=10)

    def on_currency_change(self, value):
        self.callback(value)
        self.top.destroy()

def create_interface():
    app = TradingCalculator()
    app.run()
