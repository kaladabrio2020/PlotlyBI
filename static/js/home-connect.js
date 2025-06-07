document.addEventListener('DOMContentLoaded', function() {
    // connect
    var button_ = document.querySelector('.connect-button button');
    button_.addEventListener('click', function() {
        try{
            var modal = document.getElementById('modal-connect-db');
            modal.style.display = 'block';
        }catch(error){
            alert(error);
        }
    });
    var sair = document.querySelectorAll('#modal-connect-db button')[1];
    sair.addEventListener('click', function() {
        try{
            var modal = document.getElementById('modal-connect-db');
            modal.style.display = 'none';
        }catch(error){
            alert(error);
        }
    });
})
