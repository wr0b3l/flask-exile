// Quick Actions Navbar Component
const QuickActions = {
    template: `
        <nav class="navbar">
            <div class="navbar-content">
                <div class="navbar-actions">
                    <button class="navbar-btn" @click="$emit('add-monitor')" title="Add new monitor">
                        <span class="navbar-icon">👁️</span>
                        <span class="navbar-label">Add Monitor</span>
                    </button>
                </div>
            </div>
        </nav>
    `
};

