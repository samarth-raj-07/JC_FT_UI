# File Transfer System

This system automates file transfers between a **Signal PC**, **Bridge PC**, and **Server PC**.

## **How It Works**
1. **Signal PC (GUI)**
   - User requests a file.
   - The request is sent to Bridge PC.
   
2. **Bridge PC**
   - Forwards request to Server PC.
   - Receives file and sends it back to Signal PC.

3. **Server PC**
   - Sends the requested file to Bridge PC.

## **Setup Instructions**

### **Windows (Using NSSM)**
1. Install [NSSM](https://nssm.cc/).
2. Run `start_services.bat` as Administrator.
3. Services will start automatically on boot.

### **Linux (Using systemd)**
1. Run `chmod +x start_services.sh && ./start_services.sh`.
2. Services will start automatically.

## **Usage**
- Run `signal.py` on the **Signal PC**.
- Enter the filename and request the file.
