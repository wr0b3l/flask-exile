// Pixel Display - Shows pixel information (position + color)
const PixelDisplay = {
    props: {
        x: Number,
        y: Number,
        color: Array,  // [r, g, b]
        label: String,
        removable: {
            type: Boolean,
            default: false
        }
    },
    template: `
        <div class="pixel-display">
            <span v-if="label" class="pixel-label">{{ label }}</span>
            <div class="pixel-info">
                <div class="pixel-position">
                    📌 ({{ x }}, {{ y }})
                </div>
                <div class="pixel-color-info">
                    <div 
                        class="color-box-small" 
                        :style="{ background: colorHex }">
                    </div>
                    <span class="color-values">
                        RGB({{ color[0] }}, {{ color[1] }}, {{ color[2] }})
                    </span>
                </div>
            </div>
            <button 
                v-if="removable" 
                class="btn btn-danger btn-sm" 
                @click="$emit('remove')"
                type="button">
                🗑️
            </button>
        </div>
    `,
    computed: {
        colorHex() {
            const [r, g, b] = this.color;
            return `rgb(${r}, ${g}, ${b})`;
        }
    }
};

