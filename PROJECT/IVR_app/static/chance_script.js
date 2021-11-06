let cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
let button = document.getElementById("subm");

document.getElementsByName("q1").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[0] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q2").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[1] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q3").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[2] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q4").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[3] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q5").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[4] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q6").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[5] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q7").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[6] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q8").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[7] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q9").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[8] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});

document.getElementsByName("q10").forEach((elem) => {
    elem.addEventListener("change", () => {
        cnt[9] = 1;
        if (Number(cnt.reduce((a, b) => a + b, 0)) === Number(10)) {
            button.disabled = false;
        }
    })
});