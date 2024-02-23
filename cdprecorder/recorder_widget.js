// logo_src is taken from python

let elemLoaded = false;

const wrapper = document.createElement("div");
wrapper.style["width"] = "100%"

const elem = document.createElement("div");
// elem.style["all"] = "initial";
elem.style["position"] = "fixed";
elem.style["z-index"] = 16777271;
elem.style["right"] = 0;
elem.style["top"] = 0;
elem.style["background-color"] = "rgba(127,127,127,0.5)";
elem.style["border-radius"] = "5px";
elem.draggable = "true";

const drag_button = document.createElement("div");
// drag_button.style["all"] = "initial";
drag_button.style["background-color"] = "rgba(255,255,255,0.6)";
drag_button.style["data-unselectable"] = "unselectable content";
drag_button.style["border-radius"] = "5px 5px 0px 0px";
drag_button.style["display"] = "flex";
drag_button.style["justify-content"] = "center";
drag_button.style["-webkit-touch-callout"] = "none";
drag_button.style["-webkit-user-select"] = "none";
drag_button.style["-khtml-user-select"] = "none";
drag_button.style["-moz-user-select"] = "none";
drag_button.style["-ms-user-select"] = "none";
drag_button.style["user-select"] = "none";
drag_button.style["font-size"] = "15pt";
// drag_button.style["display"] = "block";
drag_button.textContent = "✥"
elem.append(drag_button);

const timer_wrapper = document.createElement("div");
timer_wrapper.style["display"] = "flex";
timer_wrapper.style["flex-wrap"] = "wrap";

const timer_pad = document.createElement("div");
timer_pad.style["flex"] = "20%";
// timer_pad.style["height"] = "1px";
timer_pad.style["display"] = "inline";
timer_pad.style["display"] = "flex";
timer_pad.style["align-items"] = "stretch";
timer_pad.style["position"] = "relative";
timer_wrapper.append(timer_pad);

const inner_circle = document.createElement("div");
inner_circle.style["background"] = "red";
inner_circle.style["background"] = "linear-gradient(135deg, rgb(255,0,0) 0%, rgb(230,120,100) 90%)";
inner_circle.style["border-radius"] = "50%";
inner_circle.style["width"] = "30%";
inner_circle.style["height"] = "30%";
inner_circle.style["top"] = "35%";
inner_circle.style["left"] = "35%";
inner_circle.style["position"] = "absolute";

const outer_circle = document.createElement("div");
outer_circle.style["background"] = "rgb(190, 190, 190)";
outer_circle.style["border-radius"] = "50%";
outer_circle.style["border"] = "1px solid black";
outer_circle.style["width"] = "60%";
outer_circle.style["height"] = "60%";
outer_circle.style["top"] = "20%";
outer_circle.style["left"] = "20%";
outer_circle.style["position"] = "absolute";

timer_pad.append(outer_circle);
timer_pad.append(inner_circle);

const timer_div = document.createElement("div");
timer_div.textContent = "";
timer_div.style["flex"] = "60%";
timer_div.style["display"] = "inline";
timer_div.style["font-size"] = "x-large";
timer_div.style["text-align"] = "center";
timer_wrapper.append(timer_div);

const logo_div = document.createElement("div");
logo_div.style["flex"] = "20%";

const logo = document.createElement("img");
logo.src = logo_src;
logo.style["max-width"] = "100%";
logo.style["display"] = "inline";
logo.style["float"] = "right";
logo.style["-webkit-mask"] = "radial-gradient(circle, rgba(255, 255, 255, 1) 10%, rgba(255, 255, 255, 0) 70%)";
logo.style["mask"] = "radial-gradient(circle, rgba(255, 255, 255, 1) 10%, rgba(255, 255, 255, 0) 70%)";
logo_div.append(logo);
//radial-gradient(circle, rgba(255, 255, 255, 1) 10%, rgba(255, 255, 255, 0) 70%)

timer_wrapper.append(logo_div);

elem.append(timer_wrapper);

let p1 = 0;
let p2 = 0;
let click_start_x = 0;
let click_start_y = 0;

let rel_x = 0;
let rel_y = 0;

let startTime = null;
function startTimer() {
    startTime = new Date();
}

function startTimerIfElemLoaded() {
    if (elemLoaded) {
        startTime = new Date();
    }
}

function setTimerElapsed(elapsed_seconds) {
    startTime = new Date() - elapsed_seconds * 1000;
    updateTimer();
    return startTime;
}

function elapsedTime() {
    if (startTime === null) {
        return "";
    }
    const elapsed = new Date(new Date() - startTime);
    const hour = elapsed.getUTCHours().toString().padStart(2, '0')
    const minute = elapsed.getUTCMinutes().toString().padStart(2, '0')
    const second = elapsed.getUTCSeconds().toString().padStart(2, '0')
    return `${hour}:${minute}:${second}`;
}

function updateTimer() {
    timer_div.textContent = elapsedTime();
}

setInterval(updateTimer, 1000);

drag_button.onmousedown = (e) => {
    e = e || window.event;
    e.preventDefault();
    click_start_x = e.clientX;
    click_start_y = e.clientY;

    let rect = elem.getBoundingClientRect();
    rel_x = e.clientX - rect.x;
    rel_y = e.clientY - rect.y;

    document.onmouseup = () => {
        // This is not the best way of doing it 
        document.onmouseup = null;
        document.onmousemove = null;
    }
    document.onmousemove = (e) => {
        let rect = elem.getBoundingClientRect();

        p1 = click_start_x - e.clientX;
        p2 = click_start_y - e.clientY;
        click_start_x = e.clientX;
        click_start_y = e.clientY;

        window.innerWidth
        // x = (elem.offsetTop - p2);
        // y = (elem.offsetLeft - p1);
        x = e.clientX - rel_x;
        y = e.clientY - rel_y;
        if (x < 0) {
            elem.style.left = 0;
        } else if (x + rect.width > window.innerWidth) {
            // x = window.innerWidth - rect.width;
            elem.style.right = 0;
        } else {
            elem.style.left = x + "px";
        }

        if (y < 0) {
            y = 0;
        } else if (y + rect.height > window.innerHeight) {
            y = window.innerHeight - rect.height;
        }

        elem.style.top = y + "px";
    };
};

window.onresize = function() {
    let rect = elem.getBoundingClientRect();
    let x = rect.x;
    let y = rect.y;
    if (rect.x < 0) {
        elem.style.left = 0;
    } else if (rect.x + rect.width > window.innerWidth) {
        elem.style.left = (window.innerWidth - rect.width) + "px";
    }

    if (rect.y < 0) {
        elem.style.top = 0;
    } else if (rect.y + rect.height > window.innerHeight) {
        elem.style.top = (window.innerHeight - rect.height) + "px";
    }
};

if (document.body) {
    elemLoaded = true;
    document.body.append(elem);
} else {
    document.addEventListener("DOMContentLoaded", () => {
        elemLoaded = true;
        document.body.append(elem);
    });
}

const min_watcher = window.matchMedia("(max-width: 700px)");
const max_watcher = window.matchMedia("(max-width: 1200px)");

function set_width() {
    if (min_watcher.matches) {
        elem.style["width"] = "100px";
    } else if (max_watcher.matches) {
        elem.style["width"] = "200px";
    } else {
        elem.style["width"] = "250px";
    }
}

set_width();

min_watcher.addEventListener("change", function() {
    set_width();
});

max_watcher.addEventListener("change", function() {
    set_width();
});
