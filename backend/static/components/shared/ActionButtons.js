// Action Buttons - Standard button sets
const ActionButtons = {
    props: {
        saveText: {
            type: String,
            default: 'Save'
        },
        cancelText: {
            type: String,
            default: 'Cancel'
        },
        saveIcon: {
            type: String,
            default: '💾'
        }
    },
    template: `
        <div class="action-buttons">
            <button class="btn btn-primary" @click="$emit('save')" style="flex: 1;" type="button">
                {{ saveIcon }} {{ saveText }}
            </button>
            <button class="btn btn-danger" @click="$emit('cancel')" type="button">
                {{ cancelText }}
            </button>
        </div>
    `
};

