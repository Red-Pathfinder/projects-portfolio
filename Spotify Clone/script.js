const audio = document.getElementById('audio');
const play = document.getElementById('play');
const previous = document.getElementById('previous');
const next = document.getElementById('next');
const shuffle = document.getElementById('shuffle');
const repeat = document.getElementById('repeat');
const progress = document.querySelector('.progress');
const progressBar = document.querySelector('.progress-bar');
const currentTimeEl = document.getElementById('currentTime');
const totalTimeEl = document.getElementById('totalTime');
const title = document.getElementById('title');
const artist = document.getElementById('artist');
const songImg = document.getElementById('song-img');
const volumeIcon = document.getElementById('volume-icon');
const volumeBar = document.getElementById('volume-bar');


const songs = [
    {
        title: 'Mahiye Jinna Sohna',
        artist: 'Darshan Raval',
        img_src: './Media/card2img.jpeg',
        src: './Media/Mahiye-Jinna-Sohna.mp3'
    },
    {
        title: 'Mere Pass Tum Ho',
        artist: 'Silent Ocean',
        img_src: './Media/card3img.jpeg',
        src: './Media/Mere-Pass-Tum-Ho.mp3'
    },
    {
        title: 'Naa Ready',
        artist: 'Anirudh Ravichander',
        img_src: './Media/card4img.jpeg',
        src: './Media/Naa-Ready.mp3'
    }
];

let currentSongIndex = 0;
let isPlaying = false;
let isShuffle = false;
let isRepeat = false;

function playSong() {
    isPlaying = true;
    play.classList.remove('fa-play');
    play.classList.add('fa-pause');
    audio.play();
}

function pauseSong() {
    isPlaying = false;
    play.classList.remove('fa-pause');
    play.classList.add('fa-play');
    audio.pause();
}

function loadSong(song) {
    title.textContent = song.title;
    artist.textContent = song.artist;
    songImg.src = song.img_src;
    audio.src = song.src;
}

function nextSong() {
    currentSongIndex++;
    if (currentSongIndex > songs.length - 1) {
        currentSongIndex = 0;
    }
    loadSong(songs[currentSongIndex]);
    playSong();
}

function previousSong() {
    currentSongIndex--;
    if (currentSongIndex < 0) {
        currentSongIndex = songs.length - 1;
    }
    loadSong(songs[currentSongIndex]);
    playSong();
}

function updateProgress(e) {
    const { duration, currentTime } = e.srcElement;
    const progressPercent = (currentTime / duration) * 100;
    progress.style.width = `${progressPercent}%`;
}

function setProgress(e) {
    const width = this.clientWidth;
    const clickX = e.offsetX;
    const duration = audio.duration;
    audio.currentTime = (clickX / width) * duration;
}

function formatTime(time) {
    const minutes = Math.floor(time / 60);
    let seconds = Math.floor(time % 60);
    if (seconds < 10) {
        seconds = `0${seconds}`;
    }
    return `${minutes}:${seconds}`;
}

function shuffleSongs() {
    isShuffle = !isShuffle;
    if (isShuffle) {
        shuffle.classList.add('active');
    } else {
        shuffle.classList.remove('active');
    }
}

function repeatSong() {
    isRepeat = !isRepeat;
    if (isRepeat) {
        repeat.classList.add('active');
        audio.loop = true;
    } else {
        repeat.classList.remove('active');
        audio.loop = false;
    }
}

play.addEventListener('click', () => (isPlaying ? pauseSong() : playSong()));
next.addEventListener('click', nextSong);
previous.addEventListener('click', previousSong);
shuffle.addEventListener('click', shuffleSongs);
repeat.addEventListener('click', repeatSong);

audio.addEventListener('timeupdate', updateProgress);
progressBar.addEventListener('click', setProgress);

audio.addEventListener('ended', () => {
    if (isShuffle) {
        let randomIndex;
        do {
            randomIndex = Math.floor(Math.random() * songs.length);
        } while (randomIndex === currentSongIndex);
        currentSongIndex = randomIndex;
        loadSong(songs[currentSongIndex]);
        playSong();
    } else {
        nextSong();
    }
});

audio.addEventListener('loadedmetadata', () => {
    totalTimeEl.textContent = formatTime(audio.duration);
});

audio.addEventListener('timeupdate', () => {
    currentTimeEl.textContent = formatTime(audio.currentTime);
});

volumeBar.addEventListener('input', (e) => {
    audio.volume = e.target.value;
    if (audio.volume === 0) {
        volumeIcon.classList.remove('fa-volume-high');
        volumeIcon.classList.add('fa-volume-off');
    } else {
        volumeIcon.classList.remove('fa-volume-off');
        volumeIcon.classList.add('fa-volume-high');
    }
});

loadSong(songs[currentSongIndex]);

// Alert for missing audio files
audio.addEventListener('error', () => {
    alert("Error: Audio file not found. Please make sure 'Mahiye-Jinna-Sohna.mp3', 'Mere-Pass-Tum-Ho.mp3', and 'Naa-Ready.mp3' are in the Media folder.");
});