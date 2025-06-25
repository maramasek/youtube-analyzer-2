# Vytvořím upravenou HTML aplikaci s error handlingem pro API limity
# Ponechám vizuální stránku nezměněnou, ale přidám error handling

html_app = '''<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Channel Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .sidebar {
            background-color: #f8f9fa;
            border-right: 1px solid #dee2e6;
            min-height: 100vh;
        }
        .progress-container {
            display: none;
        }
        .result-card {
            border-left: 4px solid #007bff;
            margin-bottom: 1rem;
        }
        .kids-category { border-left-color: #28a745; }
        .teen-category { border-left-color: #ffc107; }
        .serious-category { border-left-color: #dc3545; }
        .mixed-category { border-left-color: #6c757d; }
        .loading-spinner {
            display: none;
        }
        .api-key-input {
            position: relative;
        }
        .api-key-toggle {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
        }
        .error-alert {
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 sidebar p-3">
                <h4><i class="fas fa-youtube text-danger"></i> YouTube Analyzer</h4>
                
                <!-- API Key Section -->
                <div class="card mt-3">
                    <div class="card-header">
                        <h6><i class="fas fa-key"></i> API Konfigurace</h6>
                    </div>
                    <div class="card-body">
                        <div class="api-key-input">
                            <input type="password" id="apiKey" class="form-control" placeholder="API klíč se načte automaticky">
                            <button type="button" class="api-key-toggle" onclick="toggleApiKey()">
                                <i class="fas fa-eye" id="apiKeyToggle"></i>
                            </button>
                        </div>
                        <small class="text-muted">Klíč se načte ze souboru api_key.txt</small>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="loadApiKey()">
                            <i class="fas fa-sync"></i> Načíst klíč
                        </button>
                    </div>
                </div>

                <!-- Classification Words Section -->
                <div class="card mt-3">
                    <div class="card-header">
                        <h6><i class="fas fa-tags"></i> Klasifikační slova</h6>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label class="form-label">Dětské kanály:</label>
                            <textarea id="kidsWords" class="form-control" rows="3"></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Teen kanály:</label>
                            <textarea id="teenWords" class="form-control" rows="3"></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Seriózní obsah:</label>
                            <textarea id="seriousWords" class="form-control" rows="3"></textarea>
                        </div>
                        <button class="btn btn-sm btn-success" onclick="saveClassificationWords()">
                            <i class="fas fa-save"></i> Uložit slova
                        </button>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div class="col-md-9 p-4">
                <h2><i class="fas fa-chart-line"></i> YouTube Channel Analyzer</h2>
                <p class="text-muted">Analyzujte YouTube kanály a videa pro optimalizaci Google Ads kampaní</p>

                <!-- Error/Success Messages -->
                <div id="messageContainer"></div>

                <!-- Input Section -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h5><i class="fas fa-upload"></i> Zadání dat</h5>
                    </div>
                    <div class="card-body">
                        <ul class="nav nav-tabs" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link active" data-bs-toggle="tab" href="#manual-input">Ruční zadání</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" data-bs-toggle="tab" href="#csv-upload">CSV soubor</a>
                            </li>
                        </ul>

                        <div class="tab-content mt-3">
                            <div id="manual-input" class="tab-pane active">
                                <div class="mb-3">
                                    <label class="form-label">YouTube URL (kanály nebo videa):</label>
                                    <textarea id="urlInput" class="form-control" rows="5" 
                                              placeholder="Zadejte URL oddělené novými řádky:&#10;https://www.youtube.com/@channel&#10;https://www.youtube.com/watch?v=VIDEO_ID&#10;https://youtu.be/VIDEO_ID"></textarea>
                                </div>
                                <button class="btn btn-primary" onclick="analyzeUrls()">
                                    <i class="fas fa-play"></i> Analyzovat URL
                                </button>
                            </div>

                            <div id="csv-upload" class="tab-pane">
                                <div class="mb-3">
                                    <label class="form-label">Vyberte CSV soubor:</label>
                                    <input type="file" id="csvFile" class="form-control" accept=".csv" onchange="handleCsvUpload()">
                                </div>
                                <div id="csvColumnsSection" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label">Vyberte sloupec s YouTube URL:</label>
                                        <select id="csvColumn" class="form-select"></select>
                                    </div>
                                    <button class="btn btn-primary" onclick="analyzeCsv()">
                                        <i class="fas fa-play"></i> Analyzovat CSV
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Progress Section -->
                <div class="progress-container">
                    <div class="card mb-4">
                        <div class="card-body">
                            <h6>Průběh analýzy:</h6>
                            <div class="progress mb-2">
                                <div id="progressBar" class="progress-bar" style="width: 0%"></div>
                            </div>
                            <div id="progressText">Příprava analýzy...</div>
                        </div>
                    </div>
                </div>

                <!-- Results Section -->
                <div id="resultsSection" style="display: none;">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5><i class="fas fa-chart-bar"></i> Výsledky analýzy</h5>
                            <button class="btn btn-outline-success btn-sm" onclick="exportResults()">
                                <i class="fas fa-download"></i> Export CSV
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="results"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Global variables
        let apiKey = '';
        let analysisResults = [];
        let classificationWords = {
            kids: ['kids', 'children', 'toys', 'cartoon', 'animation', 'disney', 'nursery', 'děti', 'dětský', 'hračky', 'pohádky', 'animace', 'animovaný', 'kreslený', 'detský', 'rozprávky', 'hračky', 'detské'],
            teen: ['teen', 'gaming', 'minecraft', 'fortnite', 'tiktok', 'challenge', 'prank', 'vlog', 'youtuberi', 'youtuber', 'gaming', 'hry', 'challenge', 'výzva', 'teenage', 'teenageři', 'mladí', 'mládež'],
            serious: ['news', 'business', 'science', 'technology', 'education', 'documentary', 'research', 'university', 'zprávy', 'věda', 'technologie', 'vzdělávání', 'univerzita', 'výzkum', 'business', 'správy', 'veda', 'technológie', 'vzdelávanie', 'univerzita', 'výskum']
        };

        // Initialize app
        document.addEventListener('DOMContentLoaded', function() {
            loadApiKey();
            loadClassificationWords();
        });

        // Message display functions
        function showMessage(message, type = 'info') {
            const container = document.getElementById('messageContainer');
            const alertClass = type === 'error' ? 'alert-danger' : type === 'success' ? 'alert-success' : 'alert-info';
            
            container.innerHTML = `
                <div class="alert ${alertClass} alert-dismissible fade show error-alert" role="alert">
                    <strong>${type === 'error' ? '🚨 Chyba:' : type === 'success' ? '✅ Úspěch:' : 'ℹ️ Info:'}</strong> ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }

        function clearMessages() {
            document.getElementById('messageContainer').innerHTML = '';
        }

        // API Key management
        function loadApiKey() {
            // Try to load from api_key.txt file
            fetch('api_key.txt')
                .then(response => response.text())
                .then(data => {
                    apiKey = data.trim();
                    if (apiKey && apiKey !== 'YOUR_YOUTUBE_DATA_API_KEY_HERE') {
                        document.getElementById('apiKey').value = apiKey;
                        showMessage('API klíč byl úspěšně načten ze souboru api_key.txt', 'success');
                    } else {
                        showMessage('Nastavte platný API klíč v souboru api_key.txt', 'error');
                    }
                })
                .catch(error => {
                    showMessage('Soubor api_key.txt nenalezen. Zadejte API klíč ručně.', 'error');
                    document.getElementById('apiKey').placeholder = 'Zadejte YouTube Data API klíč';
                });
        }

        function toggleApiKey() {
            const input = document.getElementById('apiKey');
            const toggle = document.getElementById('apiKeyToggle');
            
            if (input.type === 'password') {
                input.type = 'text';
                toggle.className = 'fas fa-eye-slash';
            } else {
                input.type = 'password';
                toggle.className = 'fas fa-eye';
            }
        }

        // Classification words management
        function loadClassificationWords() {
            document.getElementById('kidsWords').value = classificationWords.kids.join(', ');
            document.getElementById('teenWords').value = classificationWords.teen.join(', ');
            document.getElementById('seriousWords').value = classificationWords.serious.join(', ');
        }

        function saveClassificationWords() {
            classificationWords.kids = document.getElementById('kidsWords').value.split(',').map(s => s.trim()).filter(s => s);
            classificationWords.teen = document.getElementById('teenWords').value.split(',').map(s => s.trim()).filter(s => s);
            classificationWords.serious = document.getElementById('seriousWords').value.split(',').map(s => s.trim()).filter(s => s);
            
            showMessage('Klasifikační slova byla úspěšně uložena!', 'success');
        }

        // URL processing
        function extractChannelId(url) {
            const patterns = [
                /youtube\\.com\\/channel\\/([a-zA-Z0-9_-]+)/,
                /youtube\\.com\\/c\\/([a-zA-Z0-9_-]+)/,
                /youtube\\.com\\/user\\/([a-zA-Z0-9_-]+)/,
                /youtube\\.com\\/@([a-zA-Z0-9_-]+)/,
                /youtu\\.be\\/([a-zA-Z0-9_-]+)/,
                /youtube\\.com\\/watch\\?v=([a-zA-Z0-9_-]+)/,
                /youtube\\.com\\/embed\\/([a-zA-Z0-9_-]+)/
            ];

            for (let pattern of patterns) {
                const match = url.match(pattern);
                if (match) {
                    return { id: match[1], type: url.includes('watch') || url.includes('youtu.be') || url.includes('embed') ? 'video' : 'channel' };
                }
            }
            return null;
        }

        // Enhanced YouTube API calls with error handling
        async function getChannelData(channelId) {
            try {
                const response = await fetch(`https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=${channelId}&key=${apiKey}`);
                
                if (response.status === 403) {
                    const errorData = await response.json();
                    if (errorData.error && errorData.error.message.includes('quota')) {
                        showMessage('YouTube API kvóta byla vyčerpána! Zkuste to zítra nebo použijte jiný API klíč.', 'error');
                        return null;
                    } else {
                        showMessage(`API chyba 403: ${errorData.error ? errorData.error.message : 'Neznámá chyba'}`, 'error');
                        return null;
                    }
                } else if (response.status === 400) {
                    const errorData = await response.json();
                    showMessage(`Neplatná URL nebo parametry: ${errorData.error ? errorData.error.message : 'Zkontrolujte formát URL'}`, 'error');
                    return null;
                } else if (!response.ok) {
                    showMessage(`YouTube API chyba ${response.status}. Zkuste to později.`, 'error');
                    return null;
                }
                
                const data = await response.json();
                return data.items ? data.items[0] : null;
            } catch (error) {
                showMessage(`Chyba připojení: ${error.message}`, 'error');
                return null;
            }
        }

        async function getVideoData(videoId) {
            try {
                const response = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${videoId}&key=${apiKey}`);
                
                if (response.status === 403) {
                    const errorData = await response.json();
                    if (errorData.error && errorData.error.message.includes('quota')) {
                        showMessage('YouTube API kvóta byla vyčerpána! Zkuste to zítra nebo použijte jiný API klíč.', 'error');
                        return null;
                    }
                } else if (!response.ok) {
                    showMessage(`YouTube API chyba ${response.status}`, 'error');
                    return null;
                }
                
                const data = await response.json();
                return data.items ? data.items[0] : null;
            } catch (error) {
                showMessage(`Chyba při získávání video dat: ${error.message}`, 'error');
                return null;
            }
        }

        async function getChannelVideos(channelId, maxResults = 5) {
            try {
                const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${channelId}&type=video&order=date&maxResults=${maxResults}&key=${apiKey}`);
                
                if (response.status === 403) {
                    const errorData = await response.json();
                    if (errorData.error && errorData.error.message.includes('quota')) {
                        showMessage('YouTube API kvóta byla vyčerpána!', 'error');
                        return [];
                    }
                } else if (!response.ok) {
                    return [];
                }
                
                const data = await response.json();
                return data.items || [];
            } catch (error) {
                return [];
            }
        }

        // Classification algorithm
        function classifyChannel(channelData, videos) {
            const text = [
                channelData.snippet.title,
                channelData.snippet.description,
                ...videos.map(v => v.snippet.title + ' ' + v.snippet.description)
            ].join(' ').toLowerCase();

            let scores = { kids: 0, teen: 0, serious: 0 };

            // Count keyword matches
            for (let word of classificationWords.kids) {
                scores.kids += (text.match(new RegExp(word.toLowerCase(), 'g')) || []).length;
            }
            for (let word of classificationWords.teen) {
                scores.teen += (text.match(new RegExp(word.toLowerCase(), 'g')) || []).length;
            }
            for (let word of classificationWords.serious) {
                scores.serious += (text.match(new RegExp(word.toLowerCase(), 'g')) || []).length;
            }

            // Normalize scores
            const total = scores.kids + scores.teen + scores.serious || 1;
            scores.kids = Math.round((scores.kids / total) * 100);
            scores.teen = Math.round((scores.teen / total) * 100);
            scores.serious = Math.round((scores.serious / total) * 100);

            // Determine primary category
            let primaryCategory = 'Mixed';
            const maxScore = Math.max(scores.kids, scores.teen, scores.serious);
            if (maxScore > 40) {
                if (scores.kids === maxScore) primaryCategory = 'Kids';
                else if (scores.teen === maxScore) primaryCategory = 'Teen';
                else primaryCategory = 'Serious';
            }

            return { ...scores, primaryCategory };
        }

        // Analysis functions
        async function analyzeUrls() {
            const urls = document.getElementById('urlInput').value.split('\\n').filter(url => url.trim());
            if (urls.length === 0) {
                showMessage('Zadejte alespoň jednu URL', 'error');
                return;
            }

            apiKey = document.getElementById('apiKey').value.trim();
            if (!apiKey) {
                showMessage('Zadejte YouTube Data API klíč', 'error');
                return;
            }

            clearMessages();
            await performAnalysis(urls);
        }

        async function performAnalysis(urls) {
            document.querySelector('.progress-container').style.display = 'block';
            document.getElementById('resultsSection').style.display = 'none';
            analysisResults = [];
            let apiLimitReached = false;

            for (let i = 0; i < urls.length; i++) {
                const url = urls[i].trim();
                if (!url) continue;

                // Update progress
                const progress = Math.round(((i + 1) / urls.length) * 100);
                document.getElementById('progressBar').style.width = progress + '%';
                document.getElementById('progressText').textContent = `Analyzuji ${i + 1}/${urls.length}: ${url}`;

                try {
                    const extracted = extractChannelId(url);
                    if (!extracted) {
                        showMessage(`Neplatná URL: ${url}`, 'error');
                        continue;
                    }

                    let channelId = extracted.id;
                    
                    // If it's a video, get channel ID
                    if (extracted.type === 'video') {
                        const videoData = await getVideoData(extracted.id);
                        if (videoData) {
                            channelId = videoData.snippet.channelId;
                        } else {
                            continue;
                        }
                    }

                    // Get channel data
                    const channelData = await getChannelData(channelId);
                    if (!channelData) {
                        if (document.getElementById('messageContainer').innerHTML.includes('kvóta byla vyčerpána')) {
                            apiLimitReached = true;
                            break;
                        }
                        continue;
                    }

                    // Get recent videos
                    const videos = await getChannelVideos(channelId);

                    // Classify
                    const classification = classifyChannel(channelData, videos);

                    // Store result
                    analysisResults.push({
                        url: url,
                        channelTitle: channelData.snippet.title,
                        subscriberCount: parseInt(channelData.statistics.subscriberCount) || 0,
                        videoCount: parseInt(channelData.statistics.videoCount) || 0,
                        viewCount: parseInt(channelData.statistics.viewCount) || 0,
                        ...classification
                    });

                } catch (error) {
                    showMessage(`Chyba při analýze ${url}: ${error.message}`, 'error');
                }

                // Small delay to respect API limits
                await new Promise(resolve => setTimeout(resolve, 100));
            }

            if (apiLimitReached) {
                showMessage('Analýza byla zastavena kvůli dosažení API limitu. Zpracované výsledky jsou zobrazeny níže.', 'error');
            }

            displayResults();
        }

        // CSV handling
        function handleCsvUpload() {
            const file = document.getElementById('csvFile').files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const csv = e.target.result;
                const lines = csv.split('\\n');
                const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
                
                const columnSelect = document.getElementById('csvColumn');
                columnSelect.innerHTML = '';
                headers.forEach((header, index) => {
                    const option = document.createElement('option');
                    option.value = index;
                    option.textContent = header;
                    columnSelect.appendChild(option);
                });

                document.getElementById('csvColumnsSection').style.display = 'block';
            };
            reader.readAsText(file);
        }

        function analyzeCsv() {
            const file = document.getElementById('csvFile').files[0];
            const columnIndex = parseInt(document.getElementById('csvColumn').value);
            
            if (!file) {
                showMessage('Vyberte CSV soubor', 'error');
                return;
            }

            apiKey = document.getElementById('apiKey').value.trim();
            if (!apiKey) {
                showMessage('Zadejte YouTube Data API klíč', 'error');
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                const csv = e.target.result;
                const lines = csv.split('\\n').slice(1); // Skip header
                const urls = lines.map(line => {
                    const columns = line.split(',');
                    return columns[columnIndex] ? columns[columnIndex].trim().replace(/"/g, '') : '';
                }).filter(url => url);

                clearMessages();
                performAnalysis(urls);
            };
            reader.readAsText(file);
        }

        // Results display
        function displayResults() {
            document.querySelector('.progress-container').style.display = 'none';
            document.getElementById('resultsSection').style.display = 'block';

            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';

            if (analysisResults.length === 0) {
                resultsDiv.innerHTML = '<div class="alert alert-warning">Žádné výsledky k zobrazení</div>';
                return;
            }

            // Summary stats
            const summary = document.createElement('div');
            summary.className = 'row mb-4';
            const kidsCount = analysisResults.filter(r => r.primaryCategory === 'Kids').length;
            const teenCount = analysisResults.filter(r => r.primaryCategory === 'Teen').length;
            const seriousCount = analysisResults.filter(r => r.primaryCategory === 'Serious').length;
            const mixedCount = analysisResults.filter(r => r.primaryCategory === 'Mixed').length;

            summary.innerHTML = `
                <div class="col-md-3">
                    <div class="card text-center border-success">
                        <div class="card-body">
                            <h3 class="text-success">${kidsCount}</h3>
                            <p class="mb-0">Dětské kanály</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center border-warning">
                        <div class="card-body">
                            <h3 class="text-warning">${teenCount}</h3>
                            <p class="mb-0">Teen kanály</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center border-danger">
                        <div class="card-body">
                            <h3 class="text-danger">${seriousCount}</h3>
                            <p class="mb-0">Seriózní kanály</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center border-secondary">
                        <div class="card-body">
                            <h3 class="text-secondary">${mixedCount}</h3>
                            <p class="mb-0">Smíšené kanály</p>
                        </div>
                    </div>
                </div>
            `;
            resultsDiv.appendChild(summary);

            // Detailed results
            analysisResults.forEach((result, index) => {
                const resultCard = document.createElement('div');
                resultCard.className = `card result-card ${result.primaryCategory.toLowerCase()}-category mb-3`;
                
                resultCard.innerHTML = `
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <h6 class="card-title">${result.channelTitle}</h6>
                                <p class="card-text">
                                    <small class="text-muted">
                                        <i class="fas fa-users"></i> ${result.subscriberCount.toLocaleString()} odběratelů | 
                                        <i class="fas fa-video"></i> ${result.videoCount.toLocaleString()} videí | 
                                        <i class="fas fa-eye"></i> ${result.viewCount.toLocaleString()} zhlédnutí
                                    </small>
                                </p>
                                <span class="badge bg-primary">${result.primaryCategory}</span>
                            </div>
                            <div class="col-md-4">
                                <div class="progress mb-1" style="height: 15px;">
                                    <div class="progress-bar bg-success" style="width: ${result.kids}%">${result.kids}% Kids</div>
                                </div>
                                <div class="progress mb-1" style="height: 15px;">
                                    <div class="progress-bar bg-warning" style="width: ${result.teen}%">${result.teen}% Teen</div>
                                </div>
                                <div class="progress" style="height: 15px;">
                                    <div class="progress-bar bg-danger" style="width: ${result.serious}%">${result.serious}% Serious</div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                resultsDiv.appendChild(resultCard);
            });
        }

        // Export functionality
        function exportResults() {
            if (analysisResults.length === 0) {
                showMessage('Žádné výsledky k exportu', 'error');
                return;
            }

            const headers = ['URL', 'Channel Title', 'Subscribers', 'Videos', 'Views', 'Primary Category', 'Kids %', 'Teen %', 'Serious %'];
            const csvContent = [
                headers.join(','),
                ...analysisResults.map(result => [
                    result.url,
                    `"${result.channelTitle}"`,
                    result.subscriberCount,
                    result.videoCount,
                    result.viewCount,
                    result.primaryCategory,
                    result.kids,
                    result.teen,
                    result.serious
                ].join(','))
            ].join('\\n');

            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `youtube_analysis_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            showMessage('Výsledky byly úspěšně exportovány!', 'success');
        }
    </script>
</body>
</html>'''

# Uložím upravenou HTML aplikaci
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_app)

print("✅ Upravená HTML aplikace vytvořena: index.html")
print("   - Přidán error handling pro API limity")
print("   - Vylepšené zobrazování chybových zpráv")
print("   - Zachován původní vizuální design")