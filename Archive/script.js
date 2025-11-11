let totalPoints = 0;
document.addEventListener("DOMContentLoaded", function () {
    let labels = document.querySelectorAll('label');
    for (let i = 0; i < labels.length; i++) {
        let label = labels[i];
        if (label) {
            label.addEventListener('click', function (e) {
                if (e.target.nextElementSibling.className == 'checkmark') {
                    console.log('ok');
                    totalPoints++;
                    e.target.parentElement.parentElement.nextElementSibling.style.display = "block";
                } else if (e.target.nextElementSibling.className == 'crossmark') {
                    console.log('wrong');
                    totalPoints--;
                    e.target.parentElement.parentElement.nextElementSibling.nextElementSibling.style.display = "block";
                }
                let quest = e.target.parentElement.parentElement.previousElementSibling;
                if (quest) {
                    quest = quest.innerHTML;
                    let answer = e.target.parentElement.textContent.toString();
                    let message = quest + ":" + answer;
                    send_mess(message);
                }
            });
        }
    }
});


function send_mess(message) {
    let request = new XMLHttpRequest();
    let url_addr = 'http://home.inw.net.ua/message.php?q=' + message;
    console.log(url_addr);
    request.open('GET', url_addr, true);

    request.onload = function () {
        console.log(this.status);
    };
    request.onerror = function () {
        console.log("There was a connection error of some sort")
    };
    request.send();
}