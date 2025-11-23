// Tabbed Modal Component
const MonitorModal = {
    props: ['monitor', 'monitors'],
    data() {
        return {
            activeTab: 'basic',  // 'basic', 'advanced', 'type', 'action'
            form: {
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
            },
            pickingForIndex: null
        }
    },
    watch: {
        monitor: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.form = { ...newVal };
                }
            }
        }
    },
    template: `
        <div class="modal active">
            <div class="modal-content modal-tabbed">
                <h3>{{ monitor.id ? 'Edit' : 'Add' }} Pixel Monitor</h3>
                
                <!-- Tab Navigation -->
                <div class="tab-nav">
                    <button 
                        class="tab-btn" 
                        :class="{ active: activeTab === 'basic' }"
                        @click="activeTab = 'basic'">
                        📝 Basic Info
                    </button>
                    <button 
                        class="tab-btn" 
                        :class="{ active: activeTab === 'pixels' }"
                        @click="activeTab = 'pixels'">
                        🎯 Pixels
                    </button>
                    <button 
                        class="tab-btn" 
                        :class="{ active: activeTab === 'type' }"
                        @click="activeTab = 'type'">
                        👑 Type & Mode
                    </button>
                    <button 
                        class="tab-btn" 
                        :class="{ active: activeTab === 'action' }"
                        @click="activeTab = 'action'">
                        ⚡ Action
                    </button>
                </div>
                
                <!-- Tab Content -->
                <div class="tab-content">
                    <!-- TAB 1: Basic Info -->
                    <div v-show="activeTab === 'basic'" class="tab-pane">
                        <!-- Name -->
                        <div class="form-group">
                            <label>Monitor Name *</label>
                            <input v-model="form.name" placeholder="e.g., Health Monitor">
                            <p>A descriptive name for this monitor</p>
                        </div>
                        
                        <!-- Tolerance -->
                        <div class="form-group">
                            <label>Tolerance</label>
                            <input v-model.number="form.tolerance" type="number" min="0" max="255" placeholder="10">
                            <p>Color difference tolerance (0-255). Higher = more lenient</p>
                        </div>
                    </div>
                    
                    <!-- TAB 2: Pixels (Unified) -->
                    <div v-show="activeTab === 'pixels'" class="tab-pane">
                        <div v-if="form.monitor_type !== 'master'" class="info-message" style="background: rgba(107, 68, 35, 0.3); padding: 15px; border: 1px solid #6b4423; border-radius: 4px; margin-bottom: 20px;">
                            <p style="margin: 0; color: #c9a86a;">
                                ⚠️ <strong>Single pixel mode</strong>
                                <br><br>Normal and Slave monitors can only monitor one pixel. Set monitor type to "Master" in the Type & Mode tab to enable multi-pixel monitoring.
                            </p>
                        </div>
                        
                        <div style="margin-bottom: 20px;">
                            <button type="button" class="btn btn-success" @click="addPixel" style="width: 100%; padding: 15px; font-size: 1.1em;" 
                                :disabled="form.monitor_type !== 'master' && allPixels.length >= 1">
                                🖱️ Add Pixel from Screen
                            </button>
                            <p style="color: #8b7355; font-size: 0.9em; margin-top: 10px; text-align: center;">
                                {{ form.monitor_type === 'master' ? 'Click to add pixels (up to 6 total)' : 'Click to set the pixel to monitor' }}
                            </p>
                        </div>
                        
                        <!-- Pixel List -->
                        <div v-if="allPixels.length > 0">
                            <div v-for="(pixel, index) in allPixels" :key="index" 
                                 style="background: rgba(20, 15, 10, 0.5); padding: 12px; margin-bottom: 10px; border: 1px solid #6b4423; border-radius: 4px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                    <strong style="color: #d4af37;">Pixel #{{ index + 1 }}</strong>
                                    <button type="button" class="btn btn-danger btn-sm" @click="removePixel(index)" 
                                        :disabled="allPixels.length === 1"
                                        title="Remove pixel">
                                        🗑️ Remove
                                    </button>
                                </div>
                                
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                    <div>
                                        <label style="color: #c9a86a; font-size: 0.9em; display: block; margin-bottom: 5px;">Position</label>
                                        <div style="font-size: 1.1em; color: #d4af37;">
                                            📌 ({{ pixel.x }}, {{ pixel.y }})
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label style="color: #c9a86a; font-size: 0.9em; display: block; margin-bottom: 5px;">Color</label>
                                        <div style="display: flex; gap: 8px; align-items: center;">
                                            <div style="width: 30px; height: 30px; border: 2px solid #6b4423; border-radius: 4px;"
                                                :style="{ background: getPixelColor(pixel.color) }">
                                            </div>
                                            <span style="color: #c9a86a; font-size: 0.9em;">
                                                RGB({{ pixel.color[0] }}, {{ pixel.color[1] }}, {{ pixel.color[2] }})
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div v-else style="color: #8b7355; font-style: italic; text-align: center; padding: 20px;">
                            No pixels added yet. Click "Add Pixel from Screen" to start.
                        </div>
                        
                        <!-- Multi-Pixel Logic (Master Only) -->
                        <div v-if="form.monitor_type === 'master' && allPixels.length > 1" style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #6b4423;">
                            <div class="form-group">
                                <label style="color: #d4af37; font-weight: bold;">Multi-Pixel Logic</label>
                                <select v-model="form.group_logic" style="width: 100%;">
                                    <option value="all_match">✓ ALL pixels must match (AND)</option>
                                    <option value="any_match">✓ ANY pixel can match (OR)</option>
                                </select>
                                <p style="color: #c9a86a; font-size: 0.85em; margin-top: 5px;">
                                    {{ form.group_logic === 'all_match' ? 'Triggers only when ALL pixels match their targets' : 'Triggers when ANY pixel matches its target' }}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- TAB 3: Monitor Type & Mode -->
                    <div v-show="activeTab === 'type'" class="tab-pane">
                        <!-- Monitor Type -->
                        <div class="form-group">
                            <label>Monitor Type</label>
                            <select v-model="form.monitor_type">
                                <option value="normal">Normal Monitor</option>
                                <option value="master">👑 Master (Controls Others)</option>
                                <option value="slave">⛓️ Slave (Depends on Master)</option>
                            </select>
                            <p v-if="form.monitor_type === 'master'" style="color: #d4af37;">
                                👑 Master monitors control when slave monitors can run
                            </p>
                            <p v-if="form.monitor_type === 'slave'" style="color: #8b7355;">
                                ⛓️ Slave monitors only run when their master is active
                            </p>
                        </div>
                        
                        <!-- Trigger Mode -->
                        <div class="form-group">
                            <label>Trigger Mode</label>
                            <select v-model="form.trigger_mode">
                                <option value="no_match">Trigger when pixel CHANGES (doesn't match)</option>
                                <option value="match">Trigger when pixel MATCHES</option>
                            </select>
                            <p v-if="form.monitor_type === 'master'" style="color: #d4af37;">
                                👑 For masters: "match" = slaves run when pixel matches (e.g., UI visible)
                            </p>
                            <p v-else-if="form.monitor_type === 'slave'" style="color: #8b7355;">
                                ⛓️ For slaves: Choose when this monitor should trigger
                            </p>
                            <p v-else style="color: #c9a86a;">
                                "No match" detects changes, "match" confirms presence
                            </p>
                        </div>
                        
                        <!-- Master Selection (for slaves) -->
                        <div class="form-group" v-if="form.monitor_type === 'slave'">
                            <label>Master Monitor *</label>
                            <select v-model.number="form.master_id">
                                <option :value="null">-- Select a Master --</option>
                                <option v-for="m in masterMonitors" :key="m.id" :value="m.id">
                                    {{ m.name }} (ID: {{ m.id }})
                                </option>
                            </select>
                            <p>This monitor will only run when the selected master is active</p>
                        </div>
                    </div>
                    
                    <!-- TAB 4: Action & Cooldown -->
                    <div v-show="activeTab === 'action'" class="tab-pane">
                        <!-- Action Type -->
                        <div class="form-group">
                            <label>Action Type</label>
                            <select v-model="form.action.type">
                                <option value="keypress">Press Single Key</option>
                                <option value="hotkey">Hotkey Combination</option>
                                <option value="log">Log Only (No Action)</option>
                            </select>
                        </div>
                        
                        <!-- Action Key -->
                        <div class="form-group" v-if="form.action.type !== 'log'">
                            <label>Key to Press *</label>
                            <input v-model="form.action.key" placeholder="e.g., space, h, f1, enter">
                            <p>Examples: space, h, f1, escape, enter</p>
                        </div>
                        
                        <!-- Cooldown -->
                        <div class="form-group">
                            <label>Cooldown (ms)</label>
                            <input v-model.number="form.cooldown" type="number" min="0" step="100" placeholder="1000">
                            <p>Minimum time between triggers (milliseconds)</p>
                        </div>
                    </div>
                </div>
                
                <!-- Action Buttons -->
                <div style="display: flex; gap: 10px; margin-top: 30px; padding-top: 20px; border-top: 2px solid #6b4423;">
                    <button class="btn btn-primary" @click="save" style="flex: 1;">
                        💾 {{ monitor.id ? 'Update' : 'Save' }} Monitor
                    </button>
                    <button class="btn btn-danger" @click="$emit('close')">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    `,
    methods: {
        addPixel() {
            // Check limits
            const currentCount = this.allPixels.length;

            if (this.form.monitor_type !== 'master' && currentCount >= 1) {
                alert('Normal and Slave monitors can only have one pixel. Change to Master type for multi-pixel.');
                return;
            }
            if (currentCount >= 6) {
                alert('Maximum 6 pixels allowed');
                return;
            }

            // Set picking index and emit
            this.pickingForIndex = currentCount;
            this.$emit('pick-pixel');
        },

        removePixel(index) {
            if (this.allPixels.length === 1) {
                alert('At least one pixel is required');
                return;
            }

            // Remove from the unified list
            if (index === 0) {
                // If removing first pixel, move second to main position
                if (this.form.pixel_group.length > 0) {
                    const secondPixel = this.form.pixel_group[0];
                    this.form.x = secondPixel.x;
                    this.form.y = secondPixel.y;
                    this.form.target_color = secondPixel.color;
                    this.form.pixel_group.splice(0, 1);
                }
            } else {
                // Remove from pixel_group (index - 1 because first pixel is separate)
                this.form.pixel_group.splice(index - 1, 1);
            }
        },

        handlePixelPicked(pixel) {
            const pixelData = {
                x: pixel.x,
                y: pixel.y,
                color: [pixel.r, pixel.g, pixel.b],
                tolerance: this.form.tolerance
            };

            // Determine where to place the pixel based on current state
            const currentPixelCount = this.allPixels.length;

            if (currentPixelCount === 0) {
                // First pixel ever - set as main
                this.form.x = pixel.x;
                this.form.y = pixel.y;
                this.form.target_color = [pixel.r, pixel.g, pixel.b];
                this.form.colorPreview = pixel.hex;
            } else {
                // Additional pixel - add to pixel_group
                if (!this.form.pixel_group) {
                    this.form.pixel_group = [];
                }
                this.form.pixel_group.push(pixelData);
            }

            this.pickingForIndex = null;
        },

        getPixelColor(color) {
            return `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        },

        save() {
            const validation = ValidationService.validateMonitor(this.form);

            if (!validation.isValid) {
                ValidationService.showErrors(validation.errors);
                return;
            }

            this.$emit('save', this.form);
        }
    },
    computed: {
        masterMonitors() {
            return (this.monitors || []).filter(m => m.monitor_type === 'master');
        },

        allPixels() {
            // Combine main pixel and pixel_group into one array for display
            const pixels = [];

            // Add main pixel if it exists
            if (this.form.x && this.form.y) {
                pixels.push({
                    x: this.form.x,
                    y: this.form.y,
                    color: this.form.target_color
                });
            }

            // Add all pixels from pixel_group
            if (this.form.pixel_group) {
                pixels.push(...this.form.pixel_group);
            }

            return pixels;
        }
    }
};

