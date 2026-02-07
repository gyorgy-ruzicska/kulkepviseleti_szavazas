# Foreign Representation Voting 2026 - Finder 🗳️📍

**Foreign Representation Voting 2026 - Finder** is a modern web application designed to help Hungarian citizens abroad find the nearest voting location for the 2026 parliamentary elections.

## ✨ Key Features

- **🏠 Address Search**: Precise address search with autocomplete (powered by Nominatim API).
- **📍 "Find My Location"**: Instantly determines your current location and lists the nearest representations with a single click.
- **🗺️ Interactive Map**: Leaflet.js-based map visually displaying your position and voting locations.
- **♿ Accessibility Filter**: Option to filter for wheelchair-accessible locations only.
- **📏 Distance Calculation**: Calculates the straight-line distance between you and the representations.
- **🔗 Google Maps Integration**: Direct route planning to the selected representation via Google Maps.
- **📋 Copy Address**: Copy the representation's address to the clipboard with one click.

## 🛠️ Technologies

The project is built on modern web technologies without heavy external frameworks (like React or Vue) to ensure maximum performance and simplicity:

- **HTML5 & CSS3**: Modern, responsive design (Glassmorphism style).
- **JavaScript (ES6+)**: Clean, modular JavaScript code.
- **[Leaflet.js](https://leafletjs.com/)**: Open-source mapping library.
- **[OpenStreetMap](https://www.openstreetmap.org/) & [Nominatim API](https://nominatim.org/)**: Map data and geocoding.
- **[Lucide Icons](https://lucide.dev/)**: Lightweight, beautiful icons.

## 🚀 Local Setup

No complex installation is needed to run the project as it consists of static files.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/kulkepviseleti-szavazas-2026.git
    cd kulkepviseleti-szavazas-2026
    ```

2.  **Run on a local server:**
    Since modern browsers may restrict certain features (e.g., fetch API) over the `file://` protocol for security reasons, using a simple HTTP server is recommended.

    With Python 3:
    ```bash
    python3 -m http.server
    ```

    Or with Node.js `http-server`:
    ```bash
    npx http-server .
    ```

3.  **Open in browser:**
    Visit `http://localhost:8000` (or the address shown in the terminal).

## 🤝 Contribution

We welcome any ideas or bug fixes! Open an Issue or send a Pull Request.

## 📄 License

This project is open source.

---
*Made in the spirit of democracy. 🇭🇺*
