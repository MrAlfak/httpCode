let codes = [];
let translations = {};
const resultsEl = document.getElementById('results');
const searchEl = document.getElementById('search');
const langSelect = document.getElementById('lang-select');

// Initial load
async function init() {
    try {
        const response = await fetch('/codes.json');
        codes = await response.json();
        await loadTranslations('en'); // Default to English
        render();
    } catch (err) {
        console.error('Failed to load codes:', err);
    }
}

// Load translations for selected language
async function loadTranslations(lang) {
    try {
        const response = await fetch(`/i18n/${lang}.json`);
        translations = await response.json();
    } catch (err) {
        console.warn(`Could not load translations for ${lang}:`, err);
        translations = {};
    }
}

// Render the grid
function render() {
    const query = searchEl.value.toLowerCase();
    
    resultsEl.innerHTML = '';
    
    const filteredCodes = codes.filter(c => {
        const codeStr = String(c.code);
        const phrase = (translations[codeStr]?.phrase || c.phrase).toLowerCase();
        const desc = (translations[codeStr]?.description || c.description).toLowerCase();
        
        return codeStr.includes(query) || phrase.includes(query) || desc.includes(query);
    });

    filteredCodes.forEach(c => {
        const codeStr = String(c.code);
        const phrase = translations[codeStr]?.phrase || c.phrase;
        const desc = translations[codeStr]?.description || c.description;
        
        const card = document.createElement('article');
        card.className = 'card';
        card.setAttribute('role', 'article');
        card.setAttribute('aria-label', `HTTP ${c.code}: ${phrase}`);
        
        const badgeClass = `badge-${c.class.substring(0, 3)}`;
        
        card.innerHTML = `
            <div class="code">
                HTTP ${c.code}
                <span class="badge ${badgeClass}">${c.class.split(' ')[0]}</span>
            </div>
            <h2 class="phrase">${phrase}</h2>
            <p class="description">${desc}</p>
            ${c.mdn_link ? `<a href="${c.mdn_link}" target="_blank" rel="noopener noreferrer" class="mdn-link">Read MDN Docs &rarr;</a>` : ''}
        `;
        resultsEl.appendChild(card);
    });
}

// Event Listeners
searchEl.addEventListener('input', render);
langSelect.addEventListener('change', async (e) => {
    await loadTranslations(e.target.value);
    render();
});

// Start the app
init();
