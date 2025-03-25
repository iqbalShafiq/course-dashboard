# Course Dashboard
A simple dashboard project designed to learn the basics of using Django Admin and task queues with Huey. This project also includes deploying a Django application to a virtual machine on Google Cloud Platform (GCP).

>  **Note:** This project is a submission for the **AI-Enabled Python Web Development Bootcamp** by **Devscale.id**.

## Features
-  **Courses**: List, create, and edit courses.

-  **Teachers**: List and edit teacher information.

-  **Schedules**: View schedules, which are created using a task queue on the course detail page.

	- Teachers and schedule times are randomly assigned.
	- Each course can have only one schedule.

## Technical Details
-  **Database**: PostgreSQL is used as the primary database.
-  **Task Queue**: Redis is used for managing the task queue with Huey.

## Installation
1. Clone the repository:

```bash
https://github.com/iqbalShafiq/course-dashboard.git

```

2. Navigate to the project directory:

```bash
cd course-dashboard

```

3. Install the required dependencies:

```bash
pip install -r requirements.txt

```

4. Set up the PostgreSQL database and Redis server.

5. Create a `.env` file from the example file:

```bash
cp .env.example .env

```

6. Update the `.env` file with your configuration.

7. Create database migrations:

```bash
python manage.py makemigrations

```

8. Apply database migrations:

```bash
python manage.py migrate

```

## Usage
1. Run the application:

```bash
python manage.py runserver

```

2. Start the Huey task queue worker:

```bash
python manage.py run_huey

```

3. Run Tailwind CSS watcher:

```bash
npm run tw

```

## URLs

| URL Path                     | Description                     |
|------------------------------|---------------------------------|
| `/admin/`                    | Access Django Admin             |
| `/teachers/`                 | List all teachers              |
| `/teachers/<str:pk>/edit/`   | Edit a specific teacher         |
| `/schedules/`                | List all schedules             |
| `/schedules/<str:pk>/`       | View schedule details           |
| `/courses/`                  | List all courses               |
| `/courses/<str:pk>/`         | View course details            |
| `/courses/<str:pk>/edit/`    | Edit a specific course          |
| `/courses/create/new`        | Create a new course            |
| `/login/`                    | Login page                     |
| `/logout/`                   | Logout page                    |

## Accessing the Application
You can view the deployed application at: [course-dashboard.iqbalsyafiq.space](https://course-dashboard.iqbalsyafiq.space)

-  **Login Credentials**:
-  **Username**: `admin`
-  **Password**: `Test@123`

## 
Built️ by Syafiq.