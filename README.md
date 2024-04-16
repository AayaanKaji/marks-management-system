# Marks Management System

This project is a comprehensive marks management system designed to streamline the process of recording, updating, and accessing student marks for teachers, students, and administrators. Below are the key features and functionalities of the system:

## Features

### User Roles

- Admin
  - Updates teachers' associated subjects.
  - Publishes results.
  - Views teachers' details.

- Teacher

  - Modifies marks of students for particular subjects.
  - Views students' details.

- Student

  - Modifies their personal data.
  - Views their marks.

### Functionality

- **User Registration**
  - Students and teachers can register with their respective details.

- **Data Modification**
  - Users can modify their personal data such as contact information.

- **Marks Viewing**
  - Students can view their marks for different subjects.

- **Subject-wise Mark Modification**
  - Subject teachers can modify marks for students only in their respective subjects.

- **Result Publication**
  - Admin publishes the results.

- **Data Accessibility**:
  - After publication, everyone can access the data.
  - Search functionality available by roll number.
  - Data can be ordered by subject scores and total scores.

## Technologies Used

- **Frontend**
  - Tkinter - Crafting engaging graphical user interfaces with finesse.

- **Backend**
  - Python - Empowering seamless data processing and management.

- **Database**
  - SQLite3 - Ensuring robust and efficient data storage and retrieval.

## Installation

1. Clone the Repository

    ```bash
    git clone [repository_url]
    ```

2. Install Dependencies
  
    Ensure you have Python installed on your system.
    Install Tkinter using the following command:

    ```bash
    pip install tk
    ```

3. Initial Setup

    Navigate to the project directory:

    ```bash
    cd marks-managemnet-system
    ```

    Execute the following command for the initial setup: (this may take a while)

    ```bash
    make
    ```

3. Launch the GUI

    After the initial setup, launch the graphical user interface (GUI) using the following command:

    ```bash
    python3 main.py
    ```
