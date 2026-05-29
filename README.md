# MedTrack: Personal Medication Reminder System

## Application Description

MedTrack is a standalone console-based medication reminder system developed using Object-Oriented Programming (OOP) and SOLID principles. The application allows users to manage medicine schedules, receive medication reminders, and store records using CSV file handling for data persistence.

The application allows users to:

- Add and manage medicine schedules, including medicine name, dosage, and intake time. Users can also remove existing records.
- View all saved medication records in a formatted console display.
- Check due medications and receive reminder notifications based on the current system time.
- Store medication records using local CSV file handling for persistent data storage across sessions.

Built as a console-based application, the system emphasizes simplicity, accessibility, and reliability. The application operates entirely offline and does not require external databases or internet connectivity.

Through this application, users can improve medication adherence, maintain organized medicine records, and reduce the risk of forgetting scheduled medicine intake.

---

## OOP Concepts Used

This project demonstrates core Object-Oriented Programming principles:

- **Encapsulation** — Medicine attributes (`_name`, `_dosage`, `_intake_time`) are controlled through getters and setters.
- **Abstraction** — Interfaces such as `IDataSaver`, `IInputSource`, and `INotifier` define standard behaviors.
- **Polymorphism** — Different implementations can be substituted through shared interfaces.
- **Modularity** — The system separates input handling, notifications, file management, and scheduling into distinct components.
- **Dependency Injection** — Dependencies are passed into the `Scheduler` class through its constructor.

---

## Technologies Used

- Python 3.x
- CSV file handling
- Object-Oriented Programming (OOP)

### Standard Python Libraries

- `abc`
- `csv`
- `datetime`
- `os`
- `re`

---

## Project Structure

```text
MedTrack/

│

├── interfaces/

│   ├── __init__.py

│   ├── IInputSource.py

│   ├── IDataSaver.py

│   └── INotifier.py

│

├── models/

│   ├── __init__.py

│   └── Medicine.py

│

├── services/

│   ├── __init__.py

│   ├── ConsoleInput.py

│   ├── ConsoleNotifier.py

│   ├── CsvDataSaver.py

│   └── Scheduler.py

│

├── main.py

├── README.md

└── mymeds_history.csv
```

---

## How to Run

### Requirements

- Python 3.x installed on the machine

### Steps to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/yeszhaya/MedTrack.git
   ```

2. Navigate to the project folder:
   ```bash
   cd MedTrack
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Follow the on-screen menu prompts to manage medication schedules.

---

## Group Members

- Irish Yszha G. Merca
  ```bash
  https://github.com/yeszhaya
  ```
- Mira B. Maximo
  ```bash
  https://github.com/raxy-m
  ```
- Jamella B. Gaton
  ```bash
  https://github.com/jamellagaton563-cell
  ```

---

## Academic Information

In partial fulfillment of the requirements for the subject CC103 – Computer Programming 2 under the Bachelor of Science in Information Technology program at Sorsogon State University – Bulan Campus.

---

## Notes

- The application operates entirely offline.
- Data is automatically saved in `mymeds_history.csv`.
- Designed primarily for educational purposes and OOP implementation practice.
