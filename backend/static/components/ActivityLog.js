// Activity Log Component
const ActivityLog = {
    props: ['logs'],
    template: `
        <div class="section">
            <h2>📝 Activity Log</h2>
            <div class="logs">
                <div 
                    v-for="(log, index) in logs" 
                    :key="index"
                    class="log-entry">
                    <span class="log-time">[{{ log.time }}]</span>
                    <span :class="'log-' + log.type">{{ log.message }}</span>
                </div>
            </div>
        </div>
    `
};

