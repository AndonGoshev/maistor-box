## Getting started

### Requirements
Make sure you have the following installed:
- Python version 3.11 or higher (if WinOS keep in mind that higher versions may not be compatible with psycopg2 driver)
- pip version 23.2.1 or higher (if WinOS keep in mind that higher versions may not be compatible with psycopg2 driver)
- postgresql


### 1. Clone the Repository
Run the following command in your terminal or command prompt:
```bash
# Navigate to the directory where you want to clone the project
cd /path/to/your/directory

# Clone the repository
git clone https://github.com/AndonGoshev/maistor-box.git

# Move into the project directory
cd maistor-box
```

### 2. Create and Activate a Virtual Environment
#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
```

### 4. Configure the Environment Variables

2. **Update the .env File with Your Credentials**  
   Open the `.env` file in a text editor and replace the placeholders with your actual PostgreSQL credentials.

   Example `.env` file:
   ```
   SECRET_KEY=your-secret-key
   DB_NAME=maistor_box
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

   **Explanation of the fields:**
   - `SECRET_KEY`: A random secret key for Django (You can generate one using `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`).
   - `DB_NAME`: The name of your PostgreSQL database (e.g., `maistor_box`).
   - `DB_USER`: Your PostgreSQL username.
   - `DB_PASSWORD`: Your PostgreSQL password.
   - `DB_HOST`: The address of your PostgreSQL server (use `127.0.0.1` for local setup).
   - `DB_PORT`: The port number for PostgreSQL (default is `5432`).
   - `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames or IP addresses (e.g., `127.0.0.1,localhost` for local development).



### 5. Apply Migrations
Run the migrations to set up the database:
```bash
python manage.py migrate
```

### 6. Run the custom commands for populating the database
This command runs a series of other commands that populate the database. Use it to simulate a functional and usable web application and explore its capabilities. Approx. running time 1min. 
```bash
python manage.py run_all_start_up_commands
```

### 6.1 (optional alternative approach) Run the custom commands manually.

#### `python manage.py populate_region_and_specialization_models`
- This command creates instances of the **Region** and **Specialization** models. These are required for the creation of **ContractorUser** models because fields for region and specialization are mandatory during registration.
- The relationship between **Region** and **Specialization** models and the **ContractorUserModel** is many-to-many (M2M).

#### `python manage.py populate_base_user_model`
- This command creates **20** regular **Base User** instances.
- It triggers a `post_save` signal that sends a welcome email to the user after they register on the platform.
- The purpose of this command is to ensure the creation of **ClientFeedbackModel** random instances. If no regular users are created, all feedback will be submitted by contractors only.

#### `python manage.py populate_contractor_user_model`
- This command creates **50** **Base User** instances with additional required fields for first and last name, which are mandatory during contractor registration.
- It also creates **50** **ContractorUserModel** instances, which are linked one-to-one (O2O) with **BaseUserModel**.
- A welcome email is sent via `post_save` signal.
- Additionally, a second signal is triggered to create instances of **ContractorPublicModel**, which separates the logic for the user account from the public profile.

#### `python manage.py populate_projects_for_all_of_the_contractor_model_instances`
- This command iterates over all existing **ContractorUserModel** instances and creates several **ProjectModel** instances associated with the corresponding **ContractorUserModel** via a one-to-many (O2M) relationship.

#### `python manage.py populate_feedbacks_for_all_of_the_contractor_public_instances`
- This command iterates over all existing **ContractorPublicModel** instances and creates several **ClientFeedbackModel** instances associated with the corresponding **ContractorPublicModel** via a one-to-many (O2M) relationship.

#### `python manage.py create_company`
- This command creates a single instance of the **CompanyModel**, providing a centralized place to store company data.

#### `python manage.py create_groups`
- This command creates three admin groups:
  - **Super Admin**: Has all permissions.
  - **Client Feedback Redactor**: Can view everything and perform CRUD operations on **ClientFeedbackModel**.
  - **Viewer**: Can view everything but cannot make any changes.

#### <span style="color:#FD841F">**The data population process creates realistic contractor profiles with random profile images, a random number of projects, project images, feedbacks, rating stars, feedback lengths, and both positive and negative comments.**</span>

### 7. Create superuser
In order the admin panel to be usable create superuser. Run this command and follow the registration process
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```

### 9. Access the Project
Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 10. Credentials that you can use
For base users (username = regular_user1, password = password123) , for contractor users (username = contractor21, password = password123)

### 11. (optional) Assign users to groups 
Go to http://localhost:8000/admin ,login as admin ,open the user model, choose a user, open their instance, and you can place this user into group with specific permissions. 
