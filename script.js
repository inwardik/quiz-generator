let totalPoints = 0;
document.addEventListener("DOMContentLoaded", function(){
   let labels = document.querySelectorAll('label');
   for (let i = 0; i < labels.length; i++){
       let label = labels[i];
       if (label){
           label.addEventListener('click', function(e){
               if (e.target.nextElementSibling.className == 'checkmark'){
                   console.log('ok');
                   totalPoints++;
                   e.target.parentElement.parentElement.nextElementSibling.style.display = "block";
               }
               else if (e.target.nextElementSibling.className == 'crossmark'){
                   console.log('wrong');
                   totalPoints--;
                   e.target.parentElement.parentElement.nextElementSibling.nextElementSibling.style.display = "block";
               }
           });
       }
   }
});