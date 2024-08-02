function hello() {
    alert("Hello, world.");
}

function change() {
    const header = document.querySelector('#hello');
    if (header.innerHTML === "Hello!") {
        header.innerHTML = 'Goodbye!';
    }
    else {
        header.innerHTML = "Hello!";
    }
}

function count() {
    counter++;
    document.querySelector("#count").innerHTML = counter;

    if (counter % 10 === 0) {
        alert(`Count is now ${counter}`)
    }
}

function buttonChanger () {
    document.querySelectorAll('button').forEach(function (button) {
        button.onclick = function () {
        }
    })
}
// variables
var age = 54; // var -> global variable
let counter = 0; // let -> local variable. applies to current block.
const age3 = 14; // value that cannot change

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#counter').onclick = count;
    event.preventDefault(); // used for preventing the console reloading
});