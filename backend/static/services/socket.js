// Socket Service - Centralized WebSocket handling
const SocketService = {
    socket: null,
    listeners: {},

    init() {
        this.socket = io();
        return this;
    },

    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);

        if (this.socket) {
            this.socket.on(event, callback);
        }

        return this;
    },

    off(event, callback) {
        if (this.socket) {
            this.socket.off(event, callback);
        }

        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }

        return this;
    },

    emit(event, data) {
        if (this.socket) {
            this.socket.emit(event, data);
        }
        return this;
    },

    disconnect() {
        if (this.socket) {
            Object.keys(this.listeners).forEach(event => {
                this.listeners[event].forEach(callback => {
                    this.socket.off(event, callback);
                });
            });
            this.socket.disconnect();
        }
        this.listeners = {};
        return this;
    },

    isConnected() {
        return this.socket && this.socket.connected;
    }
};

