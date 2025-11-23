// Form Group - Reusable form field wrapper
const FormGroup = {
    props: {
        label: String,
        help: String,
        required: Boolean
    },
    template: `
        <div class="form-group">
            <label v-if="label">
                {{ label }}
                <span v-if="required" style="color: #cd5c5c;">*</span>
            </label>
            <slot></slot>
            <p v-if="help" style="color: #8b7355; font-size: 0.85em; margin-top: 5px;">
                {{ help }}
            </p>
        </div>
    `
};

