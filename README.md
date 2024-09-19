# Small

Small is an alternative frontend for Medium articles, built with Flask. It allows users to read Medium articles without the clutter and distractions of the original Medium interface.

## Features

- Clean, minimalist interface for reading Medium articles
- Fetches article content directly from Medium's GraphQL API
- Parses and displays article content, including text and basic formatting
- Proxies embedded images and GitHub gists
- Prevents loading iframes without user consent
- Responsive design for comfortable reading on various devices

## Installation

1. Clone the repository:
   ```
   git clone https://git.private.coffee/PrivateCoffee/small.git
   cd small
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the package:
   ```
   pip install .
   ```

## Usage

1. Start the Flask development server:
   ```
   small
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. To read a Medium article, replace `https://medium.com` in the article's URL with `http://localhost:5000`

   For example:
   - Original URL: `https://medium.com/@username/article-title-123abc`
   - Small URL: `http://localhost:5000/@username/article-title-123abc`


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [Scribe](https://git.sr.ht/~edwardloveall/scribe) project built with Crystal and Lucky
- Thanks to Medium for providing the content through their API

## Disclaimer

This project is not affiliated with, endorsed, or sponsored by Medium. It's an independent project created to provide an alternative reading experience for Medium content.