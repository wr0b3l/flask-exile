// Validation Service - Form validation logic
const ValidationService = {
    // Validate monitor form data
    validateMonitor(form) {
        const errors = [];

        if (!form.name || form.name.trim() === '') {
            errors.push('Monitor name is required');
        }

        if (!form.x && form.x !== 0) {
            errors.push('Please pick a pixel to set X coordinate');
        }

        if (!form.y && form.y !== 0) {
            errors.push('Please pick a pixel to set Y coordinate');
        }

        if (!form.target_color || !form.target_color[0] && form.target_color[0] !== 0) {
            errors.push('Please pick a pixel to set color');
        }

        if (form.tolerance < 0 || form.tolerance > 255) {
            errors.push('Tolerance must be between 0 and 255');
        }

        if (form.cooldown < 0) {
            errors.push('Cooldown must be a positive number');
        }

        if (form.action.type !== 'log' && !form.action.key) {
            errors.push('Please enter a key to press');
        }

        if (form.monitor_type === 'slave' && !form.master_id) {
            errors.push('Please select a master monitor');
        }

        // Validate pixel group - only for masters
        if (form.pixel_group && form.pixel_group.length > 0) {
            if (form.monitor_type !== 'master') {
                errors.push('Multi-pixel monitoring is only available for master monitors');
            }
            if (form.pixel_group.length > 5) {
                errors.push('Maximum 5 additional pixels allowed');
            }
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    },

    // Show validation errors
    showErrors(errors) {
        if (errors.length === 1) {
            alert(errors[0]);
        } else if (errors.length > 1) {
            alert('Please fix the following errors:\n\n• ' + errors.join('\n• '));
        }
    }
};

