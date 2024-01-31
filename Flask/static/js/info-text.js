document.addEventListener('DOMContentLoaded', function(){
    const infoButton = document.getElementById('upload_info');
    const infoText = document.getElementById('upload_help_text');

    infoButton.addEventListener('mouseover', function() {
        infoText.style.display = 'block';
    });

    infoButton.addEventListener('mouseout', function() {
        infoText.style.display = 'none';
    });
});