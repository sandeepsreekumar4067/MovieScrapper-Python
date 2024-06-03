# Movie Search Flask App

This Flask application allows users to search for movies on Rotten Tomatoes and retrieve detailed information about the first movie in the search results, including the title, year, cast, audience score, ratings, and description. The application uses Selenium to scrape data from the Rotten Tomatoes website.

## Features

- Search for a movie on Rotten Tomatoes.
- Retrieve detailed information about the first movie in the search results.
- Get a list of related movie suggestions.
- JSON responses with detailed movie information and related suggestions.
- Execution time logging.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/sandeepsreekumar4067/MovieScrapper-Python
    cd moviesearch-flask-app
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add the Rotten Tomatoes URL:

    ```plaintext
    URL=https://www.rottentomatoes.com/
    ```

## Running the Application

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. The application will start running on `http://127.0.0.1:5000`.

## Usage

To search for a movie, send a GET request to the `/search_movie` endpoint with the movie title as a query parameter. For example, using `curl`:

```bash
curl "http://127.0.0.1:5000/search_movie?movie=Inception"
