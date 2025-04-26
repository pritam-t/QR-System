import qrcode
import tkinter as tk
from tkinter import messagebox

def create_qr_code(name, address, pin_code, delivery_date, product_id):
    qr_data = f"Name: {name}\nAddress: {address}\nPin-code: {pin_code}\nDelivery Date: {delivery_date}\nProduct ID: {product_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    img.show()

def on_generate():
    name = entry_name.get()
    address = entry_address.get()
    pin_code = entry_pin.get()
    delivery_date = entry_date.get()
    product_id = entry_pid.get()

    if not (name and address and pin_code and delivery_date and product_id):
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    create_qr_code(name, address, pin_code, delivery_date, product_id)
    messagebox.showinfo("Success", "QR Code Generated and Saved as 'qrcode.png'")

# --- UI Setup ---
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x400")
root.resizable(False, False)

tk.Label(root, text="Name:").pack(pady=5)
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Address:").pack(pady=5)
entry_address = tk.Entry(root, width=40)
entry_address.pack()

tk.Label(root, text="Pin-code:").pack(pady=5)
entry_pin = tk.Entry(root, width=40)
entry_pin.pack()

tk.Label(root, text="Delivery Date (YYYY-MM-DD):").pack(pady=5)
entry_date = tk.Entry(root, width=40)
entry_date.pack()

tk.Label(root, text="Product ID:").pack(pady=5)
entry_pid = tk.Entry(root, width=40)
entry_pid.pack()

tk.Button(root, text="Generate", command=on_generate, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

root.mainloop()
