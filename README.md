

Setting Up and Running the Project 



1. Clone the repository:

   - Clone your repository by running the following command in the terminal:
 
     git clone https://github.com/yourusername/senior-project.git
   
   - Navigate to the project directory:
    
     cd senior-project
    

2. Set up a virtual environment and install dependencies:
   - Create a new virtual environment:
   
     python3 -m venv myenv
   
   - Activate the virtual environment:
     - On macOS/Linux:

       source myenv/bin/activate
 
     - On Windows:

       .\myenv\Scripts\activate
     
   - Install the required packages:
     
     pip install -r requirements.txt
     pip install django
   

3. Set up the database:
   - Run the following commands to make migrations and migrate the database:
  
     python manage.py makemigrations
     python manage.py migrate


4. Run the project
   - Start the development server:
     
     python manage.py runserver
     
   - Open a web browser and go to [http://localhost:8000/](http://localhost:8000/) to view the project.

## Generating Fake Data

To populate your database with fake data for testing and development purposes:

1. Ensure that your virtual environment is activated and you are in the project directory.
2. Run the fake data script:
   - In the terminal, execute the following command:
  
     python path/to/fixture.py

     python fixture.py
  
3. The script will generate and save fake data to your database
.   You can now use this data for testing and development purposes.





