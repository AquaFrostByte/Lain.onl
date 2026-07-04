// 1. Your images and their specific links
var imagesArray = [
    { src: "/static/img/88x31/Github.gif", link: "https://github.com/AquaFrostByte" },
    { src: "/static/img/88x31/insta.gif",   link: "https://www.instagram.com/aquafrostbyte" },
    { src: "/static/img/88x31/ditchsocial.gif",   link: "" },
    { src: "/static/img/88x31/enterogermina.gif",   link: "https://enterogermina.neocities.org" },
    { src: "/static/img/88x31/ia.gif", link: "https://web.archive.org/" }
];

// Add the CSS animation dynamically to the page
const style = document.createElement('style');
style.textContent = `
    .blink-fade {
        opacity: 0;
        transition: opacity 0.5s ease-in-out;
    }
    #x88 {
        transition: opacity 0.5s ease-in-out;
    }
`;
document.head.appendChild(style);

// Function to handle updating the image and link
function updateImage() {
    var container = document.getElementById("Friends");
    if (!container) return; // Guard clause if container isn't loaded yet

    var index = Math.floor(Math.random() * imagesArray.length);
    var selectedItem = imagesArray[index];

    // Replace the inner HTML of the container
    container.innerHTML = `
        <a href="${selectedItem.link}">
            <img src="${selectedItem.src}" alt="Header Image" id="x88">
        </a>
    `;
}

// Initial load so the page isn't blank at start
updateImage();

// Loop every 5 seconds
setInterval(function() {
    var img = document.getElementById("x88");
    
    if (img) {
        // 1. Start fading out (takes 0.5s)
        img.classList.add("blink-fade");
        
        // 2. Bring it back up to full opacity right as it changes (takes another 0.5s)
        setTimeout(function() {
            img.classList.remove("blink-fade");
        }, 500);
    }
    
    // 3. Exactly 1 second after the blink starts, swap the image/link
    setTimeout(updateImage, 1000);

}, 5000);