//These are the ad Banners i am not affiliated with anyone of them other then Archmania which is my own Project! :3
// CHnage these freely to ur likeing! please dont click on any links they can change over time and i am not responsible for them!!
const AdBanners = [
    { link: "https://archmania.lain.onl/", img: "/static/img/ads/ArchMainiaAD.gif" },
    { link: "http://www.gamespy.com/", img: "/static/img/ads/GamespyDaily.gif" },
    { link: "https://www.counter-strike.net/", img: "/static/img/ads/Cstrike.gif" },
    { link: "https://isp.netscape.com/", img: "/static/img/ads/Netscape.gif" },
    { link: "https://en.wikipedia.org/wiki/Quake_(video_game)", img: "/static/img/ads/Quake.jpeg" },
];
let currentIndex = 0;
function AdRottation() {
    currentIndex = (currentIndex + 1) % AdBanners.length;
    const Link = document.getElementById("AdBannerLink");
    const Image = document.getElementById("AdBannerImg");
    Link.href = AdBanners[currentIndex].link;
    Image.src = AdBanners[currentIndex].img;
}
setInterval(AdRottation, 5000);