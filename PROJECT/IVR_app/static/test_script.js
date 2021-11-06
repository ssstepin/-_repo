q_arr = [];

let q_n = document.getElementById("q_num").textContent.split(" ");
q_n = Number(q_n[q_n.length - 1]);
console.log(q_n);

for (let i = 0; i < q_n; ++i) {
    q_arr[i] = {
        q_obj: document.getElementById("q" + String(i)),
        q_btn: document.getElementsByName("btnq" + String(i))[0],
        number: i
    };
    if (i !== 0) q_arr[i].q_obj.style.display = 'none';
}

//console.log(q_arr);

q_arr.forEach(function (item, i, q_arr) {
    //console.log(item);
    item.q_btn.addEventListener('click', function () {
        //console.log(item);
        console.log(document.forms[0].elements['q' + String(item.number)]);
        //if(typeof document.forms[0].elements['q' + String(item.number)] === 'array')
        if (document.forms[0].elements['q' + String(item.number)].length) {
            document.forms[0].elements['q' + String(item.number)].forEach(function (item2) {
                if (item2.checked) {
                    item.q_btn.disabled = true;
                    if (item.number !== q_arr.length - 1) q_arr[item.number + 1].q_obj.style.display = '';
                }
            })
        } else {
            if (document.forms[0].elements['q' + String(item.number)].value !== '') {
                item.q_btn.disabled = true;
                if (item.number !== q_arr.length - 1) q_arr[item.number + 1].q_obj.style.display = '';
            }
        }
    });
})

function isLetter(str) {
    return str.length === 1 && (str.match(/[a-z]/i) || str.match(/[а-я]/i));
}

const inputHandler = function (e) {
    let str = e.data;
    for (let i = 0; i < str.length; ++i) {
        if (!isLetter(str[i])) {
            alert("Неверный формат ввода!");
            return;
        }
    }
}

let all_texts = document.querySelectorAll('input[type=text]');
for (let i = 0; i < all_texts.length; ++i) {
    all_texts[i].addEventListener('input', inputHandler);
    //all_texts[i].addEventListener('propertychange', inputHandler);
    //all_texts[i].addEventListener('change', inputHandler);
}