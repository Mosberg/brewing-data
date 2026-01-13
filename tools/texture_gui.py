#!/usr/bin/env python3
"""
Interactive texture generator GUI.

Provides a graphical interface for generating and previewing textures
with real-time parameter adjustments.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

from PIL import ImageTk

import texture_core as core

# UI Constants
ITEM_TYPES = list(core.SILHOUETTES.keys())
PALETTE_KEYS = list(core.PALETTES.keys())
SIZES = [16, 32, 64]
DEFAULT_PREVIEW_SIZE = 256


class TextureGUI:
    """Interactive texture generator GUI."""

    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Minecraft Item Texture Generator")
        root.geometry("800x600")

        # UI Variables
        self.item_type = tk.StringVar(value="bottle")
        self.palette_key = tk.StringVar(value="glass")
        self.size = tk.IntVar(value=16)
        self.frames = tk.IntVar(value=1)
        self.seed = tk.IntVar(value=0)
        self.use_seed = tk.BooleanVar(value=False)

        # Preview cache
        self.preview_img_tk: Optional[ImageTk.PhotoImage] = None

        self._build_ui()
        self._update_preview()

    def _build_ui(self) -> None:
        """Build user interface components."""
        # Left control panel
        control_frame = ttk.Frame(self.root, padding=8)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        ttk.Label(control_frame, text="Item Type").pack(anchor="w", pady=(0, 2))
        ttk.Combobox(
            control_frame,
            textvariable=self.item_type,
            values=ITEM_TYPES,
            state="readonly",
            width=15,
        ).pack(fill=tk.X, pady=(0, 8))

        ttk.Label(control_frame, text="Palette").pack(anchor="w", pady=(0, 2))
        ttk.Combobox(
            control_frame,
            textvariable=self.palette_key,
            values=PALETTE_KEYS,
            state="readonly",
            width=15,
        ).pack(fill=tk.X, pady=(0, 8))

        ttk.Label(control_frame, text="Size (px)").pack(anchor="w", pady=(0, 2))
        ttk.Combobox(
            control_frame,
            textvariable=self.size,
            values=SIZES,
            state="readonly",
            width=15,
        ).pack(fill=tk.X, pady=(0, 8))

        ttk.Label(control_frame, text="Frames").pack(anchor="w", pady=(0, 2))
        ttk.Spinbox(
            control_frame,
            from_=1,
            to=32,
            textvariable=self.frames,
            width=17,
        ).pack(fill=tk.X, pady=(0, 8))

        # Seed control
        seed_frame = ttk.LabelFrame(control_frame, text="Seed", padding=4)
        seed_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Checkbutton(
            seed_frame,
            text="Use custom seed",
            variable=self.use_seed,
        ).pack(anchor="w")
        ttk.Entry(
            seed_frame,
            textvariable=self.seed,
            width=18,
        ).pack(fill=tk.X, pady=(4, 0))

        # Buttons
        ttk.Button(
            control_frame,
            text="Update Preview",
            command=self._update_preview,
        ).pack(fill=tk.X, pady=(12, 4))

        ttk.Button(
            control_frame,
            text="Save PNG...",
            command=self._save_png,
        ).pack(fill=tk.X)

        # Right canvas panel
        canvas_frame = ttk.LabelFrame(self.root, text="Preview", padding=4)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#2a2a2a",
            width=DEFAULT_PREVIEW_SIZE,
            height=DEFAULT_PREVIEW_SIZE,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _update_preview(self) -> None:
        """Generate and display preview texture."""
        try:
            size = self.size.get()
            frames = max(1, int(self.frames.get()))
            item_type = self.item_type.get()
            palette_key = self.palette_key.get()
            seed = self.seed.get() if self.use_seed.get() else None

            img = core.generate_texture(
                size=size,
                item_type=item_type,
                frames=frames,
                palette_key=palette_key,
                seed=seed,
            )

            # Scale for preview display
            display_size = DEFAULT_PREVIEW_SIZE
            scale = max(1, display_size // (size * frames))
            new_w = size * scale
            new_h = size * frames * scale

            # Use NEAREST for pixel-perfect rendering
            img_resized = img.resize((new_w, new_h), resample=0)  # 0 = NEAREST

            self.preview_img_tk = ImageTk.PhotoImage(img_resized)
            self.canvas.delete("all")
            self.canvas.create_image(
                display_size // 2,
                display_size // 2,
                image=self.preview_img_tk,
            )

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameters: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def _save_png(self) -> None:
        """Save texture to PNG file."""
        try:
            size = self.size.get()
            frames = max(1, int(self.frames.get()))
            item_type = self.item_type.get()
            palette_key = self.palette_key.get()
            seed = self.seed.get() if self.use_seed.get() else None

            img = core.generate_texture(
                size=size,
                item_type=item_type,
                frames=frames,
                palette_key=palette_key,
                seed=seed,
            )

            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"{item_type}_{size}.png",
            )

            if not path:
                return

            img.save(path)
            messagebox.showinfo("Success", f"Saved to:\n{path}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameters: {e}")
        except OSError as e:
            messagebox.showerror("Error", f"Save failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")


def main() -> None:
    """Launch GUI application."""
    root = tk.Tk()
    app = TextureGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

