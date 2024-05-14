<script>
    // Fonction pour récupérer les valeurs du formulaire
    function getFormValues() {
        var depart = document.getElementById("depart").textContent;
        var destination = document.getElementById("destination").textContent;
        return {
            depart: depart,
            destination: destination
        };
    }

    // Fonction pour mettre à jour l'itinéraire sur la carte
    function updateRoute() {
        var formValues = getFormValues();
        if (formValues.depart && formValues.destination) {
            // Mise à jour de l'itinéraire avec les nouvelles valeurs
            var startPoint = formValues.depart.split(': ')[1];
            var endPoint = formValues.destination.split(': ')[1];
            searchBoxA.search(startPoint);
            searchBoxB.search(endPoint);
        }
    }

    // Associer la fonction de mise à jour de l'itinéraire à l'événement de clic sur le bouton "Calculer"
    document.getElementById("calculateBtn").addEventListener("click", function(event) {
        event.preventDefault();
        updateRoute();
    });

    // Mettre à jour l'itinéraire lors du chargement de la page
    updateRoute();
</script>
