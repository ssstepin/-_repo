function changeColorRed(){
    (document.getElementById("q1d")).style.backgroundColor = "red";
}

function changeColorGreen(obj){
    (document.getElementById("q1d")).style.backgroundColor = "green";
}


const question1y = document.getElementById("q1y");
const question1n = document.getElementById("q1n");

question1y.onclick = changeColorGreen;