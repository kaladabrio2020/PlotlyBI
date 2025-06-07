document.addEventListener('DOMContentLoaded', function() {
    const navbarButtons = document.querySelectorAll('.navbar_button');
    const modals = document.querySelectorAll('.modal');
    
    // Função para esconder todos os modais e o conteúdo principal
    function hideAllContent() {
        modals.forEach(modal => {
            modal.classList.remove('active');
        });
        navbarButtons.forEach(btn => {
            btn.classList.remove('active');
        });
    }
    
    // Função para mostrar o conteúdo principal

    
    // Função para mostrar um modal específico
    function showModal(modalId) {
        hideAllContent();
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    }
    
    // Adicionar event listeners para os botões
    navbarButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modalType = this.getAttribute('data-modal');
            this.classList.add('active');
            
            switch(modalType) {
                case 'database':
                    showModal('modal-database');
                    break;
                case 'file':
                    showModal('modal-file');
                    break;
                case 'home':
                    showModal('modal-home');
                    break;
                default:
                    showMainContent();
            }
        });
    });
});