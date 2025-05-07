function openModal(imgSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    modal.style.display = "block";
    modalImg.src = imgSrc;

    modal.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
        }
    };

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}

function closeModal() {
    document.getElementById('imageModal').style.display = "none";
}