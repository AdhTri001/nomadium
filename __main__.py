import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import match_faces as mf

TEMPLATES = []
SEARCH_IMAGES = []

def reload_module():
    """Reload the module"""
    import importlib
    importlib.reload(mf)

def laod_templates():
    """Adds the template images to the list"""
    files = filedialog.askopenfilename(
        title="Select template images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")],
        multiple=True
    )

    if files:
        files = list(files)
        TEMPLATES.extend(files)
        messagebox.showinfo("Success", "Templates added to the list")


def load_search_images():
    """Add the search images to the list"""
    files = filedialog.askopenfilename(
        title="Select images to search",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")],
        multiple=True
    )

    if files:
        files = list(files)
        SEARCH_IMAGES.extend(files)
        messagebox.showinfo("Success", "Images added to search list")


def start_search():
    """Search the images and save the list of images matched to a text file"""
    if not TEMPLATES or not SEARCH_IMAGES:
        messagebox.showerror("Error", "Please add templates and search images first")
        return

    def do_search_task():
        matched_images = mf.search_faces(TEMPLATES, SEARCH_IMAGES)

        if matched_images:
            with open("matched_images.txt", "w") as f:
                f.write("\n".join(matched_images))
            messagebox.showinfo("Success", "Matched images saved to matched_images.txt")
        else:
            messagebox.showinfo("No matches found")

    Thread(target=do_search_task).start()


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Nomadium")
    root.geometry("300x200")

    # Create a label for instructions
    label = tk.Label(root, text="Image search through faces")
    label.pack(pady=10)

    # Create buttons and attach functions
    templ_img_btn = tk.Button(root, text="Load templates", command=laod_templates)
    templ_img_btn.pack(pady=5)

    search_img_btn = tk.Button(root, text="Load search directories / Images", command=load_search_images)
    search_img_btn.pack(pady=5)

    # Create a button to start the search
    start_search_btn = tk.Button(root, text="Start search", command=start_search)
    start_search_btn.pack(pady=5)

    reload_btn = tk.Button(root, text="Reload module", command=reload_module)
    reload_btn.pack(pady=5)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()