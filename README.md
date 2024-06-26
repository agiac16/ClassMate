

## Setting Up and Running the Project 



1. Clone the repository:

   - Clone your repository by running the following command in the terminal:
 
     ```shell
     git clone https://github.com/agiac16/ClassMate.git
     ```
   
   - Navigate to the project directory:
    
     ```shell
     cd ClassMate
     ```
    

2. Set up a virtual environment and install dependencies:
   - Create a new virtual environment:
   
     ``` shell
     python3 -m venv myenv
     ```
   
   - Activate the virtual environment:
     - On macOS/Linux:

       ```shell
       source myenv/bin/activate
       ```
 
     - On Windows:

        ```shell
       .\myenv\Scripts\activate
       ```
     
   - Install the required packages:
     
       ```shell
       pip install -r requirements.txt
       ```
   

3. Set up the database:
   - Run the following commands to make migrations and migrate the database:
  
     ```shell
     python manage.py makemigrations  
     python manage.py migrate
     ```


4. Run the project
   - Start the development server:
     
     ```shell
     python manage.py runserver
     ```
     
   - Open a web browser and go to [http://localhost:8000/](http://localhost:8000/) to view the project.

## Generating Fake Data

To populate your database with fake data for testing and development purposes:

1. Ensure that your virtual environment is activated and you are in the project directory.
2. Run the fake data script:
   - In the terminal, execute the following command:
     
     ```bash
     python manage.py import_courses
  
     python path/to/fixture.py

     python fixture.py
     ```
  
3. The script will generate and save fake data to your database
.   You can now use this data for testing and development purposes.





