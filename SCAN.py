import cv2
import serial
import time
import re
import tkinter as tk
from tkinter import messagebox

# --- Bluetooth Setup ---
bluetooth_port = 'COM3'  # Update as needed
bluetooth_baud_rate = 9600

try:
    bluetooth = serial.Serial(bluetooth_port, bluetooth_baud_rate, timeout=1)
    time.sleep(2)  # Wait for connection
except serial.SerialException:
    messagebox.showerror("Error", f"Could not connect to Bluetooth on {bluetooth_port}")
    exit()

# --- Global Data ---
qr_data_dict = {
    "Name": "",
    "Address": "",
    "Pin-code": "",
    "Delivery Date": "",
    "Product ID": ""
}

# --- Functions ---

def scan_qr_code():
    global qr_data_dict

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        data, _, _ = detector.detectAndDecode(img)

        if data:
            print("QR Code Data:\n", data)

            # Extract fields using regex
            qr_data_dict["Name"] = re.search(r"Name:\s*(.*)", data).group(1) if re.search(r"Name:\s*(.*)", data) else ""
            qr_data_dict["Address"] = re.search(r"Address:\s*(.*)", data).group(1) if re.search(r"Address:\s*(.*)", data) else ""
            qr_data_dict["Pin-code"] = re.search(r"Pin-code:\s*(.*)", data).group(1) if re.search(r"Pin-code:\s*(.*)", data) else ""
            qr_data_dict["Delivery Date"] = re.search(r"Delivery Date:\s*(.*)", data).group(1) if re.search(r"Delivery Date:\s*(.*)", data) else ""
            qr_data_dict["Product ID"] = re.search(r"Product ID:\s*([\w\d]+)", data).group(1) if re.search(r"Product ID:\s*([\w\d]+)", data) else ""

            # Update labels
            lbl_name.config(text=f"Name: {qr_data_dict['Name']}")
            lbl_address.config(text=f"Address: {qr_data_dict['Address']}")
            lbl_pin.config(text=f"Pin-code: {qr_data_dict['Pin-code']}")
            lbl_date.config(text=f"Delivery Date: {qr_data_dict['Delivery Date']}")
            lbl_product.config(text=f"Product ID: {qr_data_dict['Product ID']}")
            break

        cv2.imshow("QR Code Scanner", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def send_to_robot():
    pid = qr_data_dict["Product ID"]
    if not pid:
        messagebox.showwarning("No Data", "Please scan a QR code first.")
        return
    try:
        bluetooth.write(pid.encode())
        time.sleep(1)
        lbl_status.config(text="✅ Data sent successfully to robot!", fg="green")
    except serial.SerialException:
        lbl_status.config(text="❌ Failed to send data to robot.", fg="red")

# --- GUI Setup ---

root = tk.Tk()
root.title("QR Code Robot Automation")
root.geometry("500x450")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Background color

# Title label
tk.Label(root, text="QR Code Automation System", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=20)

# Scan QR button with modern styling
btn_scan = tk.Button(root, text="📷 Scan QR Code", font=("Helvetica", 12), command=scan_qr_code, bg="#4CAF50", fg="white", relief="flat", padx=15, pady=10, bd=0, cursor="hand2")
btn_scan.pack(pady=10)

# Display QR Data
lbl_name = tk.Label(root, text="Name: ", font=("Helvetica", 12), bg="#f0f0f0", anchor="w")
lbl_name.pack(fill="x", padx=20)
lbl_address = tk.Label(root, text="Address: ", font=("Helvetica", 12), bg="#f0f0f0", anchor="w")
lbl_address.pack(fill="x", padx=20)
lbl_pin = tk.Label(root, text="Pin-code: ", font=("Helvetica", 12), bg="#f0f0f0", anchor="w")
lbl_pin.pack(fill="x", padx=20)
lbl_date = tk.Label(root, text="Delivery Date: ", font=("Helvetica", 12), bg="#f0f0f0", anchor="w")
lbl_date.pack(fill="x", padx=20)
lbl_product = tk.Label(root, text="Product ID: ", font=("Helvetica", 12, "bold"), bg="#f0f0f0", anchor="w")
lbl_product.pack(fill="x", padx=20, pady=10)

# Send Data button with modern styling
btn_send = tk.Button(root, text="📤 Send to Robot", font=("Helvetica", 12), command=send_to_robot, bg="#2196F3", fg="white", relief="flat", padx=15, pady=10, bd=0, cursor="hand2")
btn_send.pack(pady=10)

# Status label for successful or failed data sending
lbl_status = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
lbl_status.pack(pady=5)

# --- Run the GUI loop ---
def on_closing():
    bluetooth.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
