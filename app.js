let map;
let markers = [];
let userMarker;

// Initialize the map on load
window.addEventListener('DOMContentLoaded', () => {
    initMap();
    setupEventListeners();
});

function initMap() {
    // Default view: Europe center
    map = L.map('map').setView([47.4979, 19.0402], 3);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

function setupEventListeners() {
    const searchBtn = document.getElementById('searchBtn');
    const addressInput = document.getElementById('addressInput');
    const autocompleteResults = document.getElementById('autocomplete-results');

    searchBtn.addEventListener('click', handleSearch);
    addressInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
            autocompleteResults.innerHTML = '';
        }
    });

    // Autocomplete Logic
    let debounceTimer;
    addressInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const query = addressInput.value.trim();

        if (query.length < 3) {
            autocompleteResults.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`);
                const data = await response.json();

                autocompleteResults.innerHTML = '';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'autocomplete-item';
                    div.textContent = item.display_name;
                    div.addEventListener('click', () => {
                        addressInput.value = item.display_name;
                        autocompleteResults.innerHTML = '';
                        handleSearch();
                    });
                    autocompleteResults.appendChild(div);
                });
            } catch (error) {
                console.error('Autocomplete error:', error);
            }
        }, 300);
    });

    // Close autocomplete when clicking outside
    document.addEventListener('click', (e) => {
        if (!addressInput.contains(e.target) && !autocompleteResults.contains(e.target)) {
            autocompleteResults.innerHTML = '';
        }
    });

    // Filter listener
    document.getElementById('accessibleFilter').addEventListener('change', () => {
        if (document.getElementById('addressInput').value) {
            handleSearch();
        }
    });
}

async function handleSearch() {
    const address = document.getElementById('addressInput').value;
    if (!address) return;

    showLoading(true);

    try {
        const userCoords = await geocodeUserAddress(address);
        if (userCoords) {
            const closest = calculateClosest(userCoords);
            displayResults(closest);
            updateMap(userCoords, closest);
        } else {
            alert('A megadott cím nem található. Kérlek, próbáld meg pontosabban!');
        }
    } catch (error) {
        console.error(error);
        alert('Hiba történt a keresés során.');
    } finally {
        showLoading(false);
    }
}

async function geocodeUserAddress(address) {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`);
    const data = await response.json();
    if (data && data.length > 0) {
        return {
            lat: parseFloat(data[0].lat),
            lon: parseFloat(data[0].lon)
        };
    }
    return null;
}

function calculateClosest(userCoords) {
    const isOnlyAccessible = document.getElementById('accessibleFilter').checked;

    // KULKEPVISELETEK is loaded from data.js
    const results = KULKEPVISELETEK
        .filter(loc => !isOnlyAccessible || loc["Akadálymentesség"] === "akadálymentes")
        .map(loc => {
            if (loc.lat === null || loc.lon === null) return { ...loc, distance: Infinity };
            const d = haversineDistance(userCoords.lat, userCoords.lon, loc.lat, loc.lon);
            return { ...loc, distance: d };
        });

    return results.sort((a, b) => a.distance - b.distance).slice(0, 3);
}

function haversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function displayResults(closest) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    closest.forEach((loc, index) => {
        const isAccessible = loc["Akadálymentesség"] === "akadálymentes";
        const card = document.createElement('div');
        card.className = 'card';
        card.style.animationDelay = `${index * 0.1}s`;

        const gmapsLink = `https://www.google.com/maps/search/?api=1&query=${loc.lat}%2C${loc.lon}`;

        card.innerHTML = `
            <div class="card-header">
                <span class="rank">#${index + 1}</span>
                <span class="distance">${Math.round(loc.distance).toLocaleString()} km</span>
            </div>
            <h3>${loc["Ország, település"]}</h3>
            <div class="address">${loc["Külképviselet címe"]}</div>
            <div style="margin-bottom: 1rem;">
                <span class="badge ${isAccessible ? 'badge-accessible' : 'badge-not-accessible'}">
                    <i data-lucide="${isAccessible ? 'check-circle' : 'alert-circle'}" style="width:12px; height:12px; vertical-align:middle;"></i>
                    ${loc["Akadálymentesség"]}
                </span>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;">
                <p><strong>Szavazás ideje:</strong> ${loc["A szavazás ideje"]}</p>
                <p><strong>Határidő:</strong> ${loc["Kérelem benyújtásának határideje"]}</p>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <a href="${gmapsLink}" target="_blank" class="maps-link">
                    <i data-lucide="map-pin" style="width:14px; height:14px;"></i>
                    Megnyitás Google Mapsben
                </a>
                <button class="copy-btn" data-address="${loc["Külképviselet címe"]}">
                    <i data-lucide="copy" style="width:14px; height:14px;"></i>
                    Cím másolása
                </button>
            </div>
        `;

        const copyBtn = card.querySelector('.copy-btn');
        copyBtn.addEventListener('click', () => copyToClipboard(loc["Külképviselet címe"]));

        resultsDiv.appendChild(card);
    });

    lucide.createIcons();
}

function updateMap(userCoords, closest) {
    // Clear previous markers
    markers.forEach(m => map.removeLayer(m));
    if (userMarker) map.removeLayer(userMarker);
    markers = [];

    // Add user marker
    userMarker = L.marker([userCoords.lat, userCoords.lon], {
        icon: L.divIcon({
            className: 'user-marker',
            html: '<div style="background-color:#e74c3c; width:12px; height:12px; border-radius:50%; border:2px solid white; box-shadow:0 0 10px rgba(0,0,0,0.3);"></div>'
        })
    }).addTo(map).bindPopup('Te itt vagy').openPopup();

    // Add result markers
    const group = [L.latLng(userCoords.lat, userCoords.lon)];

    closest.forEach((loc, index) => {
        const gmapsLink = `https://www.google.com/maps/search/?api=1&query=${loc.lat}%2C${loc.lon}`;
        const m = L.marker([loc.lat, loc.lon]).addTo(map)
            .bindPopup(`
                <b>#${index + 1}: ${loc["Ország, település"]}</b><br>
                ${loc["Külképviselet címe"]}<br><br>
                <a href="${gmapsLink}" target="_blank" style="color:var(--accent-color); font-weight:bold; text-decoration:none;">
                    📍 Google Maps megnyitása
                </a>
            `);
        markers.push(m);
        group.push(L.latLng(loc.lat, loc.lon));
    });

    const bounds = L.latLngBounds(group);
    map.fitBounds(bounds, { padding: [50, 50] });
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('results').style.opacity = show ? '0.3' : '1';
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast();
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}

function showToast() {
    const toast = document.getElementById('toast');
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}
