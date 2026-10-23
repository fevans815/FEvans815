# Kitchen Inventory Task Manager

## Project Overview
Kitchen Inventory Task Manager is a desktop application developed in Python for my Advanced Software Engineering course at Full Sail University.

The application helps users manage kitchen inventory, monitor low-stock items, and maintain a shopping list.

## Features
- Add new inventory items with names, quantities, and minimum stock levels.
- Update existing inventory items.
- Delete inventory items.
- Automatically identify items that are low in stock.
- Display color-coded inventory statuses.
- Generate shopping-list tasks for low-stock items.
- Mark shopping-list items as purchased.
- Prevent duplicate active shopping-list tasks.
- Validate user input and display helpful error messages.

## Technologies Used
- Python 3
- Tkinter for the graphical user interface
- SQLite for database storage
- Python unittest for automated testing
- PyInstaller for building the macOS application

## Running the Application
Open Terminal and navigate to the project folder:

```bash
cd ~/Documents/GitHub/FEvans815
```

Run the application:

```bash
python3 main.py
```

## Automated Testing
The project includes 12 automated tests covering inventory management, low-stock detection, shopping-list generation, purchased-item tracking, and data validation.

Run the tests using:

```bash
python3 -m unittest test_database.py -v
```

## Building the Application
The macOS application can be built using PyInstaller:

```bash
python3 -m PyInstaller --clean --noconfirm --windowed --name KitchenInventory main.py
```

The application will be created inside the `dist` folder as `KitchenInventory.app`.

## Known Limitations
- The application is designed for local desktop use.
- Inventory data is stored in a local SQLite database.
- Shopping-list items must be marked as purchased manually.

## Developer
Developed for Full Sail University's Advanced Software Engineering course.

## Milestone 3
Milestone 3 focuses on input validation, clearer error messages, improved interface readability, regression testing, documentation, and final application packaging.