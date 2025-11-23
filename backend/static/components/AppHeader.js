// Header Component
const AppHeader = {
    props: ['isConnected'],
    template: `
        <div class="header">
            <h1>
            Flask
                <img src="/static/images/logo.png" alt="Flask Exile" class="header-logo" :class="{ connected: isConnected }">
                Exile
            </h1>
        </div>
    `
};

