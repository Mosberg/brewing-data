# texture_gui.py
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk
import texture_core as core

ITEM_TYPES = list(core.SILHOUETTES.keys())
PALETTE_KEYS = list(core.PALETTES.keys())
SIZES = [16, 32, 64]

class TextureGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minecraft Item Texture Generator")

        self.item_type = tk.StringVar(value="bottle")
        self.palette_key = tk.StringVar(value="glass")
        self.size = tk.IntVar(value=16)
        self.frames = tk.IntVar(value=1)
        self.seed = tk.IntVar(value=0)
        self.use_seed = tk.BooleanVar(value=False)

        self._build_controls()
        self._build_canvas()
        self.preview_img_tk = None

        self.update_preview()

    def _build_controls(self):
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(frame, text="Item type").pack(anchor="w")
        ttk.Combobox(frame, textvariable=self.item_type, values=ITEM_TYPES, state="readonly")\
            .pack(fill=tk.X)

        ttk.Label(frame, text="Palette").pack(anchor="w", pady=(8,0))
        ttk.Combobox(frame, textvariable=self.palette_key, values=PALETTE_KEYS, state="readonly")\
            .pack(fill=tk.X)

        ttk.Label(frame, text="Size").pack(anchor="w", pady=(8,0))
        ttk.Combobox(frame, textvariable=self.size, values=SIZES, state="readonly")\
            .pack(fill=tk.X)

        ttk.Label(frame, text="Frames (vertical strip)").pack(anchor="w", pady=(8,0))
        ttk.Spinbox(frame, from_=1, to=32, textvariable=self.frames)\
            .pack(fill=tk.X)

        seed_frame = ttk.Frame(frame)
        seed_frame.pack(fill=tk.X, pady=(8,0))
        ttk.Checkbutton(seed_frame, text="Use seed", variable=self.use_seed)\
            .pack(side=tk.LEFT)
        ttk.Entry(seed_frame, textvariable=self.seed, width=6)\
            .pack(side=tk.LEFT, padx=(4,0))

        ttk.Button(frame, text="Update preview", command=self.update_preview)\
            .pack(fill=tk.X, pady=(12,0))
        ttk.Button(frame, text="Save PNG...", command=self.save_png)\
            .pack(fill=tk.X, pady=(4,0))

    def _build_canvas(self):
        self.canvas_frame = ttk.Frame(self.root, padding=8)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#202020", width=256, height=256)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def update_preview(self):
        size = self.size.get()
        frames = max(1, int(self.frames.get()))
        item_type = self.item_type.get()
        palette_key = self.palette_key.get()
        seed = self.seed.get() if self.use_seed.get() else None

        img = core.generate_texture(size, item_type, frames=frames,
                                    palette_key=palette_key, seed=seed)

        display_size = 256
        scale_x = display_size // size
        scale_y = display_size // size
        scale = min(max(1, scale_x), max(1, scale_y))

        new_w = size
        new_h = size * frames
        img_resized = img.resize((new_w*scale, new_h*scale), Image.NEAREST)

        self.preview_img_tk = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0,0,new_w*scale,new_h*scale))
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_img_tk)

    def save_png(self):
        size = self.size.get()
        frames = max(1, int(self.frames.get()))
        item_type = self.item_type.get()
        palette_key = self.palette_key.get()
        seed = self.seed.get() if self.use_seed.get() else None

        img = core.generate_texture(size, item_type, frames=frames,
                                    palette_key=palette_key, seed=seed)

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files","*.png")],
            initialfile=f"{item_type}_{size}.png"
        )
        if not path:
            return
        img.save(path)

def main():
    root = tk.Tk()
    app = TextureGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
