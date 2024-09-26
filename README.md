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

### Local / Development

1. Start the Flask development server:
   ```
   small
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. To read a Medium article, replace `https://medium.com` in the article's URL with `http://localhost:5000`

   For example:
   - Original URL: `https://medium.com/@username/article-title-123abc`
   - Small URL: `http://localhost:5000/@username/article-title-123abc`

### Production

For production use, it is recommended to deploy Small using a WSGI server like uWSGI, and behind a reverse proxy like Caddy.

This is a basic guide to deploy Small using uWSGI and Caddy.

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

4. Install uWSGI:
   ```
   pip install uwsgi
   ```

5. Create a `small.ini` file with the following content (adjust as needed):
   ```
   [uwsgi]
   module = small.app:app

   uid = small
   gid = small
   master = true
   processes = 5

   virtualenv = /srv/small/venv/
   chdir = /srv/small/

   http-socket = /tmp/small.sock
   chown-socket = caddy
   ```

6. Start the uWSGI server (consider using a process manager like `systemd`):
   ```
   uwsgi --ini small.ini
   ```

7. Configure Caddy to reverse proxy requests to the uWSGI server:
   ```
   small.example.com {
       reverse_proxy unix//tmp/small.sock
   }
   ```

#### Proxy Fix

If you are using a reverse proxy like Nginx, and it is setting the `X-Forwarded-Host` header instead of passing the `Host` header (you will notice this if the URL displayed on the landing page shows the internal IP and port instead of the domain name), you can use the `ProxyFix` middleware to fix the issue. To enable it, simply set the `PROXY_FIX` environment variable to `1`.

For uWSGI, you can add the following line to the `small.ini` file:
```
env = PROXY_FIX=1
```

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