const scores = document.querySelectorAll(".score");
const scoreUp = document.querySelectorAll(".score-up");
const scoreDown = document.querySelectorAll(".score-down");
const scoreValue = document.querySelectorAll(".score-value");

scores.forEach(item => {
    item.addEventListener("click", (e) => {
        const target = e.target;
        const parent = target.parentElement;
        const up = parent.children[0];
        const down = parent.children[2];
        const score = parent.children[1];
        const classNames = {
            up : "score-up-post",
            down : "score-down-post"
        }
        
        if (target.classList.contains("score-up")) {
            if (up.classList.contains(classNames.up)) {
                up.classList.remove(classNames.up)
                score.innerHTML = parseInt(score.innerHTML) - 1
            } else {
                up.classList.add(classNames.up);
                if (down.classList.contains(classNames.down)) {
                    down.classList.remove(classNames.down)
                    score.innerHTML = parseInt(score.innerHTML) + 2
                } else {
                    score.innerHTML = parseInt(score.innerHTML) + 1
                }
            }
        } else if (target.classList.contains("score-down")) {
            if (down.classList.contains(classNames.down)) {
                down.classList.remove(classNames.down)
                score.innerHTML = parseInt(score.innerHTML) + 1

            } else {
                down.classList.add(classNames.down);
                if (up.classList.contains(classNames.up)) {
                    up.classList.remove(classNames.up)
                    score.innerHTML = parseInt(score.innerHTML) - 2
                } else {
                    score.innerHTML = parseInt(score.innerHTML) - 1
                }
            }
        }
    })
})

