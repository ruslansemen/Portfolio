'use strict';
const video = document.querySelector('video');
const playBtn = document.querySelector('.fa-play');
const pauseBtn = document.querySelector('.fa-pause');
const volume = document.querySelector('.volume');
const timing = document.querySelector('.timing');
const currentTimeEl = document.querySelector('.currentTime');

let wasVideoPlaying = false;
let progressIdentifier = null;

window.addEventListener('load', function () {
    timing.min = 0;
    timing.max = video.duration;
});

playBtn.addEventListener("click", function () {
    if (video.paused) {
        video.play();
        progressIdentifier = setInterval(changeProgress, 100);
    }
});

pauseBtn.addEventListener("click", function () {
    if (!video.paused) {
        video.pause();
        clearInterval(progressIdentifier);
    }
});

timing.addEventListener("mouseup", function (event) {
    video.currentTime = timing.value;
    if (wasVideoPlaying) {
        video.play();
        progressIdentifier = setInterval(changeProgress, 100);
    }
});

timing.addEventListener("mousedown", function (event) {
    clearInterval(progressIdentifier);
    wasVideoPlaying = !video.paused;
    if (wasVideoPlaying) {
        video.pause();
    }
});

function changeProgress() {
    currentTimeEl.innerHTML = video.currentTime;
    timing.value = video.currentTime;
}

video.addEventListener('ended', function () {
    clearInterval(progressIdentifier);
});

volume.addEventListener("change", function () {
    video.volume = volume.value;
});