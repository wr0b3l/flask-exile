// API Service - Centralized API calls
const API = {
    // Monitor endpoints
    monitors: {
        async list() {
            const response = await fetch('/api/monitor/list');
            return await response.json();
        },

        async add(monitorData) {
            const response = await fetch('/api/monitor/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(monitorData)
            });
            return await response.json();
        },

        async edit(id, monitorData) {
            const response = await fetch(`/api/monitor/edit/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(monitorData)
            });
            return await response.json();
        },

        async remove(id) {
            const response = await fetch(`/api/monitor/remove/${id}`, {
                method: 'DELETE'
            });
            return await response.json();
        },

        async toggle(id) {
            const response = await fetch(`/api/monitor/toggle/${id}`, {
                method: 'POST'
            });
            return await response.json();
        }
    },

    // Pixel picker endpoints
    picker: {
        async launch() {
            const response = await fetch('/api/picker/launch', {
                method: 'POST'
            });
            return await response.json();
        }
    },

    // Screen capture endpoints
    screen: {
        async capture(region = null) {
            const response = await fetch('/api/screen/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region })
            });
            return await response.json();
        },

        async getPixelColor(x, y) {
            const response = await fetch('/api/pixel/get-color', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ x, y })
            });
            return await response.json();
        }
    },

    // Status endpoint
    async getStatus() {
        const response = await fetch('/api/status');
        return await response.json();
    }
};

