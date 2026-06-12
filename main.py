import customtkinter as ctk
from tkinter import filedialog, messagebox
import tomllib
import tomli_w

CONFIG_FILE = "modengine.toml"


class ModEngineGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dark Souls Remastered - Mod Engine Config")
        self.geometry("1000x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.data = None
        self.mod_widgets = []

        title = ctk.CTkLabel(
            self,
            text="Dark Souls Remastered - Mod Engine",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=15)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Reload",
            command=self.load_config
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Add Mod",
            command=self.add_mod
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Save",
            command=self.save_config
        ).pack(side="right", padx=5)

        self.load_config()

    def browse_folder(self, entry):
        folder = filedialog.askdirectory()

        if folder:
            entry.delete(0, "end")
            entry.insert(0, folder)

    def remove_mod(self, mod_info):
        mod_info["frame"].destroy()

        if mod_info in self.mod_widgets:
            self.mod_widgets.remove(mod_info)

    def create_mod_row(self, mod):
        frame = ctk.CTkFrame(self.scroll)
        frame.pack(fill="x", pady=5)

        enabled = ctk.BooleanVar(value=mod.get("enabled", True))

        checkbox = ctk.CTkCheckBox(
            frame,
            text="",
            variable=enabled,
            width=30
        )
        checkbox.grid(row=0, column=0, padx=10)

        name = ctk.CTkEntry(frame, width=200)
        name.insert(0, mod.get("name", ""))
        name.grid(row=0, column=1, padx=5)

        path = ctk.CTkEntry(frame)
        path.insert(0, mod.get("path", ""))
        path.grid(row=0, column=2, padx=5, sticky="ew")

        browse_btn = ctk.CTkButton(
            frame,
            text="Browse",
            width=90,
            command=lambda e=path: self.browse_folder(e)
        )
        browse_btn.grid(row=0, column=3, padx=5)

        delete_btn = ctk.CTkButton(
            frame,
            text="✕",
            width=40
        )
        delete_btn.grid(row=0, column=4, padx=5)

        frame.grid_columnconfigure(2, weight=1)

        mod_info = {
            "frame": frame,
            "enabled": enabled,
            "name": name,
            "path": path
        }

        delete_btn.configure(
            command=lambda: self.remove_mod(mod_info)
        )

        self.mod_widgets.append(mod_info)

    def add_mod(self):
        self.create_mod_row({
            "enabled": True,
            "name": "New Mod",
            "path": ""
        })

    def load_config(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.mod_widgets.clear()

        try:
            with open(CONFIG_FILE, "rb") as f:
                self.data = tomllib.load(f)

        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                f"Could not find {CONFIG_FILE}"
            )
            return

        modengine = self.data["modengine"]
        mod_loader = self.data["extension"]["mod_loader"]
        scylla = self.data["extension"]["scylla_hide"]

        ctk.CTkLabel(
            self.scroll,
            text="General Settings",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.debug_var = ctk.BooleanVar(
            value=modengine.get("debug", False)
        )

        ctk.CTkCheckBox(
            self.scroll,
            text="Debug Console",
            variable=self.debug_var
        ).pack(anchor="w", pady=5)

        self.loader_var = ctk.BooleanVar(
            value=mod_loader.get("enabled", True)
        )

        ctk.CTkCheckBox(
            self.scroll,
            text="Mod Loader Enabled",
            variable=self.loader_var
        ).pack(anchor="w", pady=5)

        self.loose_var = ctk.BooleanVar(
            value=mod_loader.get("loose_params", False)
        )

        ctk.CTkCheckBox(
            self.scroll,
            text="Loose Params",
            variable=self.loose_var
        ).pack(anchor="w", pady=5)

        self.scylla_var = ctk.BooleanVar(
            value=scylla.get("enabled", False)
        )

        ctk.CTkCheckBox(
            self.scroll,
            text="Scylla Hide",
            variable=self.scylla_var
        ).pack(anchor="w", pady=5)

        ctk.CTkLabel(
            self.scroll,
            text="Mods",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", pady=(20, 10))

        for mod in mod_loader.get("mods", []):
            self.create_mod_row(mod)

    def save_config(self):
        try:
            self.data["modengine"]["debug"] = self.debug_var.get()

            self.data["extension"]["mod_loader"]["enabled"] = (
                self.loader_var.get()
            )

            self.data["extension"]["mod_loader"]["loose_params"] = (
                self.loose_var.get()
            )

            self.data["extension"]["scylla_hide"]["enabled"] = (
                self.scylla_var.get()
            )

            mods = []

            for mod in self.mod_widgets:
                mods.append({
                    "enabled": mod["enabled"].get(),
                    "name": mod["name"].get(),
                    "path": mod["path"].get()
                })

            self.data["extension"]["mod_loader"]["mods"] = mods

            with open(CONFIG_FILE, "wb") as f:
                f.write(
                    tomli_w.dumps(self.data).encode("utf-8")
                )

            messagebox.showinfo(
                "Success",
                "Configuration saved successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


if __name__ == "__main__":
    app = ModEngineGUI()
    app.mainloop()