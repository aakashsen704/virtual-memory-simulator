"""
Web Interface Generator - Creates interactive HTML visualization
"""

def generate_web_interface():
    """Generate standalone HTML file with interactive visualization"""
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virtual Memory Simulator - Interactive Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .controls {
            padding: 30px;
            background: #f8f9fa;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
        }
        
        .control-group label {
            font-weight: 600;
            margin-bottom: 8px;
            color: #2c3e50;
        }
        
        .control-group select,
        .control-group input {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .control-group select:focus,
        .control-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn-simulate {
            grid-column: 1 / -1;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn-simulate:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .visualization {
            padding: 30px;
        }
        
        .memory-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }
        
        .frame {
            aspect-ratio: 1;
            border: 2px solid #ddd;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            transition: all 0.3s;
            position: relative;
        }
        
        .frame.occupied {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        .frame.empty {
            background: #f8f9fa;
            color: #aaa;
        }
        
        .frame.fault {
            animation: pageFault 0.5s;
        }
        
        @keyframes pageFault {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); background: #e74c3c; }
        }
        
        .frame-label {
            font-size: 0.7em;
            opacity: 0.7;
            margin-top: 5px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: 700;
            color: #2c3e50;
            margin: 10px 0;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .reference-string {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .reference-string h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .pages {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .page {
            width: 40px;
            height: 40px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        
        .page.current {
            background: #667eea;
            color: white;
            transform: scale(1.2);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .page.visited {
            background: #ddd;
            color: #666;
        }
        
        .page.unvisited {
            background: white;
            border: 2px solid #ddd;
            color: #999;
        }
        
        .algorithm-info {
            margin: 20px 0;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
        }
        
        .algorithm-info h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }
        
        .progress-bar {
            width: 100%;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖥️ Virtual Memory Simulator</h1>
            <p>Interactive Page Replacement Algorithm Visualization</p>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="algorithm">Replacement Algorithm</label>
                <select id="algorithm">
                    <option value="FIFO">FIFO (First-In-First-Out)</option>
                    <option value="LRU" selected>LRU (Least Recently Used)</option>
                    <option value="LFU">LFU (Least Frequently Used)</option>
                    <option value="Clock">Clock (Second Chance)</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="frames">Physical Frames</label>
                <input type="number" id="frames" value="5" min="1" max="20">
            </div>
            
            <div class="control-group">
                <label for="pages">Virtual Pages</label>
                <input type="number" id="pages" value="20" min="10" max="50">
            </div>
            
            <div class="control-group">
                <label for="refLength">Reference Length</label>
                <input type="number" id="refLength" value="50" min="10" max="200">
            </div>
            
            <div class="control-group">
                <label for="pattern">Access Pattern</label>
                <select id="pattern">
                    <option value="random">Random Access</option>
                    <option value="locality" selected>Locality of Reference</option>
                    <option value="sequential">Sequential Access</option>
                    <option value="loop">Loop Pattern</option>
                </select>
            </div>
            
            <button class="btn-simulate" onclick="runSimulation()">🚀 Run Simulation</button>
        </div>
        
        <div class="visualization">
            <div id="algorithmInfo" class="algorithm-info" style="display:none;"></div>
            
            <div id="progress" class="progress-bar" style="display:none;">
                <div id="progressFill" class="progress-fill"></div>
            </div>
            
            <div id="referenceString" class="reference-string" style="display:none;">
                <h3>Page Reference String</h3>
                <div id="pages" class="pages"></div>
            </div>
            
            <h3>Physical Memory Frames</h3>
            <div id="memoryGrid" class="memory-grid"></div>
            
            <div id="stats" class="stats"></div>
        </div>
    </div>
    
    <script>
        // Simulation engine
        class PageReplacementSimulator {
            constructor(algorithm, numFrames, numPages) {
                this.algorithm = algorithm;
                this.numFrames = numFrames;
                this.numPages = numPages;
                this.frames = [];
                this.pageFaults = 0;
                this.accesses = 0;
                this.accessTimes = {};
                this.accessCounts = {};
                this.queue = [];
                this.clockHand = 0;
                this.referenceBits = {};
            }
            
            accessPage(pageNum) {
                this.accesses++;
                const time = this.accesses;
                
                // Check if page in memory
                const pageIndex = this.frames.indexOf(pageNum);
                
                if (pageIndex !== -1) {
                    // Page hit
                    this.updateAccessInfo(pageNum, time);
                    return { fault: false, victim: null };
                } else {
                    // Page fault
                    this.pageFaults++;
                    let victim = null;
                    
                    if (this.frames.length >= this.numFrames) {
                        victim = this.selectVictim();
                        const victimIndex = this.frames.indexOf(victim);
                        this.frames[victimIndex] = pageNum;
                        this.removeFromTracking(victim);
                    } else {
                        this.frames.push(pageNum);
                    }
                    
                    this.addToTracking(pageNum, time);
                    return { fault: true, victim: victim };
                }
            }
            
            selectVictim() {
                if (this.algorithm === 'FIFO') {
                    return this.queue[0];
                } else if (this.algorithm === 'LRU') {
                    let oldest = this.frames[0];
                    let oldestTime = this.accessTimes[oldest];
                    for (let page of this.frames) {
                        if (this.accessTimes[page] < oldestTime) {
                            oldestTime = this.accessTimes[page];
                            oldest = page;
                        }
                    }
                    return oldest;
                } else if (this.algorithm === 'LFU') {
                    let minCount = Infinity;
                    let victim = this.frames[0];
                    for (let page of this.frames) {
                        if (this.accessCounts[page] < minCount) {
                            minCount = this.accessCounts[page];
                            victim = page;
                        }
                    }
                    return victim;
                } else if (this.algorithm === 'Clock') {
                    while (true) {
                        const page = this.frames[this.clockHand];
                        if (this.referenceBits[page] === 0) {
                            const victim = page;
                            this.clockHand = (this.clockHand + 1) % this.frames.length;
                            return victim;
                        } else {
                            this.referenceBits[page] = 0;
                            this.clockHand = (this.clockHand + 1) % this.frames.length;
                        }
                    }
                }
            }
            
            updateAccessInfo(pageNum, time) {
                this.accessTimes[pageNum] = time;
                this.accessCounts[pageNum] = (this.accessCounts[pageNum] || 0) + 1;
                this.referenceBits[pageNum] = 1;
            }
            
            addToTracking(pageNum, time) {
                if (this.algorithm === 'FIFO') {
                    this.queue.push(pageNum);
                }
                this.accessTimes[pageNum] = time;
                this.accessCounts[pageNum] = 1;
                this.referenceBits[pageNum] = 1;
            }
            
            removeFromTracking(pageNum) {
                if (this.algorithm === 'FIFO') {
                    const idx = this.queue.indexOf(pageNum);
                    if (idx !== -1) this.queue.splice(idx, 1);
                }
                delete this.accessTimes[pageNum];
                delete this.accessCounts[pageNum];
                delete this.referenceBits[pageNum];
            }
            
            getStats() {
                return {
                    faults: this.pageFaults,
                    accesses: this.accesses,
                    faultRate: (this.pageFaults / this.accesses * 100).toFixed(2),
                    hitRate: ((this.accesses - this.pageFaults) / this.accesses * 100).toFixed(2)
                };
            }
        }
        
        // Generate reference string
        function generateReferenceString(length, numPages, pattern) {
            const refs = [];
            
            if (pattern === 'random') {
                for (let i = 0; i < length; i++) {
                    refs.push(Math.floor(Math.random() * numPages));
                }
            } else if (pattern === 'sequential') {
                for (let i = 0; i < length; i++) {
                    refs.push(i % numPages);
                }
            } else if (pattern === 'locality') {
                const hotPages = [];
                const hotCount = Math.floor(numPages * 0.2);
                for (let i = 0; i < hotCount; i++) {
                    hotPages.push(Math.floor(Math.random() * numPages));
                }
                for (let i = 0; i < length; i++) {
                    if (Math.random() < 0.8) {
                        refs.push(hotPages[Math.floor(Math.random() * hotPages.length)]);
                    } else {
                        refs.push(Math.floor(Math.random() * numPages));
                    }
                }
            } else if (pattern === 'loop') {
                const workingSet = [];
                const setSize = Math.min(10, numPages);
                for (let i = 0; i < setSize; i++) {
                    workingSet.push(Math.floor(Math.random() * numPages));
                }
                for (let i = 0; i < length; i++) {
                    refs.push(workingSet[i % setSize]);
                }
            }
            
            return refs;
        }
        
        // Algorithm descriptions
        const algorithmInfo = {
            'FIFO': 'First-In-First-Out: Replaces the oldest page in memory. Simple but may evict frequently used pages.',
            'LRU': 'Least Recently Used: Replaces the page that hasn\'t been used for the longest time. Good performance but higher overhead.',
            'LFU': 'Least Frequently Used: Replaces the page with the lowest access count. May retain old pages too long.',
            'Clock': 'Second Chance: Circular FIFO with reference bits. Good balance between performance and simplicity.'
        };
        
        // Run simulation
        async function runSimulation() {
            const algorithm = document.getElementById('algorithm').value;
            const numFrames = parseInt(document.getElementById('frames').value);
            const numPages = parseInt(document.getElementById('pages').value);
            const refLength = parseInt(document.getElementById('refLength').value);
            const pattern = document.getElementById('pattern').value;
            
            // Show algorithm info
            const infoDiv = document.getElementById('algorithmInfo');
            infoDiv.innerHTML = `<h3>${algorithm} Algorithm</h3><p>${algorithmInfo[algorithm]}</p>`;
            infoDiv.style.display = 'block';
            
            // Generate reference string
            const referenceString = generateReferenceString(refLength, numPages, pattern);
            
            // Display reference string
            displayReferenceString(referenceString);
            
            // Create simulator
            const sim = new PageReplacementSimulator(algorithm, numFrames, numPages);
            
            // Initialize memory grid
            updateMemoryGrid([], numFrames);
            
            // Show progress
            document.getElementById('progress').style.display = 'block';
            
            // Run simulation with animation
            for (let i = 0; i < referenceString.length; i++) {
                await new Promise(resolve => setTimeout(resolve, 100));
                
                const page = referenceString[i];
                const result = sim.accessPage(page);
                
                // Update progress
                const progress = ((i + 1) / referenceString.length * 100);
                document.getElementById('progressFill').style.width = progress + '%';
                
                // Highlight current page
                highlightCurrentPage(i);
                
                // Update memory grid
                updateMemoryGrid(sim.frames, numFrames, result.fault);
                
                // Update stats
                updateStats(sim.getStats());
            }
        }
        
        function displayReferenceString(refs) {
            const div = document.getElementById('pages');
            div.innerHTML = refs.map((p, i) => 
                `<div class="page unvisited" id="page-${i}">${p}</div>`
            ).join('');
            document.getElementById('referenceString').style.display = 'block';
        }
        
        function highlightCurrentPage(index) {
            document.querySelectorAll('.page').forEach((el, i) => {
                if (i === index) {
                    el.className = 'page current';
                } else if (i < index) {
                    el.className = 'page visited';
                } else {
                    el.className = 'page unvisited';
                }
            });
        }
        
        function updateMemoryGrid(frames, numFrames, isFault = false) {
            const grid = document.getElementById('memoryGrid');
            let html = '';
            
            for (let i = 0; i < numFrames; i++) {
                const page = frames[i];
                const className = page !== undefined ? 
                    (isFault ? 'frame occupied fault' : 'frame occupied') : 
                    'frame empty';
                const content = page !== undefined ? 
                    `<div>Page ${page}</div><div class="frame-label">Frame ${i}</div>` : 
                    `<div>Empty</div><div class="frame-label">Frame ${i}</div>`;
                
                html += `<div class="${className}">${content}</div>`;
            }
            
            grid.innerHTML = html;
        }
        
        function updateStats(stats) {
            const statsDiv = document.getElementById('stats');
            statsDiv.innerHTML = `
                <div class="stat-card">
                    <div class="stat-label">Total Accesses</div>
                    <div class="stat-value">${stats.accesses}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Page Faults</div>
                    <div class="stat-value">${stats.faults}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Page Fault Rate</div>
                    <div class="stat-value">${stats.faultRate}%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Hit Rate</div>
                    <div class="stat-value">${stats.hitRate}%</div>
                </div>
            `;
        }
        
        // Initialize on load
        window.onload = () => {
            updateMemoryGrid([], 5);
        };
    </script>
</body>
</html>
'''
    
    with open('interactive_demo.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Interactive web demo created: interactive_demo.html")
    return 'interactive_demo.html'


if __name__ == "__main__":
    html_file = generate_web_interface()
    print(f"\nOpen {html_file} in a web browser to see the interactive demo!")