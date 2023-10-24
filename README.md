# Django Reservations App

The Django Reservations App is a web application that allows listing owners to create listings and manage reservations for those listings. The app includes features for checking availability, creating reservations, and generating reports in multiple formats.

## Installation

To install the Django Reservations App, follow these steps:

1. Install the required packages:

   ```bash
   cd real_state
   pip install -r requirements.txt
   ```
2. Run the migrations to create the database schema:

   ```bash
   python manage.py migrate
   ```
3. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

The Django Reservations App includes the following endpoints:

- `/listings/`: Create a new listing or retrieve a list of all listings.
- `/listings/{listing_id}/`: Retrieve a specific listing.
- `/listings/{listing_id}/reservations/`: Create a new reservation or retrieve a list of all reservations for a specific listing.
- `/listings/{listing_id}/availability/`: Check the availability of a specific listing.
- `/report/`: Generate a reservation report in PDF or CSV format.

To use these endpoints, you can send HTTP requests to the appropriate URL using your preferred HTTP client (e.g., curl, httpie, or a web browser).

### Create a new listing

```bash
curl --location --request POST 'http://localhost:8000/listings/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Cozy Cabin",
    "description": "A cozy cabin in the woods.",
    "price": 100.00
}'
```

### Retrieve a list of all listings

```bash
curl --location --request GET 'http://localhost:8000/listings/'
```

### Retrieve a specific listing

```bash
curl --location --request GET 'http://localhost:8000/listings/1/'
```

### Create a new reservation

```bash
curl --location --request POST 'http://localhost:8000/listings/1/reservations/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Ali",
    "start_time": "2023-06-01T10:00:00",
    "end_time": "2023-06-05T12:00:00"
}'
```

### Retrieve a list of all reservations for a specific listing
In the following command instead of 1 use the listing ID

```bash
curl --location --request GET 'http://localhost:8000/listings/1/reservations/'
```

### Check the availability of a specific listing for a given date range
In the following command instead of 1 use the listing ID
```bash
curl --location --request POST 'http://localhost:8000/listings/1/availability/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'start_time=2023-06-01T10:00:00' \
--data-urlencode 'end_time=2023-06-05T12:00:00'
```

### Generate a reservation report in JSON, HTML or PDF format

#### JSON

```bash
curl --location --request GET 'http://localhost:8000/report/'
```

#### HTML

```bash
curl --location --request GET 'http://localhost:8000/report/?format=html'
```

#### PDF

```bash
curl --location --request GET 'http://localhost:8000/report/?format=pdf'
```

## Authentication

The Django Reservations App does not currently require authentication for any of its endpoints. However, you can add authentication and permission classes to the REST
