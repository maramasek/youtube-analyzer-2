// YouTube Channel Analyzer JavaScript

class YouTubeAnalyzer {
    constructor() {
        this.apiKey = '';
        this.currentData = [];
        this.csvData = [];
        this.results = [];
        
        // Keywords for classification
        this.keywords = {
            kids: ["kids", "children", "baby", "toy", "cartoon", "animation", "nursery", "disney", "peppa", "elsa", "minecraft for kids", "cocomelon", "finger family", "abc song", "color song", "preschool", "toddler", "learning", "educational", "songs for kids", "kids tv", "little", "cute", "fun", "playground"],
            teen: ["teen", "gaming", "fortnite", "roblox", "tiktok", "challenge", "prank", "makeup", "fashion", "kpop", "bts", "dance", "trending", "viral", "reactions", "youtube shorts", "instagram", "snapchat", "school", "high school", "college", "teenagers", "youth", "young"],
            serious: ["news", "business", "science", "technology", "research", "professional", "education", "documentary", "analysis", "finance", "politics", "health", "cooking", "fitness", "tutorial", "review", "how to", "guide", "tips", "advice", "expert", "course", "training", "conference"]
        };
        
        this.sampleUrls = [
            "https://www.youtube.com/channel/UCbCmjCuTUZos6Inko4u57UQ",
            "https://www.youtube.com/@CoComelon", 
            "https://www.youtube.com/watch?v=YQHsXMglC9A",
            "https://www.youtube.com/channel/UCsooa4yRKGN_zEE8iknghZA",
            "https://youtu.be/dQw4w9WgXcQ"
        ];
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        // Note: localStorage is not available in sandbox, so we skip loading saved API key
    }
    
    bindEvents() {
        // API Key events
        document.getElementById('toggleApiKey').addEventListener('click', () => this.toggleApiKeyVisibility());
        document.getElementById('saveApiKey').addEventListener('click', () => this.saveApiKey());
        
        // Tab events
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Input events
        document.getElementById('loadSampleData').addEventListener('click', () => this.loadSampleData());
        document.getElementById('csvFile').addEventListener('change', (e) => this.handleCsvUpload(e));
        document.getElementById('csvColumn').addEventListener('change', () => this.updateCsvPreview());
        
        // Analysis and export
        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeChannels());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportResults());
        
        // Filtering
        document.getElementById('categoryFilter').addEventListener('change', () => this.filterResults());
    }
    
    toggleApiKeyVisibility() {
        const input = document.getElementById('apiKey');
        const button = document.getElementById('toggleApiKey');
        
        if (input.type === 'password') {
            input.type = 'text';
            button.textContent = 'Skrýt';
        } else {
            input.type = 'password';
            button.textContent = 'Zobrazit';
        }
    }
    
    saveApiKey() {
        const apiKey = document.getElementById('apiKey').value.trim();
        const statusEl = document.getElementById('apiKeyStatus');
        
        if (!apiKey) {
            this.showStatus(statusEl, 'Zadejte API klíč', 'error');
            return;
        }
        
        this.apiKey = apiKey;
        this.showStatus(statusEl, 'API klíč byl uložen', 'success');
        this.updateAnalyzeButton();
    }
    
    showStatus(element, message, type) {
        element.innerHTML = `<div class="${type === 'success' ? 'success-message' : 'error-message'}">${message}</div>`;
        setTimeout(() => {
            element.innerHTML = '';
        }, 3000);
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.add('hidden');
        });
        document.getElementById(`${tabName}-tab`).classList.remove('hidden');
        
        this.updateAnalyzeButton();
    }
    
    loadSampleData() {
        document.getElementById('manualUrls').value = this.sampleUrls.join('\n');
        this.updateAnalyzeButton();
    }
    
    handleCsvUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            const csv = e.target.result;
            Papa.parse(csv, {
                header: true,
                complete: (results) => {
                    this.csvData = results.data;
                    this.populateCsvColumns(results.meta.fields);
                    this.updateAnalyzeButton();
                },
                error: (error) => {
                    this.showError('Chyba při načítání CSV: ' + error.message);
                }
            });
        };
        reader.readAsText(file);
    }
    
    populateCsvColumns(fields) {
        const select = document.getElementById('csvColumn');
        select.innerHTML = '<option value="">Vyberte sloupec...</option>';
        
        fields.forEach(field => {
            const option = document.createElement('option');
            option.value = field;
            option.textContent = field;
            select.appendChild(option);
            
            // Auto-select likely URL columns
            const lowerField = field.toLowerCase();
            if (lowerField.includes('url') || lowerField.includes('placement') || lowerField.includes('website')) {
                option.selected = true;
            }
        });
        
        this.updateCsvPreview();
    }
    
    updateCsvPreview() {
        const column = document.getElementById('csvColumn').value;
        const previewEl = document.getElementById('csvPreview');
        
        if (!column || !this.csvData.length) {
            previewEl.innerHTML = '';
            return;
        }
        
        const urls = this.csvData
            .map(row => row[column])
            .filter(url => this.isYouTubeUrl(url))
            .slice(0, 10);
        
        if (urls.length === 0) {
            previewEl.innerHTML = '<div class="error-message">Ve vybraném sloupci nebyly nalezeny YouTube URL</div>';
            return;
        }
        
        const table = document.createElement('table');
        table.className = 'csv-preview';
        table.innerHTML = `
            <thead>
                <tr><th>Nalezené YouTube URL (prvních 10)</th></tr>
            </thead>
            <tbody>
                ${urls.map(url => `<tr><td>${url}</td></tr>`).join('')}
            </tbody>
        `;
        
        previewEl.innerHTML = '';
        previewEl.appendChild(table);
    }
    
    updateAnalyzeButton() {
        const btn = document.getElementById('analyzeBtn');
        const hasApiKey = this.apiKey.trim() !== '';
        const hasData = this.hasInputData();
        
        btn.disabled = !hasApiKey || !hasData;
    }
    
    hasInputData() {
        const activeTab = document.querySelector('.tab-content:not(.hidden)').id;
        
        if (activeTab === 'manual-tab') {
            const urls = document.getElementById('manualUrls').value.trim();
            return urls.length > 0;
        } else if (activeTab === 'csv-tab') {
            const column = document.getElementById('csvColumn').value;
            return column && this.csvData.length > 0;
        }
        
        return false;
    }
    
    async analyzeChannels() {
        const urls = this.getUrlsToAnalyze();
        if (urls.length === 0) {
            this.showError('Nebyly nalezeny žádné platné YouTube URL');
            return;
        }
        
        this.showProgress(true);
        this.results = [];
        
        try {
            for (let i = 0; i < urls.length; i++) {
                const url = urls[i];
                const progress = ((i + 1) / urls.length) * 100;
                this.updateProgress(progress, `Analyzuji ${i + 1}/${urls.length}: ${url}`);
                
                try {
                    const result = await this.analyzeUrl(url);
                    this.results.push(result);
                } catch (error) {
                    console.error('Error analyzing URL:', url, error);
                    this.results.push({
                        url: url,
                        error: error.message || 'Neznámá chyba'
                    });
                }
                
                // Add delay to avoid rate limits
                if (i < urls.length - 1) {
                    await this.delay(200);
                }
            }
            
            this.displayResults();
            this.showProgress(false);
            
        } catch (error) {
            this.showError('Chyba při analýze: ' + error.message);
            this.showProgress(false);
        }
    }
    
    getUrlsToAnalyze() {
        const activeTab = document.querySelector('.tab-content:not(.hidden)').id;
        
        if (activeTab === 'manual-tab') {
            const text = document.getElementById('manualUrls').value.trim();
            return text.split('\n')
                .map(line => line.trim())
                .filter(line => this.isYouTubeUrl(line));
        } else if (activeTab === 'csv-tab') {
            const column = document.getElementById('csvColumn').value;
            return this.csvData
                .map(row => row[column])
                .filter(url => this.isYouTubeUrl(url));
        }
        
        return [];
    }
    
    async analyzeUrl(url) {
        const urlType = this.getUrlType(url);
        let channelId = null;
        let videoId = null;
        
        if (urlType === 'video') {
            videoId = this.extractVideoId(url);
            const videoData = await this.getVideoInfo(videoId);
            channelId = videoData.snippet.channelId;
        } else {
            channelId = await this.extractChannelId(url);
        }
        
        const channelData = await this.getChannelInfo(channelId);
        const channelVideos = await this.getChannelVideos(channelId);
        
        const classification = this.classifyContent(channelData, channelVideos);
        
        return {
            url: url,
            type: urlType === 'video' ? 'Video' : 'Kanál',
            channelName: channelData.snippet.title,
            subscriberCount: this.formatSubscriberCount(channelData.statistics.subscriberCount),
            category: classification.category,
            kidsScore: classification.scores.kids,
            teenScore: classification.scores.teen,
            seriousScore: classification.scores.serious,
            madeForKids: channelData.status?.madeForKids || false,
            channelId: channelId
        };
    }
    
    getUrlType(url) {
        return url.includes('/watch?v=') || url.includes('youtu.be/') ? 'video' : 'channel';
    }
    
    extractVideoId(url) {
        const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
    }
    
    async extractChannelId(url) {
        // Handle different channel URL formats
        if (url.includes('/channel/')) {
            return url.split('/channel/')[1].split('?')[0];
        }
        
        if (url.includes('/@')) {
            const handle = url.split('/@')[1].split('?')[0];
            return await this.getChannelIdByHandle(handle);
        }
        
        if (url.includes('/c/') || url.includes('/user/')) {
            const username = url.split('/').pop().split('?')[0];
            return await this.getChannelIdByUsername(username);
        }
        
        throw new Error('Nepodařilo se extrahovat ID kanálu z URL');
    }
    
    async getChannelIdByHandle(handle) {
        const response = await fetch(
            `https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q=${handle}&key=${this.apiKey}`
        );
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error.message);
        }
        
        if (data.items && data.items.length > 0) {
            return data.items[0].snippet.channelId;
        }
        
        throw new Error('Kanál nebyl nalezen');
    }
    
    async getChannelIdByUsername(username) {
        const response = await fetch(
            `https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername=${username}&key=${this.apiKey}`
        );
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error.message);
        }
        
        if (data.items && data.items.length > 0) {
            return data.items[0].id;
        }
        
        // Fallback to search
        return await this.getChannelIdByHandle(username);
    }
    
    async getVideoInfo(videoId) {
        const response = await fetch(
            `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${videoId}&key=${this.apiKey}`
        );
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error.message);
        }
        
        if (!data.items || data.items.length === 0) {
            throw new Error('Video nebylo nalezeno');
        }
        
        return data.items[0];
    }
    
    async getChannelInfo(channelId) {
        const response = await fetch(
            `https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,status&id=${channelId}&key=${this.apiKey}`
        );
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error.message);
        }
        
        if (!data.items || data.items.length === 0) {
            throw new Error('Kanál nebyl nalezen');
        }
        
        return data.items[0];
    }
    
    async getChannelVideos(channelId) {
        const response = await fetch(
            `https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${channelId}&type=video&order=date&maxResults=10&key=${this.apiKey}`
        );
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error.message);
        }
        
        return data.items || [];
    }
    
    classifyContent(channelData, videos) {
        const textToAnalyze = [
            channelData.snippet.title,
            channelData.snippet.description,
            ...videos.map(video => video.snippet.title + ' ' + video.snippet.description)
        ].join(' ').toLowerCase();
        
        const scores = {
            kids: this.calculateScore(textToAnalyze, this.keywords.kids),
            teen: this.calculateScore(textToAnalyze, this.keywords.teen),
            serious: this.calculateScore(textToAnalyze, this.keywords.serious)
        };
        
        const maxScore = Math.max(scores.kids, scores.teen, scores.serious);
        let category = 'Smíšené';
        
        if (maxScore > 0) {
            if (scores.kids === maxScore) category = 'Dětské';
            else if (scores.teen === maxScore) category = 'Teen';
            else if (scores.serious === maxScore) category = 'Seriózní';
        }
        
        return { category, scores };
    }
    
    calculateScore(text, keywords) {
        let score = 0;
        keywords.forEach(keyword => {
            const regex = new RegExp('\\b' + keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi');
            const matches = text.match(regex);
            if (matches) {
                score += matches.length;
            }
        });
        return Math.min(score * 10, 100); // Cap at 100%
    }
    
    displayResults() {
        const tbody = document.querySelector('#resultsTable tbody');
        tbody.innerHTML = '';
        
        this.results.forEach(result => {
            if (result.error) {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td class="url-display">${result.url}</td>
                    <td colspan="8" class="error-message">Chyba: ${result.error}</td>
                `;
                return;
            }
            
            const row = tbody.insertRow();
            row.innerHTML = `
                <td class="url-display" title="${result.url}">${result.url}</td>
                <td>${result.type}</td>
                <td>${result.channelName}</td>
                <td class="subscriber-count">${result.subscriberCount}</td>
                <td><span class="category-badge category-badge--${this.getCategoryClass(result.category)}">${result.category}</span></td>
                <td>${result.kidsScore}%</td>
                <td>${result.teenScore}%</td>
                <td>${result.seriousScore}%</td>
                <td class="made-for-kids made-for-kids--${result.madeForKids ? 'yes' : 'no'}">${result.madeForKids ? 'Ano' : 'Ne'}</td>
            `;
        });
        
        document.getElementById('resultsSection').classList.remove('hidden');
        document.getElementById('exportBtn').disabled = false;
    }
    
    getCategoryClass(category) {
        const map = {
            'Dětské': 'kids',
            'Teen': 'teen', 
            'Seriózní': 'serious',
            'Smíšené': 'mixed'
        };
        return map[category] || 'mixed';
    }
    
    filterResults() {
        const filter = document.getElementById('categoryFilter').value;
        const rows = document.querySelectorAll('#resultsTable tbody tr');
        
        rows.forEach(row => {
            if (!filter) {
                row.style.display = '';
                return;
            }
            
            const categoryCell = row.cells[4];
            if (categoryCell && categoryCell.textContent.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    
    exportResults() {
        const csvData = this.results
            .filter(result => !result.error)
            .map(result => ({
                'URL': result.url,
                'Typ': result.type,
                'Název kanálu': result.channelName,
                'Odběratelé': result.subscriberCount,
                'Kategorie': result.category,
                'Dětské %': result.kidsScore,
                'Teen %': result.teenScore,
                'Seriózní %': result.seriousScore,
                'Made for Kids': result.madeForKids ? 'Ano' : 'Ne'
            }));
        
        const csv = Papa.unparse(csvData);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        link.setAttribute('href', url);
        link.setAttribute('download', `youtube-analyza-${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    formatSubscriberCount(count) {
        const num = parseInt(count);
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
    
    isYouTubeUrl(url) {
        if (!url || typeof url !== 'string') return false;
        return /^https?:\/\/(www\.)?youtube\.com\/|^https?:\/\/youtu\.be\//.test(url.trim());
    }
    
    showProgress(show) {
        const section = document.getElementById('progressSection');
        if (show) {
            section.classList.remove('hidden');
        } else {
            section.classList.add('hidden');
        }
    }
    
    updateProgress(percent, text) {
        document.getElementById('progressFill').style.width = percent + '%';
        document.getElementById('progressText').textContent = text;
    }
    
    showError(message) {
        const errorEl = document.getElementById('errorMessages');
        errorEl.innerHTML = `<div class="error-message">${message}</div>`;
        setTimeout(() => {
            errorEl.innerHTML = '';
        }, 5000);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new YouTubeAnalyzer();
});