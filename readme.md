# Reddit Post Explorer

The Reddit Post Explorer is a web application built using Python and Streamlit that allows users to browse and explore posts from different subreddits. The application fetches data from the Reddit API and provides a user-friendly interface to view post details, such as title, author, creation time, content, score, number of comments, and subreddit.

## Features

- Select a subreddit from a dropdown menu or enter a custom subreddit name.
- View posts with various content types, including images, videos, self-text, and links.
- Display post information such as author, creation time, score, number of comments, and subreddit.
- Load more posts to explore additional content.
- Responsive and intuitive user interface.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/habitual69/reddit-post-explorer.git
   ```

2. Navigate to the project directory:

   ```bash
   cd reddit-post-explorer
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the following command to start the application:

   ```bash
   streamlit run main.py
   ```

2. Open your web browser and go to `http://localhost:8501` to access the Reddit Post Explorer.

3. Select a subreddit from the dropdown menu or enter a custom subreddit name.

4. Browse through the posts and click on the "Load More" button to fetch additional posts.

5. Interact with the application to view post details and explore different subreddits.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

The Reddit Post Explorer was developed using the following libraries and frameworks:

- Python
- Streamlit
- Requests
- JSON
- datetime
- urllib
- time