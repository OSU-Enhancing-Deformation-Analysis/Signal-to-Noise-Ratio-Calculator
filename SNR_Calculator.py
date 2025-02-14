import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class SNRApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SNR Calculation Tool")
        self.master.geometry("800x600")
        
        self.folder1_path = None
        self.folder2_path = None
        self.roi = None
        self.image_folder1 = None
        self.image_folder2 = None
        
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Select two folders to process .tif images", font=("Arial", 14))
        self.label.grid(row=0, column=0, columnspan=3, pady=20)

        self.select_folder_button = tk.Button(self.master, text="Select Folder 1", command=self.select_folder1)
        self.select_folder_button.grid(row=1, column=0, padx=10, pady=5)

        self.select_folder_button2 = tk.Button(self.master, text="Select Folder 2", command=self.select_folder2)
        self.select_folder_button2.grid(row=1, column=1, padx=10, pady=5)

        self.start_button = tk.Button(self.master, text="Start SNR Calculation", state=tk.DISABLED, command=self.start_snr_calculation)
        self.start_button.grid(row=2, column=0, columnspan=3, pady=20)

        self.folder1_label = tk.Label(self.master, text="Folder 1: Not selected", anchor="w")
        self.folder1_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.folder2_label = tk.Label(self.master, text="Folder 2: Not selected", anchor="w")
        self.folder2_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        self.image_label1 = tk.Label(self.master, text="Folder 1 Image Preview")
        self.image_label1.grid(row=5, column=0, padx=10, pady=5)

        self.image_label2 = tk.Label(self.master, text="Folder 2 Image Preview")
        self.image_label2.grid(row=5, column=1, padx=10, pady=5)

        self.image_canvas1 = tk.Canvas(self.master, width=250, height=250)
        self.image_canvas1.grid(row=6, column=0, padx=10, pady=5)

        self.image_canvas2 = tk.Canvas(self.master, width=250, height=250)
        self.image_canvas2.grid(row=6, column=1, padx=10, pady=5)

    def select_folder1(self):
        self.folder1_path = filedialog.askdirectory(title="Select First Folder Containing .tif Images")
        if self.folder1_path:
            self.folder1_label.config(text=f"Folder 1: {self.folder1_path}")
            self.load_image(self.folder1_path, 1)
            self.select_folder_button.config(state=tk.NORMAL)

    def select_folder2(self):
        self.folder2_path = filedialog.askdirectory(title="Select Second Folder Containing .tif Images")
        if self.folder2_path:
            self.folder2_label.config(text=f"Folder 2: {self.folder2_path}")
            self.load_image(self.folder2_path, 2)
            self.select_folder_button2.config(state=tk.NORMAL)

    def load_image(self, folder_path, folder_num):
        image_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]
        if image_files:
            first_image_path = os.path.join(folder_path, image_files[0])
            image_pil = Image.open(first_image_path)
            image_resized = image_pil.resize((250, 250))  # Resize for display
            image_tk = ImageTk.PhotoImage(image_resized)

            if folder_num == 1:
                self.image_folder1 = np.array(image_pil)
                self.image_canvas1.create_image(0, 0, anchor="nw", image=image_tk)
                self.image_canvas1.image = image_tk
            else:
                self.image_folder2 = np.array(image_pil)
                self.image_canvas2.create_image(0, 0, anchor="nw", image=image_tk)
                self.image_canvas2.image = image_tk

            if self.folder1_path and self.folder2_path:
                self.start_button.config(state=tk.NORMAL)

    def start_snr_calculation(self):
        if not self.folder1_path or not self.folder2_path:
            messagebox.showerror("Error", "Both folders must be selected.")
            return

        try:
            self.process_folders()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_folders(self):
        folder1_files = [f for f in os.listdir(self.folder1_path) if f.endswith('.tif')]
        folder2_files = [f for f in os.listdir(self.folder2_path) if f.endswith('.tif')]

        if not folder1_files or not folder2_files:
            messagebox.showerror("Error", "No .tif images found in one or both folders.")
            return

        self.roi = cv2.selectROI("Select ROI", self.image_folder1)
        cv2.destroyWindow("Select ROI")

        folder1_snr_values, folder1_avg_snr = self.process_folder(self.folder1_path, folder1_files)
        folder2_snr_values, folder2_avg_snr = self.process_folder(self.folder2_path, folder2_files)

        self.show_results(folder1_avg_snr, folder2_avg_snr)

    def process_folder(self, folder_path, image_files):
        total_snr = 0
        snr_values = []
        for file_name in image_files:
            file_path = os.path.join(folder_path, file_name)
            image_pil = Image.open(file_path)
            image = np.array(image_pil)
            snr = self.calculate_snr(image)
            snr_values.append(snr)
            total_snr += snr
        if len(snr_values) > 0:
            average_snr = total_snr / len(snr_values)
        else:
            average_snr = 0
        return snr_values, average_snr

    def calculate_snr(self, image):
        x, y, w, h = self.roi
        roi_image = image[y:y+h, x:x+w]
        mean_signal = np.mean(roi_image)
        std_noise = np.std(roi_image)
        if std_noise > 0:
            snr = mean_signal / std_noise
        else:
            snr = 0
        return snr

    def show_results(self, folder1_avg_snr, folder2_avg_snr):
        result_message = f"Average SNR for Folder 1: {folder1_avg_snr:.2f}\n"
        result_message += f"Average SNR for Folder 2: {folder2_avg_snr:.2f}\n"

        if folder1_avg_snr > folder2_avg_snr:
            result_message += f"Folder 1 has the better average SNR."
        elif folder1_avg_snr < folder2_avg_snr:
            result_message += f"Folder 2 has the better average SNR."
        else:
            result_message += f"Both folders have the same average SNR."

        messagebox.showinfo("Results", result_message)

def main():
    root = tk.Tk()
    app = SNRApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
