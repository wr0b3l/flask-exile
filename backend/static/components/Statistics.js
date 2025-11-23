// Statistics Component
const Statistics = {
    props: ['stats'],
    template: `
        <div class="section">
            <h2>📊 Statistics</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.monitors }}</div>
                    <div class="stat-label">Active Monitors</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.matches }}</div>
                    <div class="stat-label">Total Matches</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.actions }}</div>
                    <div class="stat-label">Actions Triggered</div>
                </div>
            </div>
        </div>
    `
};

