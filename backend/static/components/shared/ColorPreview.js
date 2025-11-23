// Color Preview - Shows color with RGB values
const ColorPreview = {
    props: {
        color: Array,  // [r, g, b]
        size: {
            type: String,
            default: '40px'
        }
    },
    template: `
        <div class="color-preview-component">
            <div 
                class="color-box" 
                :style="{ 
                    width: size, 
                    height: size, 
                    background: colorHex,
                    border: '2px solid #6b4423'
                }">
            </div>
            <span v-if="color" class="color-text">
                RGB({{ color[0] }}, {{ color[1] }}, {{ color[2] }})
            </span>
        </div>
    `,
    computed: {
        colorHex() {
            if (!this.color || this.color.length !== 3) return '#fff';
            const [r, g, b] = this.color;
            return `rgb(${r}, ${g}, ${b})`;
        }
    }
};

