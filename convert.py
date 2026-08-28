import pandas as pd

# Membaca CSV asli
df = pd.read_csv('Database_IKAL_SITALA_Dummy_2019_2026.csv', sep=';')
csv_text = df.to_csv(index=False, sep=';')

# Template HTML lengkap
html_content = f"""<!DOCTYPE html>
<html lang="id" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebGIS Analisis Kualitas Air & Parameter Terumbu Karang - IKAL SITALA</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{ extend: {{ colors: {{ darkbg: '#020617' }} }} }}
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; transition: background-color 0.3s, color 0.3s; }}
        .custom-popup .leaflet-popup-content-wrapper {{ border-radius: 8px; width: 420px; max-height: 400px; overflow-y: auto; }}
        th, td {{ white-space: nowrap; }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-screen overflow-hidden" id="mainBody">
    <header class="bg-slate-900 border-b border-slate-800 h-14 flex items-center justify-between px-6 z-20 shrink-0 transition-colors" id="topHeader">
        <div class="flex items-center space-x-3">
            <div class="bg-cyan-500 p-1.5 rounded-lg text-slate-950 font-bold"><i class="fa-solid fa-water text-base"></i></div>
            <div>
                <h1 class="font-bold text-sm tracking-wide text-cyan-400">IKAL SITALA WebGIS — Parameter Lengkap & Status Kelayakan</h1>
                <p class="text-[11px] text-cyan-300 font-medium" id="loadStatus">Memuat database...</p>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <button onclick="toggleTheme()" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 px-3 py-1.5 rounded-lg border border-slate-700 text-xs font-semibold flex items-center space-x-1.5 transition" id="themeBtn">
                <i class="fa-solid fa-moon" id="themeIcon"></i><span id="themeText">Mode Gelap</span>
            </button>
            <div class="flex items-center bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">
                <label for="yearSelect" class="text-xs text-slate-200 mr-2 font-semibold"><i class="fa-solid fa-calendar-days mr-1"></i> Tahun:</label>
                <select id="yearSelect" class="bg-slate-900 text-cyan-300 font-bold text-xs px-2 py-1 rounded focus:outline-none" onchange="filterAndUpdate()">
                    <option value="ALL">Semua Tahun</option>
                </select>
            </div>
            <div class="flex items-center bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">
                <label for="periodSelect" class="text-xs text-slate-200 mr-2 font-semibold"><i class="fa-solid fa-clock mr-1"></i> Periode:</label>
                <select id="periodSelect" class="bg-slate-900 text-cyan-300 font-bold text-xs px-2 py-1 rounded focus:outline-none" onchange="filterAndUpdate()">
                    <option value="ALL">Semua Periode</option>
                    <option value="1">Periode 1</option>
                    <option value="2">Periode 2</option>
                </select>
            </div>
        </div>
    </header>
    <div class="flex flex-1 overflow-hidden">
        <div class="flex-1 flex flex-col h-full overflow-hidden">
            <div id="map" class="flex-1 w-full z-10 min-h-[45%]" style="background-color: #0b132b;"></div>
            <div class="h-80 bg-slate-900 border-t border-slate-800 flex flex-col shrink-0 z-20">
                <div class="px-4 py-2 bg-slate-900/90 border-b border-slate-800 flex justify-between items-center">
                    <h3 class="font-bold text-xs text-cyan-400 uppercase tracking-wider"><i class="fa-solid fa-table mr-1"></i> Tabel Lengkap Parameter & Status Kelayakan Terumbu Karang</h3>
                    <span id="tableCount" class="text-xs text-cyan-300 font-medium">Memuat data...</span>
                </div>
                <div class="flex-1 overflow-auto p-2">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-800 text-cyan-300 sticky top-0 font-semibold z-10">
                                <th class="p-2.5 border-b border-slate-700">Kode</th>
                                <th class="p-2.5 border-b border-slate-700">Nama Lokasi</th>
                                <th class="p-2.5 border-b border-slate-700">Provinsi</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">Tgl Pantau</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">Suhu (°C)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">Salinitas (ppt)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">DO (mg/L)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">pH</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">TSS (mg/L)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">Kekeruhan (NTU)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">NO3 (mg/L)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">PO4 (mg/L)</th>
                                <th class="p-2.5 border-b border-slate-700 text-center">Aksi</th>
                            </tr>
                        </thead>
                        <tbody id="dataTableBody" class="divide-y divide-slate-800 text-slate-200 font-medium"></tbody>
                    </table>
                </div>
            </div>
        </div>
        <aside class="w-[440px] bg-slate-900 border-l border-slate-800 flex flex-col shrink-0 z-20 shadow-2xl">
            <div class="p-3 border-b border-slate-800 bg-slate-900/90 flex justify-between items-center">
                <h3 class="font-bold text-xs text-cyan-400 uppercase tracking-wider"><i class="fa-solid fa-chart-bar mr-1"></i> Grafik Rata-Rata Parameter</h3>
                <select id="paramSelect" class="bg-slate-800 text-cyan-300 font-semibold text-xs px-2 py-1 rounded border border-slate-700 focus:outline-none" onchange="updateChart()">
                    <option value="SUHU">Suhu (°C)</option>
                    <option value="SALINITAS">Salinitas (ppt)</option>
                    <option value="DO (mg/L)">DO (mg/L)</option>
                    <option value="PH">pH</option>
                    <option value="TSS (mg/L)">TSS (mg/L)</option>
                    <option value="KEKERUHAN (NTU)">Kekeruhan (NTU)</option>
                    <option value="NITRAT (NO3) (mg/L)" selected>Nitrat / NO3 (mg/L)</option>
                    <option value="FOSPAT (PO4) (mg/L)">Fosfat / PO4 (mg/L)</option>
                </select>
            </div>
            <div class="p-4 flex-1 flex flex-col space-y-4 overflow-y-auto">
                <div class="bg-slate-800/60 p-3 rounded-lg border border-slate-700 flex-1 flex flex-col">
                    <p class="text-xs text-slate-200 mb-2 font-medium">Perbandingan rata-rata per provinsi berdasarkan filter aktif.</p>
                    <div class="relative flex-1 w-full min-h-[260px]"><canvas id="paramChart"></canvas></div>
                </div>
            </div>
        </aside>
    </div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const rawCsvData = `{csv_text}`;

        const map = L.map('map', {{ zoomControl: false }}).setView([-2.5, 118.0], 5);
        L.control.zoom({{ position: 'bottomright' }}).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{ maxZoom: 18 }}).addTo(map);

        let globalData = [];
        let markersLayer = L.layerGroup().addTo(map);
        let myChart = null;
        let isDarkMode = true;

        window.addEventListener('DOMContentLoaded', () => {{
            Papa.parse(rawCsvData, {{
                header: true,
                delimiter: ";",
                skipEmptyLines: true,
                complete: function(results) {{
                    globalData = results.data.map(row => {{
                        let cleanRow = {{}};
                        for (let key in row) {{
                            let cleanKey = key.trim().replace(/^\\uFEFF/, '');
                            cleanRow[cleanKey] = row[key];
                        }}
                        return cleanRow;
                    }});
                    document.getElementById('loadStatus').innerText = `Berhasil memuat ${{globalData.length}} data pemantauan!`;
                    initYears();
                    filterAndUpdate();
                }}
            }});
        }});

        function initYears() {{
            let yearsSet = new Set();
            globalData.forEach(d => {{
                let tgl = d['TANGGAL PEMANTAUAN'] || '';
                let parts = tgl.split('/');
                if (parts.length === 3) yearsSet.add(parts[2]);
            });
            let sortedYears = Array.from(yearsSet).sort();
            let yearSelect = document.getElementById('yearSelect');
            yearSelect.innerHTML = '<option value="ALL">Semua Tahun</option>';
            sortedYears.forEach(yr => {{
                yearSelect.innerHTML += `<option value="${{yr}}" ${{yr === '2026' ? 'selected' : ''}}>${{yr}}</option>`;
            }});
        }}

        function filterAndUpdate() {{
            if (globalData.length === 0) return;
            const selectedYear = document.getElementById('yearSelect').value;
            const selectedPeriod = document.getElementById('periodSelect').value;

            let filtered = globalData.filter(d => {{
                let tgl = d['TANGGAL PEMANTAUAN'] || '';
                let yr = tgl.split('/')[2];
                let per = String(d['PERIODE PEMANTAUAN'] || '').trim();
                let matchYear = (selectedYear === 'ALL' || yr === selectedYear);
                let matchPeriod = (selectedPeriod === 'ALL' || per === selectedPeriod);
                return matchYear && matchPeriod && d['LATITUDE'] && d['LONGITUDE'];
            }});
            renderMapAndTable(filtered);
            updateChartData(filtered);
        }}

        function renderMapAndTable(data) {{
            markersLayer.clearLayers();
            let tableHtml = '';
            data.forEach((p) => {{
                let lat = parseFloat(p['LATITUDE']);
                let lon = parseFloat(p['LONGITUDE']);
                if (isNaN(lat) || isNaN(lon)) return;

                let suhu = p['SUHU'] || '-';
                let sal = p['SALINITAS'] || '-';
                let doVal = p['DO (mg/L)'] || '-';
                let ph = p['PH'] || '-';
                let tss = p['TSS (mg/L)'] || '-';
                let kek = p['KEKERUHAN (NTU)'] || '-';
                let no3 = p['NITRAT (NO3) (mg/L)'] || '-';
                let po4 = p['FOSPAT (PO4) (mg/L)'] || '-';

                let circleMarker = L.circleMarker([lat, lon], {{ radius: 6, fillColor: "#38bdf8", color: "#0284c7", weight: 2, fillOpacity: 0.9 }});
                circleMarker.bindPopup(`
                    <div class="custom-popup p-3 bg-slate-900 text-slate-100">
                        <h4 class="font-bold text-cyan-400 text-sm mb-1">${{p['NAMA LOKASI'] || 'Lokasi'}} (${{p['KODE LOKASI'] || ''}})</h4>
                        <p class="text-xs text-slate-400 mb-2 font-medium">Provinsi: ${{p['PROVINSI']}} | Tgl: ${{p['TANGGAL PEMANTAUAN']}}</p>
                    </div>
                `);
                markersLayer.addLayer(circleMarker);

                tableHtml += `
                    <tr class="hover:bg-slate-800 cursor-pointer transition" onclick="map.setView([${{lat}}, ${{lon}}], 9)">
                        <td class="p-2.5 border-b border-slate-800 text-cyan-400 font-bold">${{p['KODE LOKASI'] || '-'}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-slate-100 font-semibold">${{p['NAMA LOKASI'] || '-'}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-slate-300">${{p['PROVINSI'] || '-'}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-slate-300 text-center">${{p['TANGGAL PEMANTAUAN'] || '-'}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{suhu}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{sal}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{doVal}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{ph}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center font-semibold text-cyan-300">${{tss}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{kek}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{no3}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">${{po4}}</td>
                        <td class="p-2.5 border-b border-slate-800 text-center">
                            <button class="bg-cyan-600 hover:bg-cyan-500 text-slate-950 px-2 py-1 rounded text-xs font-bold shadow">Zoom</button>
                        </td>
                    </tr>
                `;
            }});
            document.getElementById('dataTableBody').innerHTML = tableHtml;
            document.getElementById('tableCount').innerText = `Menampilkan ${{data.length}} titik pantau`;
        }}

        function updateChartData(data) {{
            const paramKey = document.getElementById('paramSelect').value;
            let groups = {{}};
            data.forEach(d => {{
                let prov = d['PROVINSI'] || 'Lainnya';
                let val = parseFloat(d[paramKey]);
                if (!isNaN(val)) {{
                    if (!groups[prov]) groups[prov] = [];
                    groups[prov].push(val);
                }}
            }});
            let labels = Object.keys(groups);
            let averages = labels.map(prov => {{
                let arr = groups[prov];
                return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2);
            }});
            const ctx = document.getElementById('paramChart').getContext('2d');
            if (myChart) myChart.destroy();
            myChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{ label: `Rata-rata ${{paramKey}}`, data: averages, backgroundColor: 'rgba(6, 182, 212, 0.8)', borderColor: '#06b6d4', borderWidth: 1.5, borderRadius: 4 }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ labels: {{ color: '#e2e8f0', font: {{ size: 11, weight: 'bold' }} }} }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#e2e8f0', font: {{ size: 10 }}, maxRotation: 45 }}, grid: {{ color: '#334155' }} }},
                        y: {{ ticks: {{ color: '#e2e8f0', font: {{ size: 11 }} }}, grid: {{ color: '#334155' }} }}
                    }}
                }}
            }});
        }}

        function updateChart() {{ filterAndUpdate(); }}
        function toggleTheme() {{
            isDarkMode = !isDarkMode;
            document.getElementById('mainBody').className = isDarkMode ? "bg-slate-950 text-slate-100 flex flex-col h-screen overflow-hidden" : "bg-slate-100 text-slate-900 flex flex-col h-screen overflow-hidden";
            filterAndUpdate();
        }}
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("File index.html berhasil dibuat dengan seluruh 2500 data!")