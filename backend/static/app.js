// Main App
const { createApp } = Vue;

const app = createApp({});

// Register shared components
app.component('form-group', FormGroup);
app.component('color-preview', ColorPreview);
app.component('pixel-display', PixelDisplay);
app.component('action-buttons', ActionButtons);

// Register feature components
app.component('app-header', AppHeader);
app.component('quick-actions', QuickActions);
app.component('monitors-list', MonitorsList);
app.component('activity-log', ActivityLog);
app.component('monitor-modal', MonitorModal);
app.component('app-container', AppContainer);

// Mount app
app.mount('#app');

