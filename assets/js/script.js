// Gestion du formulaire de contact
document.addEventListener('DOMContentLoaded', function() {
    const contactForms = document.querySelectorAll('#contact-form');
    
    contactForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Récupération des valeurs du formulaire
            const name = form.querySelector('#name').value;
            const email = form.querySelector('#email').value;
            const message = form.querySelector('#message').value;
            
            // Ici, vous pourriez ajouter une logique pour envoyer les données à un serveur
            console.log('Formulaire soumis:', { name, email, message });
            
            // Affichage d'un message de confirmation
            alert('Merci pour votre message ! Nous vous contacterons bientôt.');
            
            // Réinitialisation du formulaire
            form.reset();
        });
    });

    // Animation des cartes de projet au chargement
    const projectCards = document.querySelectorAll('.project-card, .service-card');
    
    project