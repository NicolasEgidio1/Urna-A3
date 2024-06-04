document.getElementById('voting-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
    if (selectedCandidate) {
        alert(`Você votou no ${selectedCandidate.value}`);
    } else {
        alert('Por favor, selecione um candidato antes de votar.');
    }
});
