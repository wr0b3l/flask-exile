// Main App Container Component
const AppContainer = {
    template: `
        <div class="container">
            <app-header :is-connected="isConnected"></app-header>
            
            <quick-actions @add-monitor="showModal"></quick-actions>
            
            <div class="layout">
                <div class="main-content">
                    <monitors-list 
                        :monitors="monitors"
                        :total="stats.monitors"
                        @toggle="toggleMonitor"
                        @edit="editMonitor"
                        @remove="removeMonitor">
                    </monitors-list>
                    
                    <activity-log :logs="logs"></activity-log>
                </div>
            </div>
            
            <monitor-modal
                v-if="modalOpen"
                ref="monitorModal"
                :monitor="editingMonitor"
                :monitors="monitors"
                @close="closeModal"
                @save="saveMonitor"
                @pick-pixel="pickPixel">
            </monitor-modal>
        </div>
    `,
    data() {
        return {
            serverStatus: 'Connecting...',
            isConnected: false,
            monitors: [],
            logs: [],
            stats: {
                monitors: 0,
                matches: 0,
                actions: 0
            },
            modalOpen: false,
            editingMonitor: null,
            socket: null
        }
    },
    mounted() {
        this.initSocket();
        this.loadMonitors();
        this.addLog('Pixel Bot ready', 'info');
    },
    methods: {
        initSocket() {
            this.socket = SocketService.init().socket;

            SocketService
                .on('connect', () => {
                    this.serverStatus = 'Connected';
                    this.isConnected = true;
                    this.addLog('Connected to server', 'success');
                })
                .on('disconnect', () => {
                    this.serverStatus = 'Disconnected';
                    this.isConnected = false;
                    this.addLog('Disconnected from server', 'error');
                })
                .on('pixel_picked', (pixel) => {
                    this.addLog(`Pixel picked: (${pixel.x}, ${pixel.y}) = ${pixel.hex}`, 'success');
                    // Pass pixel to modal if it's open
                    if (this.modalOpen && this.$refs.monitorModal) {
                        this.$refs.monitorModal.handlePixelPicked(pixel);
                    }
                })
                .on('monitor_added', () => this.loadMonitors())
                .on('monitor_updated', () => this.loadMonitors())
                .on('monitor_removed', () => this.loadMonitors())
                .on('activity_log', (data) => this.addLog(data.message, data.type))
                .on('monitor_state_change', (data) => {
                    const index = this.monitors.findIndex(m => m.id === data.id);
                    if (index !== -1) {
                        const monitor = this.monitors[index];
                        this.monitors[index] = {
                            ...monitor,
                            in_cooldown: 'in_cooldown' in data ? data.in_cooldown : monitor.in_cooldown,
                            blocked_by_master: 'blocked_by_master' in data ? data.blocked_by_master : monitor.blocked_by_master
                        };
                    }
                })
                .on('master_state_change', (data) => {
                    const index = this.monitors.findIndex(m => m.id === data.id);
                    if (index !== -1) {
                        this.monitors[index] = {
                            ...this.monitors[index],
                            is_active: data.is_active
                        };
                    }
                })
                .on('monitor_match', (data) => {
                    this.addLog(`Monitor "${data.name}" matched`, 'success');
                    const monitor = this.monitors.find(m => m.id === data.id);
                    if (monitor) {
                        if (!monitor.triggerCount) monitor.triggerCount = 0;
                        monitor.triggerCount++;
                    }
                    this.stats.matches++;
                })
                .on('action_triggered', (data) => {
                    this.addLog(`Action triggered: ${data.action.type}`, 'info');
                    this.stats.actions++;
                });
        },

        async loadMonitors() {
            try {
                const data = await API.monitors.list();
                this.monitors = data.monitors || [];
                this.monitors.forEach(m => {
                    if (!m.triggerCount) m.triggerCount = 0;
                });
                this.stats.monitors = this.monitors.length;
            } catch (err) {
                this.addLog('Error loading monitors: ' + err, 'error');
            }
        },

        showModal() {
            this.editingMonitor = {
                name: '',
                x: '',
                y: '',
                target_color: ['', '', ''],
                tolerance: 10,
                cooldown: 1000,
                action: { type: 'keypress', key: '' },
                colorPreview: '#fff',
                monitor_type: 'normal',
                master_id: null,
                trigger_mode: 'no_match',
                pixel_group: [],
                group_logic: 'all_match'
            };
            this.modalOpen = true;
        },

        closeModal() {
            this.modalOpen = false;
            this.editingMonitor = null;
        },

        async saveMonitor(monitor) {
            try {
                const data = monitor.id
                    ? await API.monitors.edit(monitor.id, monitor)
                    : await API.monitors.add(monitor);

                if (data.success) {
                    this.addLog(monitor.id ? 'Monitor updated' : 'Monitor added', 'success');
                    this.closeModal();
                    this.loadMonitors();
                } else {
                    this.addLog('Failed: ' + data.error, 'error');
                }
            } catch (err) {
                this.addLog('Error: ' + err, 'error');
            }
        },

        async toggleMonitor(id) {
            try {
                const data = await API.monitors.toggle(id);
                if (data.success) {
                    this.addLog(`Monitor ${data.status}`, 'info');
                    this.loadMonitors();
                }
            } catch (err) {
                this.addLog('Error: ' + err, 'error');
            }
        },

        editMonitor(monitor) {
            this.editingMonitor = { ...monitor };
            this.editingMonitor.colorPreview = `rgb(${monitor.target_color[0]}, ${monitor.target_color[1]}, ${monitor.target_color[2]})`;
            this.modalOpen = true;
        },

        async removeMonitor(id) {
            if (!confirm('Remove this monitor?')) return;

            try {
                const data = await API.monitors.remove(id);
                if (data.success) {
                    this.addLog('Monitor removed', 'success');
                    this.loadMonitors();
                }
            } catch (err) {
                this.addLog('Error: ' + err, 'error');
            }
        },

        async pickPixel() {
            this.addLog('Launching pixel picker...', 'info');
            try {
                const data = await API.picker.launch();
                if (!data.success) {
                    this.addLog('Picker failed: ' + data.error, 'error');
                }
            } catch (err) {
                this.addLog('Error: ' + err, 'error');
            }
        },

        addLog(message, type = 'info') {
            const time = new Date().toLocaleTimeString();
            this.logs.unshift({ time, message, type });
            if (this.logs.length > 50) {
                this.logs.pop();
            }
        }
    }
};

