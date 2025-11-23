// Monitors List Component
const MonitorsList = {
    props: ['monitors', 'total'],
    template: `
        <div class="section">
            <h2>
                👁️ Active Monitors ({{ total }})
                <span v-if="monitorCounts.masters > 0 || monitorCounts.slaves > 0" style="font-size: 0.75em; color: #8b7355; font-weight: normal;">
                    <span v-if="monitorCounts.masters > 0">
                        👑 {{ monitorCounts.masters }} master{{ monitorCounts.masters !== 1 ? 's' : '' }}
                    </span>
                    <span v-if="monitorCounts.slaves > 0">
                        {{ monitorCounts.masters > 0 ? ', ' : '' }}
                        ⛓️ {{ monitorCounts.slaves }} slave{{ monitorCounts.slaves !== 1 ? 's' : '' }}
                    </span>
                    <span v-if="monitorCounts.normal > 0">
                        {{ (monitorCounts.masters > 0 || monitorCounts.slaves > 0) ? ', ' : '' }}
                        {{ monitorCounts.normal }} normal
                    </span>
                </span>
            </h2>
            <div class="monitors-list">
                <div v-if="monitors.length === 0" class="empty-state">
                    <div class="icon">👁️</div>
                    <p>No active monitors</p>
                    <p style="font-size: 0.9em; margin-top: 10px;">Click "Add Monitor" to start monitoring pixels</p>
                </div>
                
                <!-- Render grouped monitors -->
                <div v-for="group in groupedMonitors" :key="'group-' + group.master?.id || group.normal[0]?.id">
                    <!-- Master Monitor -->
                    <div v-if="group.master" class="monitor-group">
                        <div 
                            class="monitor-item master-monitor"
                            :class="{ paused: !group.master.enabled, inactive: !group.master.is_active }">
                            
                            <div class="monitor-icon">
                                <img 
                                    :src="getMonitorIcon(group.master)" 
                                    :alt="getMonitorState(group.master)"
                                    :title="getMonitorState(group.master)"
                                    class="monitor-state-icon">
                            </div>
                            
                            <div class="monitor-info">
                                <div class="monitor-name" :class="{ paused: !group.master.enabled, inactive: !group.master.is_active }">
                                    <span title="Master Monitor">👑 </span>
                                    {{ group.master.name }}
                                    <span v-if="getPixelCount(group.master) > 1" style="color: #d4af37; font-size: 0.85em; margin-left: 5px;">
                                        [{{ getPixelCount(group.master) }} pixels]
                                    </span>
                                    <span v-if="group.slaves.length > 0" style="color: #8b7355; font-size: 0.9em;">
                                        ({{ group.slaves.length }} slave{{ group.slaves.length !== 1 ? 's' : '' }})
                                    </span>
                                </div>
                                <div class="monitor-details">
                                    Position: ({{ group.master.x }}, {{ group.master.y }}) | 
                                    Color: RGB({{ group.master.target_color[0] }}, {{ group.master.target_color[1] }}, {{ group.master.target_color[2] }}) | 
                                    Tolerance: {{ group.master.tolerance }} | 
                                    Mode: {{ getTriggerModeText(group.master.trigger_mode) }} | 
                                    Action: {{ getActionText(group.master.action) }}
                                </div>
                            </div>
                            
                            <div class="monitor-actions">
                                <button 
                                    class="btn"
                                    :class="group.master.enabled ? 'btn-warning' : 'btn-success'"
                                    @click="$emit('toggle', group.master.id)"
                                    :title="group.master.enabled ? 'Pause' : 'Resume'">
                                    {{ group.master.enabled ? '⏸️' : '▶️' }}
                                </button>
                                <button 
                                    class="btn btn-primary"
                                    @click="$emit('edit', group.master)"
                                    title="Edit monitor">
                                    ✏️
                                </button>
                                <button 
                                    class="btn btn-danger"
                                    @click="$emit('remove', group.master.id)"
                                    title="Remove monitor">
                                    🗑️
                                </button>
                            </div>
                        </div>
                        
                        <!-- Slave Monitors (nested under master) -->
                        <div v-if="group.slaves.length > 0" class="slave-monitors">
                            <div 
                                v-for="slave in group.slaves" 
                                :key="slave.id"
                                class="monitor-item slave-monitor"
                                :class="{ paused: !slave.enabled, blocked: slave.blocked_by_master }">
                                
                                <div class="slave-connector">⤷</div>
                                
                                <div class="monitor-icon">
                                    <img 
                                        :src="getMonitorIcon(slave)" 
                                        :alt="getMonitorState(slave)"
                                        :title="getMonitorState(slave)"
                                        class="monitor-state-icon">
                                </div>
                                
                                <div class="monitor-info">
                                    <div class="monitor-name" :class="{ paused: !slave.enabled, blocked: slave.blocked_by_master }">
                                        <span title="Slave Monitor">⛓️ </span>
                                        {{ slave.name }}
                                        <span v-if="getPixelCount(slave) > 1" style="color: #c9a86a; font-size: 0.85em; margin-left: 5px;">
                                            [{{ getPixelCount(slave) }} pixels]
                                        </span>
                                    </div>
                                    <div class="monitor-details">
                                        Position: ({{ slave.x }}, {{ slave.y }}) | 
                                        Color: RGB({{ slave.target_color[0] }}, {{ slave.target_color[1] }}, {{ slave.target_color[2] }}) | 
                                        Tolerance: {{ slave.tolerance }} | 
                                        Cooldown: {{ slave.cooldown || 1000 }}ms | 
                                        Mode: {{ getTriggerModeText(slave.trigger_mode) }} | 
                                        Action: {{ getActionText(slave.action) }}
                                    </div>
                                </div>
                                
                                <div class="monitor-actions">
                                    <button 
                                        class="btn"
                                        :class="slave.enabled ? 'btn-warning' : 'btn-success'"
                                        @click="$emit('toggle', slave.id)"
                                        :title="slave.enabled ? 'Pause' : 'Resume'">
                                        {{ slave.enabled ? '⏸️' : '▶️' }}
                                    </button>
                                    <button 
                                        class="btn btn-primary"
                                        @click="$emit('edit', slave)"
                                        title="Edit monitor">
                                        ✏️
                                    </button>
                                    <button 
                                        class="btn btn-danger"
                                        @click="$emit('remove', slave.id)"
                                        title="Remove monitor">
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Normal Monitors (no master/slave relationship) -->
                    <div 
                        v-for="monitor in group.normal" 
                        :key="monitor.id"
                        class="monitor-item"
                        :class="{ paused: !monitor.enabled }">
                        
                        <div class="monitor-icon">
                            <img 
                                :src="getMonitorIcon(monitor)" 
                                :alt="getMonitorState(monitor)"
                                :title="getMonitorState(monitor)"
                                class="monitor-state-icon">
                        </div>
                        
                        <div class="monitor-info">
                            <div class="monitor-name" :class="{ paused: !monitor.enabled }">
                                {{ monitor.name }}
                                <span v-if="getPixelCount(monitor) > 1" style="color: #c9a86a; font-size: 0.85em; margin-left: 5px;">
                                    [{{ getPixelCount(monitor) }} pixels]
                                </span>
                            </div>
                            <div class="monitor-details">
                                Position: ({{ monitor.x }}, {{ monitor.y }}) | 
                                Color: RGB({{ monitor.target_color[0] }}, {{ monitor.target_color[1] }}, {{ monitor.target_color[2] }}) | 
                                Tolerance: {{ monitor.tolerance }} | 
                                Cooldown: {{ monitor.cooldown || 1000 }}ms | 
                                Mode: {{ getTriggerModeText(monitor.trigger_mode) }} | 
                                Action: {{ getActionText(monitor.action) }}
                            </div>
                        </div>
                        
                        <div class="monitor-actions">
                            <button 
                                class="btn"
                                :class="monitor.enabled ? 'btn-warning' : 'btn-success'"
                                @click="$emit('toggle', monitor.id)"
                                :title="monitor.enabled ? 'Pause' : 'Resume'">
                                {{ monitor.enabled ? '⏸️' : '▶️' }}
                            </button>
                            <button 
                                class="btn btn-primary"
                                @click="$emit('edit', monitor)"
                                title="Edit monitor">
                                ✏️
                            </button>
                            <button 
                                class="btn btn-danger"
                                @click="$emit('remove', monitor.id)"
                                title="Remove monitor">
                                🗑️
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    computed: {
        monitorCounts() {
            return {
                masters: this.monitors.filter(m => m.monitor_type === 'master').length,
                slaves: this.monitors.filter(m => m.monitor_type === 'slave').length,
                normal: this.monitors.filter(m => !m.monitor_type || m.monitor_type === 'normal').length
            };
        },
        groupedMonitors() {
            // Group monitors: masters with their slaves, and normal monitors
            const groups = [];
            const masters = this.monitors.filter(m => m.monitor_type === 'master');
            const slaves = this.monitors.filter(m => m.monitor_type === 'slave');
            const normal = this.monitors.filter(m => !m.monitor_type || m.monitor_type === 'normal');

            // Create a group for each master with its slaves
            masters.forEach(master => {
                const masterSlaves = slaves.filter(s => s.master_id === master.id);
                groups.push({
                    master: master,
                    slaves: masterSlaves,
                    normal: []
                });
            });

            // Add orphaned slaves (slaves without a valid master)
            const orphanedSlaves = slaves.filter(s => !masters.find(m => m.id === s.master_id));
            if (orphanedSlaves.length > 0) {
                groups.push({
                    master: null,
                    slaves: [],
                    normal: orphanedSlaves
                });
            }

            // Add normal monitors
            if (normal.length > 0) {
                groups.push({
                    master: null,
                    slaves: [],
                    normal: normal
                });
            }

            return groups;
        }
    },
    methods: {
        getPixelCount(monitor) {
            return 1 + (monitor.pixel_group ? monitor.pixel_group.length : 0);
        },
        getActionText(action) {
            if (action.type === 'keypress') {
                return 'Press ' + action.key;
            }
            return action.type;
        },
        getTriggerModeText(mode) {
            if (mode === 'match') {
                return '✓ On Match';
            }
            return '≠ On Change';
        },
        getMonitorIcon(monitor) {
            if (!monitor.enabled) {
                return '/static/images/flask_inactive.png';
            }
            if (monitor.monitor_type === 'master') {
                // Master: show cooldown icon when inactive
                return monitor.is_active ? '/static/images/flask_inactive.png' : '/static/images/flask_blocked.png';
            }
            if (monitor.blocked_by_master) {
                return '/static/images/flask_blocked.png';
            }
            if (monitor.in_cooldown) {
                return '/static/images/flask_cooldown.png';
            }
            return '/static/images/flask_inactive.png';
        },
        getMonitorState(monitor) {
            if (!monitor.enabled) {
                return 'Paused';
            }
            if (monitor.monitor_type === 'master') {
                return monitor.is_active ? 'Master Active' : 'Master Inactive';
            }
            if (monitor.blocked_by_master) {
                return 'Blocked by Master';
            }
            if (monitor.in_cooldown) {
                return 'In Cooldown';
            }
            return 'Ready';
        }
    }
};

