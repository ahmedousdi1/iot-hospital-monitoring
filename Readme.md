IoT Hospital Monitoring

An IoT-based system for tracking patient vitals in real time. Sensor nodes collect data such as heart rate and body temperature and send it to a Flask backend, which makes it available through a simple web dashboard.

Features


Real-time monitoring of patient vital signs
Multiple sensor nodes (environment, patient, RFID-based identification)
Flask backend for receiving and processing sensor data
Simple web dashboard for viewing live data


Tech Stack


Backend: Python (Flask)
Frontend: HTML
Hardware: ESP32 / Arduino-based sensor nodes


Project Structure

.
├── backend_appli.py     # Main Flask backend application
├── envi_node.py          # Environment sensor node script
├── patient_node.py       # Patient vitals sensor node script
├── rfid_node.py           # RFID identification node script
├── templates/
│   └── index.html        # Web dashboard
├── .env                  # Environment variables (not committed)
└── .gitignore

Getting Started

Prerequisites


Python 3.x
Flask
ESP32/Arduino sensor nodes (for live hardware data)


Installation


Clone the repository


bash   git clone https://github.com/ahmedousdi1/iot-hospital-monitoring.git
   cd iot-hospital-monitoring


Install dependencies


bash   pip install flask


Set up environment variables in a .env file (see .env for required keys — never commit this file)
Run the backend


bash   python backend_appli.py


Flash envi_node.py, patient_node.py, and rfid_node.py to their respective sensor devices
Open the dashboard in your browser at the address shown in the terminal


Notes


Sensor nodes communicate readings to the backend, which processes and serves them to the dashboard.
The RFID node is used to identify/associate readings with a specific patient.


License

No license specified yet.